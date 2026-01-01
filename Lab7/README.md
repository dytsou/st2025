# Lab7

## Introduction

In this lab, you will write a LLVM pass in `llvm-pass/afl-demo-pass.so.cc` and `llvm-pass/afl-demo-rt.o.c`, and enable AFL++ to detect command injection vulnerabilities.

## Environment (Important.)

1. x86_64 machine
2. Ubuntu 22.04
3. llvm-14

## Requirement

**(100%)** In this lab, you will write a LLVM pass in `llvm-pass/afl-demo-pass.so.cc` & `llvm-pass/afl-demo-rt.o.c` and satisfy the following requirements.
1. When running afl++ to fuzz the `program`, the `program` can't crash by `system("echo AAA");` at line 34 in `program.c`. It's not command injection, and you will see the error message below when you try to fuzz:
    ```
    [-] PROGRAM ABORT : We need at least one valid input seed that does not crash!
    ```
    Of course, you can not just detect this line to avoid it. We will modify this command and add additional system functions (which won't cause command injection) in `program.c` during testing with your fuzzer.
2. When running afl++ to fuzz the `program`, the fuzzer needs to find the command injection `system(cmd)` at line 18 in `program.c`.
3. Write a report in `{student_ID}.pdf` to explain your work.
    - Your report must include the following sections.
        - Your name and student ID,
        - Explanation of your work
        - Copy the crash fuzzer report and crash input (use `xxd`) in `{student_ID}.pdf`.

**Template**

    Name:
    student_ID:

    ```
    Explanation of your work
    ```

    Crash fuzzer report
    ```

                american fuzzy lop ++4.01c {default} (./program) [fast]
    ┌─ process timing ────────────────────────────────────┬─ overall results ────┐
    │        run time : 0 days, 0 hrs, 0 min, 18 sec      │  cycles done : 9     │
    │   last new find : 0 days, 0 hrs, 0 min, 8 sec       │ corpus count : 7     │
    │last saved crash : 0 days, 0 hrs, 0 min, 3 sec       │saved crashes : 1     │
    │ last saved hang : none seen yet                     │  saved hangs : 0     │
    ├─ cycle progress ─────────────────────┬─ map coverage┴──────────────────────┤
    │  now processing : 5.3 (71.4%)        │    map density : 30.77% / 76.92%    │
    │  runs timed out : 0 (0.00%)          │ count coverage : 39.40 bits/tuple   │
    ├─ stage progress ─────────────────────┼─ findings in depth ─────────────────┤
    │  now trying : havoc                  │ favored items : 7 (100.00%)         │
    │ stage execs : 312/1175 (26.55%)      │  new edges on : 7 (100.00%)         │
    │ total execs : 97.2k                  │ total crashes : 1 (1 saved)         │
    │  exec speed : 5329/sec               │  total tmouts : 1 (0 saved)         │
    ├─ fuzzing strategy yields ────────────┴─────────────┬─ item geometry ───────┤
    │   bit flips : disabled (default, enable with -D)   │    levels : 6         │
    │  byte flips : disabled (default, enable with -D)   │   pending : 0         │
    │ arithmetics : disabled (default, enable with -D)   │  pend fav : 0         │
    │  known ints : disabled (default, enable with -D)   │ own finds : 6         │
    │  dictionary : n/a                                  │  imported : 0         │
    │havoc/splice : 4/38.3k, 3/58.5k                     │ stability : 100.00%   │
    │py/custom/rq : unused, unused, unused, unused       ├───────────────────────┘
    │    trim/eff : 0.00%/7, disabled                    │          [cpu000: 12%]
    └────────────────────────────────────────────────────┘

    ```
    Crash Input:
    ```
    $ xxd output/default/crashes/id\:000000\,sig\:06\,src\:000006\,time\:15137\,execs\:81803\,op\:havoc\,rep\:2
    00000000: 4655 5a5a 2146 ec40                      FUZZ!F.@
    ```

## Submission

1. Lab7 will not have GitHub CI, so the grade of Lab7 will be determined with your report `{student_ID}.pdf`
2. Submit the report `{student_ID}.pdf` to explain your work.
3. You must submit these two files `llvm-pass/afl-demo-pass.so.cc` and `llvm-pass/afl-demo-rt.o.c`.
4. You need to commit and push the corresponding changes to your repository, which contains the code that satisfies the aforementioned requirements.
