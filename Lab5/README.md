# Lab5

## Introduction

In this lab, you will write a function to bypass the detection of ASan in `antiasan.c`.

## Requirement

1. (100%) Write a function antoasan to bypass the detection of ASan in `antiasan.c`.
You can run `validate.sh` in your local environment to test if you satisfy the requirements.

Please note that you must not alter files other than `antiasan.c`, `antiasan.h`. You will get 0 points if

1. You modify other files to achieve the requirements.
2. You can't pass all CI on your PR.
3. You use `__asan_unpoison_memory_region` function.

## Submission

You need to commit and push the corresponding changes to your repository, which contains the code that satisfies the aforementioned requirements.
