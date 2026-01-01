# Lab6

## Introduction

In this lab, you will write a `solve.py` to learn how to use angr to execute the binary and find the correct input symbolically.

## Goal

This challenge is designed to test your skills in reverse engineering and symbolic execution. You will be working with a stripped ELF binary (`chal`) that contains multiple layers of traps and complex logic.

Your goal is to find **two secret 8-byte inputs** that cause the program to print the success message. You need to create a `solve.py` script that generates these two inputs and saves them as `1.txt` and `2.txt`.

Hints for the Inputs
*   The solution for `1.txt` consists of 8 **alphanumeric** bytes.
*   The solution for `2.txt` consists of 8 bytes that may include **non-printable** characters.
*   Remember that your final `.txt` files should contain the 8-byte secret followed by a newline character (`\n`), for a total of 9 bytes.

While other creative solutions might exist, this problem is specifically designed to be solved efficiently using **symbolic execution**. We strongly recommend using the **angr** framework to navigate the program's intricate paths and automatically solve for the correct inputs.

## Requirement

Your grade will be based on the following criteria:

1.  **(55%) Correctness**:
    *   (20%) Your generated `1.txt` passes the check from `./validate.sh 1`.
    *   (35%) Your generated `2.txt` passes the check from `./validate.sh 2`.
2.  **(15%)** You utilize angr to solve the problem.
2.  **(30%) Solution Report**:
    *   You must submit a report named `{student_id}_solution.pdf` (e.g., `314551001_solution.pdf`).
    *   This report should clearly explain your methodology, the challenges you encountered, and how you solved them. If you used `angr`, describe the features you used.
        *   Elapsed time your solution took to run.
        *   If you submit 1.txt or 2.txt, this report is required to be submitted, or you will get 0 points for the entire Lab 6.
    
### Bonus

1. **(10%)** Your solution report is well-organized, easy to read, and includes clear code snippets with syntax highlighting.
2. **(20%)** You use **angr** to solve the problem within 10 minutes. DEMO REQUIRED.
3. If you find more than two answers, please contact the TA via email, and you will receive some bonus rewards.

You will get 0 points if
1. You modify any other files (e.g., Makefile, validate.sh) or patch the binary (`chal`) to simplify the challenge.
2. You can't pass all CI on your PR.

## Submission

You need to commit and push the following files to your repository:
1. Your `solve.py` script (or any other scripts you use).
2. The generated `1.txt` and `2.txt` files.
3. Your final report, `{student_id}_solution.pdf`.

You need to commit and push the corresponding changes to your repository, which contains the code that satisfies the aforementioned requirements.

**Important**: The CI will **not** execute your `solve.py`. It will directly use the `1.txt` and `2.txt` files you commit to run the validation. Please ensure you have run your script locally to generate the correct files before committing.
