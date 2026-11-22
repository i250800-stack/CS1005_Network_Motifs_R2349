# =============================================================
# Member 4: T6 Z-scores (T7 chart is made in Excel: member4_T7_chart.xlsx)
# CS1005 Discrete Structures - Fall 2026 - Network Motifs Project
# =============================================================
# GROUP PARAMETERS (derived from R, Section 5 of the project statement)
#   R                       = 3309
#   Department A            = top-20[4]      = 1
#   Department B            = top-20[14]     = 5
#   Number of random nets   = 20 + (R mod 31) = 43
#
# Run after member3.py, from the same folder:
#       python member4.py
#
# Inputs (written by member3.py):
#   member3_T4_triad_counts.csv       (observed counts in the real subgraphs)
#   member3_random_network_counts.csv (counts in each of the 43 random networks)
#
# Outputs:
#   member4_Z_table_A.csv   (13 Z-scores, Department A)
#   member4_Z_table_B.csv   (13 Z-scores, Department B)
#   member4_z_scores.csv    (A and B together)
#
# The T7 grouped bar chart is built in Excel from member4_z_scores.csv
# (see member4_T7_chart.xlsx and chart.png).
# =============================================================

import csv
import math

R = 3309
NUM_RANDOM_NETWORKS = 20 + (R % 31)
DEPT_A = 1   # top-20[4]
DEPT_B = 5   # top-20[14]

FIELDS = ["department", "department_id", "class", "observed_count",
          "random_mean", "population_std_dev", "z_score", "interpretation"]


# ---------------- load Member 3's output ----------------

def load_observed():
    """Return {"A": [13 counts], "B": [13 counts]} from the T4 table."""
    observed = {"A": [0] * 13, "B": [0] * 13}
    with open("member3_T4_triad_counts.csv", newline="") as file:
        for row in csv.DictReader(file):
            if row["class"] == "total":
                continue
            k = int(row["class"]) - 1
            observed["A"][k] = int(row["department_A_id_%d" % DEPT_A])
            observed["B"][k] = int(row["department_B_id_%d" % DEPT_B])
    return observed


def load_random_counts():
    """Return {"A": [[13 counts] for each random network], "B": ...}."""
    nets = {"A": {}, "B": {}}
    with open("member3_random_network_counts.csv", newline="") as file:
        for row in csv.DictReader(file):
            counts = nets[row["department"]].setdefault(int(row["random_network"]), [0] * 13)
            counts[int(row["class"]) - 1] = int(row["triad_count"])
    randomized = {}
    for label in ("A", "B"):
        randomized[label] = [nets[label][n] for n in sorted(nets[label])]
        assert len(randomized[label]) == NUM_RANDOM_NETWORKS, "expected 43 random networks"
    return randomized


# ---------------- T6: Z-scores ----------------

def compute_z_scores(observed, randomized_counts):
    """For each class k: Z = (observed - mean) / std, using the population std.
    If std = 0 the Z-score is reported as 0."""
    means, stds, z_scores = [], [], []
    for k in range(13):
        values = [counts[k] for counts in randomized_counts]
        mean_value = sum(values) / NUM_RANDOM_NETWORKS
        variance = sum((v - mean_value) ** 2 for v in values) / NUM_RANDOM_NETWORKS
        std_value = math.sqrt(variance)           # population std deviation
        z_value = 0 if std_value == 0 else (observed[k] - mean_value) / std_value
        means.append(mean_value)
        stds.append(std_value)
        z_scores.append(z_value)
    return means, stds, z_scores


def interpret(z):
    if z > 2:
        return "Motif"
    if z < -2:
        return "Anti-motif"
    return "Neither"


def save_results(results):
    def row_for(result, i):
        return {
            "department": result["label"], "department_id": result["department_id"],
            "class": i + 1, "observed_count": result["observed"][i],
            "random_mean": round(result["means"][i], 4),
            "population_std_dev": round(result["stds"][i], 4),
            "z_score": round(result["z_scores"][i], 4),
            "interpretation": interpret(result["z_scores"][i]),
        }

    with open("member4_z_scores.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        for result in results:
            for i in range(13):
                writer.writerow(row_for(result, i))

    for result in results:                       # one table per department
        with open(f"member4_Z_table_{result['label']}.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            for i in range(13):
                writer.writerow(row_for(result, i))


def main():
    print("R =", R)
    print("Department A =", DEPT_A, ", Department B =", DEPT_B)
    print("Random networks =", NUM_RANDOM_NETWORKS)

    observed = load_observed()
    randomized = load_random_counts()

    results = []
    for label, department_id in [("A", DEPT_A), ("B", DEPT_B)]:
        means, stds, z_scores = compute_z_scores(observed[label], randomized[label])
        results.append({
            "label": label, "department_id": department_id,
            "observed": observed[label],
            "means": means, "stds": stds, "z_scores": z_scores,
        })

        print("\nDepartment", label, "(ID:", department_id, ")")
        print("Observed triad counts:", observed[label])
        print("Z-scores:", [round(z, 4) for z in z_scores])
        print("Motifs:", [i + 1 for i, z in enumerate(z_scores) if z > 2])
        print("Anti-motifs:", [i + 1 for i, z in enumerate(z_scores) if z < -2])

    save_results(results)
    print("\nSaved member4_z_scores.csv, member4_Z_table_A.csv and member4_Z_table_B.csv.")


if __name__ == "__main__":
    main()
