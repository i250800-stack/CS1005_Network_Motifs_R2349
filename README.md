CS1005 Discrete Structures - Fall 2026 Project
Finding Network Motifs in an Email Network

Group R = 2349

Group Members
- [Member 1 Name] - [Roll Number] (Member 1)
- Ayesha Hassan - i250800 (Group Leader)
- [Member 3 Name] - [Roll Number] (Member 3)

Derived Parameters
- R: 2349
- Pair Number: 69 -> (3, 19)
- Department A: top20[3] = ID 21
- Department B: top20[19] = ID 20
- Number of Random Networks: 44
- Swap Attempts: 8 × edges
- Random Seed: 2349

How to Run
1. Download the dataset files (email-Eu-core.txt and email-Eu-core-department-labels.txt) from the SNAP website and place them in the root folder.
2. Compile the C++ code: g++ main.cpp -o main
3. Run the executable: ./main

---

Task 3 & Task 4 (Member 2's Contributions)

Hand-Worked Example (Class 1, Canonical Code 3)
Let's classify a triad where Node a sends emails to Node b and Node c (edges a->b, a->c).
1. Order (a, b, c): a->b is Bit 0, a->c is Bit 1. Code = 3.
2. Order (a, c, b): a->c is Bit 0, a->b is Bit 1. Code = 3.
3. Order (b, a, c): No matching edges. Code = 0.
4. Order (b, c, a): No matching edges. Code = 0.
5. Order (c, a, b): No matching edges. Code = 0.
6. Order (c, b, a): No matching edges. Code = 0.

The minimum code across all 6 permutations is 3. According to the project statement, Code 3 maps to Class 1.

Table 1: Triad Census for Department A (ID 21)
Class 1: 126
Class 2: 113
Class 3: 908
Class 4: 44
Class 5: 19
Class 6: 174
Class 7: 420
Class 8: 919
Class 9: 0
Class 10: 30
Class 11: 41
Class 12: 423
Class 13: 985
Total Connected Triads: 4202

Table 2: Triad Census for Department B (ID 20)
Class 1: 2
Class 2: 2
Class 3: 23
Class 4: 0
Class 5: 0
Class 6: 1
Class 7: 16
Class 8: 24
Class 9: 0
Class 10: 1
Class 11: 0
Class 12: 14
Class 13: 48
Total Connected Triads: 131

Verification Note
We implemented a built-in 4-test verification function in our code to ensure our bit-mapping and counting logic is correct. The tests output the expected class for known edge configurations, and all tests pass successfully.

---

Task 5, 6 & 7 (Member 3's Contributions)
(Member 3 should fill this section with the Z-score tables, the bar chart image, and the explanation of how the randomization works).

---

Contributions
- Member 1: Data preprocessing, Top-20 computation, [add other tasks].
- Member 2 (Leader): T3 (Triad Classification), T4 (Triad Counting), Hand-worked example, Verification test, Department A and B count tables, Repository setup.
- Member 3: T5 (Randomization), T6 (Z-Scores), T7 (Chart), Interpretation of differences.
