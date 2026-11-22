# =============================================================
# Member 3: T4 Triad Counting + T5 Randomization
# CS1005 Discrete Structures - Fall 2026 - Network Motifs Project
# =============================================================
# GROUP PARAMETERS (derived from R, Section 5 of the project statement)
#   R                       = 3309
#   Pair number             = R mod 190      = 79  -> (i, j) = (4, 14)
#   Department A            = top-20[4]      = 1
#   Department B            = top-20[14]     = 5
#   Number of random nets   = 20 + (R mod 31) = 43
#   Swap attempts / network = (5 + (R mod 6)) * edges = 8 * edges
#   Random seed             = R = 3309
#       Network k (k = 0..42) uses seed R + k, so every random
#       network is different but the whole run is reproducible.
#
# Run from the folder containing clean_edges.csv and department_labels.csv:
#       python member3.py
#
# Outputs:
#   member3_T4_triad_counts.csv       (T4: 13 observed counts x 2 departments)
#   member3_random_network_counts.csv (T5: triad counts of every random network)
#
# Member 4 reads these two files in member4.py to compute the Z-scores (T6)
# and draw the chart (T7).
# =============================================================

import csv
import random
import itertools

R = 3309
PAIR_NUMBER = R % 190
NUM_RANDOM_NETWORKS = 20 + (R % 31)
SWAP_MULTIPLIER = 5 + (R % 6)
SEED = R
DEPT_A = 1   # top-20[4]
DEPT_B = 5   # top-20[14]

EDGE_BITS = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]
CODE_TO_CLASS = {
    3: 1, 6: 2, 7: 3, 10: 4, 11: 5, 15: 6, 21: 7,
    23: 8, 25: 9, 27: 10, 30: 11, 31: 12, 63: 13,
}


# ---------------- triad classification (same as Member 2's T3) ----------------

def triad_class(a, b, c, edges):
    """Return the connected triad class (1-13), or 0 if disconnected."""
    best_code = 64
    for order in itertools.permutations((a, b, c)):
        code = 0
        for bit, (i, j) in enumerate(EDGE_BITS):
            if (order[i], order[j]) in edges:
                code |= (1 << bit)
        best_code = min(best_code, code)
    return CODE_TO_CLASS.get(best_code, 0)


def degree_signature(edges, nodes):
    """Return (in-degree dictionary, out-degree dictionary)."""
    in_degree = {node: 0 for node in nodes}
    out_degree = {node: 0 for node in nodes}
    for u, v in edges:
        out_degree[u] += 1
        in_degree[v] += 1
    return in_degree, out_degree


# ---------------- T5: RANDOMIZATION ----------------

def randomize(edges, attempts, seed):
    """
    Return one randomized graph (list of edges) made by double-edge swaps.

    One attempt: pick two edges (a,b), (c,d) uniformly at random and replace
    them with (a,d), (c,b). The attempt is rejected (graph unchanged) if
    a == d, c == b, (a,d) already exists, or (c,b) already exists.
    Rejected attempts still count towards `attempts`.
    The input list is never modified: every call starts from the original.
    """
    rng = random.Random(seed)
    current_edges = list(edges)
    edge_set = set(current_edges)

    for _ in range(attempts):
        i = rng.randrange(len(current_edges))
        j = rng.randrange(len(current_edges))
        if i == j:                      # same edge picked twice -> rejected
            continue

        a, b = current_edges[i]
        c, d = current_edges[j]
        new_edge_1 = (a, d)
        new_edge_2 = (c, b)

        if a == d or c == b:            # would create a self-loop
            continue
        if new_edge_1 in edge_set or new_edge_2 in edge_set:   # parallel edge
            continue

        edge_set.remove((a, b))
        edge_set.remove((c, d))
        edge_set.add(new_edge_1)
        edge_set.add(new_edge_2)
        current_edges[i] = new_edge_1
        current_edges[j] = new_edge_2

    assert len(current_edges) == len(edge_set)
    return current_edges


# ---------------- T4: triad counting ----------------

def count_triads(edges, nodes):
    """
    Count all 13 connected triad classes, each connected triple exactly once.
    For every node, take every pair of its neighbours (in either direction);
    the triple is stored in a set (sorted) so duplicates disappear.
    """
    edge_set = set(edges)
    neighbours = {node: set() for node in nodes}
    for u, v in edge_set:
        neighbours[u].add(v)
        neighbours[v].add(u)

    candidate_triples = set()
    for center, adjacent in neighbours.items():
        adjacent = sorted(adjacent)
        for i in range(len(adjacent)):
            for j in range(i + 1, len(adjacent)):
                candidate_triples.add(tuple(sorted((center, adjacent[i], adjacent[j]))))

    counts = [0] * 13
    for a, b, c in candidate_triples:
        class_number = triad_class(a, b, c, edge_set)
        if class_number != 0:
            counts[class_number - 1] += 1
    return counts


def verify_counts_bruteforce(edges, nodes, counts):
    """T4 check only: test every 3-subset directly and compare with count_triads.
    (Too slow for large graphs, fine for our two small departments.)"""
    edge_set = set(edges)
    slow = [0] * 13
    for a, b, c in itertools.combinations(sorted(nodes), 3):
        k = triad_class(a, b, c, edge_set)
        if k != 0:
            slow[k - 1] += 1
    assert slow == counts, "triad counts disagree with brute force!"


def save_t4(results):
    with open("member3_T4_triad_counts.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["class", "department_A_id_%d" % DEPT_A, "department_B_id_%d" % DEPT_B])
        for k in range(13):
            writer.writerow([k + 1, results[0]["observed"][k], results[1]["observed"][k]])
        writer.writerow(["total", sum(results[0]["observed"]), sum(results[1]["observed"])])


# ---------------- data loading ----------------

def load_csv_data():
    edges = []
    with open("clean_edges.csv", newline="") as file:
        for row in csv.DictReader(file):
            edges.append((int(row["source"]), int(row["target"])))

    departments = {}
    with open("department_labels.csv", newline="") as file:
        for row in csv.DictReader(file):
            departments[int(row["node"])] = int(row["department"])
    return edges, departments


def get_department_graph(all_edges, departments, department_id):
    nodes = {n for n, dep in departments.items() if dep == department_id}
    edges = [(u, v) for u, v in all_edges if u in nodes and v in nodes]
    return nodes, edges


# ---------------- self-tests for T5 ----------------

def self_test_randomize():
    """Small hand-checkable tests of randomize()."""
    # 1. Degrees preserved and graph valid on a small graph
    small = [(0, 1), (2, 3), (4, 5), (1, 2), (3, 4), (5, 0)]
    nodes = set(range(6))
    out = randomize(small, 200, 1)
    assert degree_signature(out, nodes) == degree_signature(small, nodes)
    assert len(set(out)) == len(small) and all(u != v for u, v in out)

    # 2. Input list must not be modified
    original = list(small)
    randomize(small, 200, 2)
    assert small == original

    # 3. Same seed -> same result (reproducible)
    assert randomize(small, 200, 7) == randomize(small, 200, 7)

    # 4. Graph with only two edges that cannot be swapped:
    #    (0,1),(2,0): swap gives (0,0) -> self-loop -> always rejected
    stuck = [(0, 1), (2, 0)]
    assert sorted(randomize(stuck, 1000, 3)) == sorted(stuck)

    # 5. attempts = 0 -> graph unchanged
    assert randomize(small, 0, 5) == small


# ---------------- T4 + T5: analysis of one department ----------------

def analyze_department(label, department_id, nodes, original_edges):
    attempts = SWAP_MULTIPLIER * len(original_edges)
    original_degrees = degree_signature(original_edges, nodes)

    observed = count_triads(original_edges, nodes)       # T4
    verify_counts_bruteforce(original_edges, nodes, observed)
    randomized_counts = []

    for network_number in range(NUM_RANDOM_NETWORKS):
        network_seed = SEED + network_number
        randomized_edges = randomize(original_edges, attempts, network_seed)

        # T5 verification (required assert): in/out-degree of EVERY node unchanged
        assert degree_signature(randomized_edges, nodes) == original_degrees
        assert len(randomized_edges) == len(original_edges)
        assert len(set(randomized_edges)) == len(randomized_edges)
        assert all(u != v for u, v in randomized_edges)

        randomized_counts.append(count_triads(randomized_edges, nodes))

    return {
        "label": label, "department_id": department_id,
        "nodes": len(nodes), "edges": len(original_edges),
        "attempts": attempts, "observed": observed,
        "randomized_counts": randomized_counts,
    }


def save_random_counts(results):
    with open("member3_random_network_counts.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "department", "department_id", "random_network", "class", "triad_count"])
        writer.writeheader()
        for result in results:
            for net, counts in enumerate(result["randomized_counts"], start=1):
                for k, count in enumerate(counts, start=1):
                    writer.writerow({"department": result["label"],
                                     "department_id": result["department_id"],
                                     "random_network": net, "class": k,
                                     "triad_count": count})


def main():
    print("R =", R)
    print("Pair number =", PAIR_NUMBER, "-> Department A =", DEPT_A, ", Department B =", DEPT_B)
    print("Random networks =", NUM_RANDOM_NETWORKS)
    print("Swap multiplier =", SWAP_MULTIPLIER)
    print("Random seed =", SEED, "(network k uses seed R + k)")

    self_test_randomize()
    print("randomize() self-tests passed.")

    all_edges, departments = load_csv_data()

    results = []
    for label, department_id in [("A", DEPT_A), ("B", DEPT_B)]:
        nodes, edges = get_department_graph(all_edges, departments, department_id)
        result = analyze_department(label, department_id, nodes, edges)
        results.append(result)

        print("\nDepartment", label, "(ID:", department_id, ")")
        print("Nodes:", result["nodes"])
        print("Edges:", result["edges"])
        print("Swap attempts per network:", result["attempts"])
        print("Observed triad counts:", result["observed"])

    save_t4(results)
    save_random_counts(results)
    print("\nT4 counts verified against brute force for both departments.")
    print("T5 degree-preservation assertions passed for all",
          2 * NUM_RANDOM_NETWORKS, "randomized networks.")
    print("Saved member3_T4_triad_counts.csv and member3_random_network_counts.csv.")
    print("Next: run member4.py for the Z-scores (T6) and the chart (T7).")


if __name__ == "__main__":
    main()
