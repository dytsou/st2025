#!/bin/bash

test_path="${BASH_SOURCE[0]}"
solution_path="$(realpath .)"
tmp_dir=$(mktemp -d -t lab6-XXXXXXXXXX)
answer=""

cd $tmp_dir

rm -rf *
cp $solution_path/Makefile .
cp $solution_path/ans .
cp $solution_path/chal .
cp $solution_path/*.txt .

if [ "$1" -eq 1 ]; then
  if grep -q "[^a-zA-Z0-9]" 1.txt; then
    echo "[!] 1.txt contains non-alphanumeric characters."
    exit 1
  fi
fi

if [ "$1" -eq 2 ]; then
  if ! grep -q "[^[:print:]]" 2.txt; then
    echo "[!] 2.txt must contain at least one non-printable character."
    exit 1
  fi
fi

make run$1 > out
result=$(diff --strip-trailing-cr ans out)
if [[ -n $result ]]; then
  echo "[!] Expected: "
  cat ans
  echo ""
  echo "[!] Actual:   "
  cat out
  echo ""
  exit 1
else
  echo "[V] Pass"
fi

rm -rf $tmp_dir

exit 0

# vim: set fenc=utf8 ff=unix et sw=2 ts=2 sts=2:
