#!/usr/bin/env python3

"""
Angr-assisted solver for the stripped chal ELF. The script now performs the
entire preprocessing pipeline programmatically:

- Uses `angr.Project` + Capstone to scan `.text` for TEA artifacts without
  printing raw assembly. The TEA key is auto-located by detecting the delta
  constant (`0x9e3779b9`) and grouping [RIP+disp], imm32 stores that form
  the key array. The two 64-bit comparison constants are likewise recovered by
  hunting for movabs immediates.
- Applies double TEA decryption (since the binary encrypts twice) to derive the
  original 8-byte inputs, verifies by re-encrypting twice, and writes 1.txt
  (printable) / 2.txt (raw bytes).
"""

import angr
import struct
import sys

# TEA delta constant (derived from golden ratio)
DELTA = 0x9e3779b9

def tea_encrypt(v, key, rounds=32):
    """TEA encryption - implements the binary's encrypt function."""
    v0, v1 = v[0], v[1]
    sum_val = 0
    
    for _ in range(rounds):
        sum_val = (sum_val + DELTA) & 0xFFFFFFFF
        v0 = (v0 + (((v1 << 4) + key[0]) ^ (v1 + sum_val) ^ ((v1 >> 5) + key[1]))) & 0xFFFFFFFF
        v1 = (v1 + (((v0 << 4) + key[2]) ^ (v0 + sum_val) ^ ((v0 >> 5) + key[3]))) & 0xFFFFFFFF
    
    return (v0, v1)

def tea_decrypt(v, key, rounds=32):
    """TEA decryption - reverses the binary's encrypt function."""
    v0, v1 = v[0], v[1]
    sum_val = (DELTA * rounds) & 0xFFFFFFFF
    
    for _ in range(rounds):
        v1 = (v1 - (((v0 << 4) + key[2]) ^ (v0 + sum_val) ^ ((v0 >> 5) + key[3]))) & 0xFFFFFFFF
        v0 = (v0 - (((v1 << 4) + key[0]) ^ (v1 + sum_val) ^ ((v1 >> 5) + key[1]))) & 0xFFFFFFFF
        sum_val = (sum_val - DELTA) & 0xFFFFFFFF
    
    return (v0, v1)

def print_angr_disassembly(proj):
    """Dump the entire .text section using angr's Capstone interface."""
    text_sec = None
    for sec in proj.loader.main_object.sections:
        if sec.name == '.text':
            text_sec = sec
            break
    if text_sec is None:
        print("[warn] .text section not found", file=sys.stderr)
        return
    blob = proj.loader.memory.load(text_sec.vaddr, text_sec.memsize)
    cap = proj.arch.capstone
    print("=== Disassembly via angr/Capstone ===", file=sys.stderr)
    for insn in cap.disasm(bytes(blob), text_sec.vaddr):
        print(f"{insn.address:#08x}: {insn.mnemonic} {insn.op_str}", file=sys.stderr)
    print("=== End of disassembly ===", file=sys.stderr)

def explore_with_simgr(proj):
    """
    Demonstrate angr's simulation manager (simgr) for symbolic execution.
    This shows the stash-based exploration model: active, deadended, errored.
    """
    base = proj.loader.main_object.min_addr
    
    # Create an entry state at the program's entry point
    state = proj.factory.entry_state()
    
    # Create a simulation manager to manage exploration
    simgr = proj.factory.simgr(state)
    
    print("=== angr Simulation Manager Demo ===", file=sys.stderr)
    print(f"Initial state: {state}", file=sys.stderr)
    print(f"Entry point: {hex(state.addr)}", file=sys.stderr)
    
    # Step a few times to show how simgr works
    print("\nStepping through execution...", file=sys.stderr)
    for i in range(5):
        simgr.step()
        print(f"  Step {i+1}:", file=sys.stderr)
        print(f"    Active states: {len(simgr.active)}", file=sys.stderr)
        print(f"    Deadended states: {len(simgr.deadended)}", file=sys.stderr)
        if hasattr(simgr, 'errored'):
            print(f"    Errored states: {len(simgr.errored)}", file=sys.stderr)
        
        # Dump the current address of active states
        for idx, s in enumerate(simgr.active[:3]):
            print(f"      active[{idx}] @ {hex(s.addr)}", file=sys.stderr)
    
    print("\n=== End of simgr demo ===", file=sys.stderr)

def find_tea_key(proj):
    """
    Find TEA key by scanning for the delta constant (0x9e3779b9)
    and analyzing nearby mov instructions using Capstone's operand API.
    """
    from capstone import x86_const
    
    base = proj.loader.main_object.min_addr
    mem = proj.loader.memory
    
    # Get Capstone with detail mode enabled
    cap = proj.arch.capstone
    cap.detail = True
    
    # Find .text section
    text_sec = None
    for sec in proj.loader.main_object.sections:
        if sec.name == '.text':
            text_sec = sec
            break
    
    if text_sec is None:
        print("TEXT SECTION NOT FOUND IN BINARY", file=sys.stderr)
        return None
    
    blob = bytes(mem.load(text_sec.vaddr, text_sec.memsize))
    
    # Find TEA delta constant location
    delta_addr = None
    for insn in cap.disasm(blob, text_sec.vaddr):
        if insn.mnemonic == 'add':
            for op in insn.operands:
                if op.type == x86_const.X86_OP_IMM and op.imm == DELTA:
                    delta_addr = insn.address
                    print(f"Found TEA delta at {hex(delta_addr)}", file=sys.stderr)
                    break
        if delta_addr:
            break
    
    # Find mov dword ptr [RIP+disp], imm32 instructions
    # effective address = instruction address + instruction size + displacement
    key_candidates = []
    
    for insn in cap.disasm(blob, text_sec.vaddr):
        if insn.mnemonic == 'mov' and len(insn.operands) == 2:
            dst, src = insn.operands[0], insn.operands[1]
            
            # Check: dst is memory with RIP base, src is immediate
            if (dst.type == x86_const.X86_OP_MEM and 
                src.type == x86_const.X86_OP_IMM and
                dst.mem.base == x86_const.X86_REG_RIP):
                
                imm_val = src.imm & 0xFFFFFFFF
                # Calculate effective address for RIP-relative
                eff_addr = insn.address + insn.size + dst.mem.disp
                
                # Filter: large 32-bit values (likely key material)
                if imm_val > 0x10000000:
                    key_candidates.append((insn.address, imm_val, eff_addr))
    
    print(f"Found {len(key_candidates)} potential key values", file=sys.stderr)
    
    # Find cluster where effective addresses are 4 bytes apart (array of key words)
    key_candidates.sort(key=lambda x: x[0])  # Sort by instruction address for clustering
    
    for i in range(len(key_candidates) - 3):
        cluster = key_candidates[i:i+4]
        
        # Sort by effective address for contiguous array check
        cluster.sort(key=lambda x: x[2])
        
        # Check if they form a contiguous array of key words (4 bytes apart)
        eff_addrs = [c[2] for c in cluster]
        if all(eff_addrs[j+1] - eff_addrs[j] == 4 for j in range(3)):
            tea_key = [c[1] for c in cluster]  # Already sorted by effective address
            print(f"Found key array at {hex(eff_addrs[0])}: {[hex(k) for k in tea_key]}")
            return tea_key
    
    print("COULD NOT FIND TEA KEY", file=sys.stderr)
    return None


def find_tea_constants(proj):
    """
    Find 64-bit comparison constants using Capstone's operand API.
    """
    from capstone import x86_const
    
    mem = proj.loader.memory
    cap = proj.arch.capstone
    cap.detail = True
    
    text_sec = None
    for sec in proj.loader.main_object.sections:
        if sec.name == '.text':
            text_sec = sec
            break
    
    if text_sec is None:
        return None
    
    blob = bytes(mem.load(text_sec.vaddr, text_sec.memsize))
    
    # Find movabs instructions with 64-bit immediates
    constants = []
    
    for insn in cap.disasm(blob, text_sec.vaddr):
        if insn.mnemonic == 'movabs' and len(insn.operands) == 2:
            for op in insn.operands:
                if op.type == x86_const.X86_OP_IMM:
                    imm_val = op.imm
                    # Make unsigned if negative (Python issue with large values)
                    if imm_val < 0:
                        imm_val = imm_val & 0xFFFFFFFFFFFFFFFF
                    # 64-bit constant (larger than 32-bit range)
                    if imm_val > 0xFFFFFFFF:
                        constants.append((insn.address, imm_val))
    
    print(f"Found {len(constants)} movabs 64-bit constants", file=sys.stderr)
    
    if len(constants) >= 2:
        # Last two are typically the comparison values
        result = [c[1] for c in constants[-2:]]
        print(f"Extracted constants: {[hex(c) for c in result]}", file=sys.stderr)
        return result
    
    return None

def analyze_with_angr():
    """Use angr to analyze the binary and extract key/constant information."""
    proj = angr.Project('./chal', auto_load_libs=False)
    
    # print full disassembly:
    # print_angr_disassembly(proj)
    # Demonstrate simgr exploration (shows angr's symbolic execution capability)
    # explore_with_simgr(proj)
    
    # Find TEA key and constants
    key_words = find_tea_key(proj)
    constants = find_tea_constants(proj)

    return key_words, constants

def xor_all_bytes(val, xb):
    result = 0
    for i in range(8):
        byte = (val >> (i * 8)) & 0xFF
        result |= ((byte ^ xb) << (i * 8))
    return result

def main():
    """Compute the two secret inputs."""
    key_words, constants = analyze_with_angr()

    # Calculate the XOR key
    xor_key = 3
    for i in range(100):
        if i not in [13, 27, 87]:
            xor_key += (i % 10) + 1
    xor_byte = xor_key & 0xFF
    print(f"XOR key: {xor_key}, xor_byte: 0x{xor_byte:02x}", file=sys.stderr)

    # XOR the constants with the XOR key
    expected1 = xor_all_bytes(constants[0], xor_byte)
    expected2 = xor_all_bytes(constants[1], xor_byte)
    print(f"Expected 1: 0x{expected1:016x}", file=sys.stderr)
    print(f"Expected 2: 0x{expected2:016x}", file=sys.stderr)

    # Decrypt the solutions
    exp1_v = (expected1 & 0xFFFFFFFF, (expected1 >> 32) & 0xFFFFFFFF)
    exp2_v = (expected2 & 0xFFFFFFFF, (expected2 >> 32) & 0xFFFFFFFF)
    sol1_v = tea_decrypt(tea_decrypt(exp1_v, key_words), key_words)
    sol2_v = tea_decrypt(tea_decrypt(exp2_v, key_words), key_words)
    sol1_bytes = struct.pack('<II', sol1_v[0], sol1_v[1])
    sol2_bytes = struct.pack('<II', sol2_v[0], sol2_v[1])
    print(f"\nSolution 1: {sol1_bytes!r}", file=sys.stderr)
    print(f"Solution 2: {sol2_bytes!r}", file=sys.stderr)

    # Verify the solutions
    verify1 = tea_encrypt(tea_encrypt(sol1_v, key_words), key_words)
    verify2 = tea_encrypt(tea_encrypt(sol2_v, key_words), key_words)
    assert verify1 == exp1_v and verify2 == exp2_v, "Verification failed!"
    
    with open('1.txt', 'wb') as f:
        f.write(sol1_bytes + b'\n')
    with open('2.txt', 'wb') as f:
        f.write(sol2_bytes + b'\n')

if __name__ == '__main__':
    main()
