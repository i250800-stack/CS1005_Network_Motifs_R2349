CS1005 Discrete Structures - Fall 2026 Project
Finding Network Motifs in an Email Network

Group R = 3309

Group Members
- Farwa Fatima - 2 (Member 1 - Dataset & Parameters)
- Ayesha Hassan- 25i0800 (Member 2 - Subgraphs & Classification)
- [Name 3] - [Roll Number 3] (Member 3 - Counting & Randomization)
- [Name 4] - [Roll Number 4] (Member 4 - Analysis & Results)

Derived Parameters
- R: 3309
- Pair Number: 79 -> (4, 14)
- Department A: top20[4] = ID 1
- Department B: top20[14] = ID 5
- Number of Random Networks: 43
- Swap Attempts: 8 × edges
- Random Seed: 3309

How to Run
1. Run Member 1's notebook to generate clean_edges.csv and department_labels.csv.
2. Run Member 2's Python script to generate the induced subgraphs and classifications.
3. Run Member 3's Python script for counting and randomization.
4. Run Member 4's Python script for Z-scores and the chart.

---

Task 1 (Member 1's Contributions)
- Downloaded and loaded the email-Eu-core.txt and email-Eu-core-department-labels.txt datasets.
- Preprocessed the data by removing all self-loops and duplicate edges, resulting in 24,929 clean edges.
- Calculated the number of internal edges for all 42 departments.
- Generated the Top-20 department ranking based on internal edges.
- Calculated R = 3309 and all derived parameters (Pair number: 79, Dept A: 1, Dept B: 5, Random networks: 43, Swap multiplier: 8, Seed: 3309).
- Deliverables: Member1_Dataset_Parameters.ipynb, clean_edges.csv, department_labels.csv, top20_departments.csv, parameter_report.csv, and the extracted department node/edge CSV files.
---

Task 2 & Task 3 (Member 2's Contributions - My Work)

Induced Subgraphs (T2)
We created the induced subgraphs for Department A (ID 1) and Department B (ID 5).
- Department A: 65 Nodes, 502 Internal Edges
- Department B:18 Nodes, 147 Internal Edges

Hand-Worked Example (T3 - Class 1, Canonical Code 3)
Let's classify a triad where Node a sends emails to Node b and Node c (edges a->b, a->c).
1. Order (a, b, c): a->b is Bit 0, a->c is Bit 1. Code = 3.
2. Order (a, c, b): a->c is Bit 0, a->b is Bit 1. Code = 3.
3. Order (b, a, c): No matching edges. Code = 0.
4. Order (b, c, a): No matching edges. Code = 0.
5. Order (c, a, b): No matching edges. Code = 0.
6. Order (c, b, a): No matching edges. Code = 0.
The minimum code across all 6 permutations is 3. According to the project statement, Code 3 maps to Class 1.

Triad Classification Function (T3)
We implemented triad_class(a, b, c) in Python, which generates the canonical code for any given triad by checking all 6 node permutations and mapping the minimum code to one of the 13 connected classes. We included a 4-test verification function in the code which successfully passes.
Deliverables: Python code for subgraphs and triad_class, and hand-worked example.

---

Task 4 & Task 5 (Member 3's Contributions)
- Implemented efficient triad counting for both departments.
- Counted all 13 classes, avoiding duplicate counting.
- Implemented randomize(edges, attempts, seed).
- Performed double-edge swaps.
- Verified in-degree and out-degree preservation.
- Deliverables: Triad count tables and randomization function with assertions.

---

Task 6, 7 & 8 (Member 4's Contributions)
- Generated 43 random networks using Member 3's function.
- Calculated mean and population standard deviation.
- Calculated Z-scores for both departments.
- Identified motifs (Z > 2) and anti-motifs (Z < -2).
- Created grouped bar chart with ±2 dashed lines.
- Compared communication patterns of both departments.
- Deliverables: Z-score tables, chart, and comparison paragraph.
