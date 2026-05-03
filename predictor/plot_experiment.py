import re
import os
import matplotlib.pyplot as plt
from collections import defaultdict

EXPERIMENT_RESULTS = "results_1-5"
OUTPUT = "result_plots"

# Algorithm accronim: exact result file name.
FILES = {
    "ABC": "results-abc.txt",
    "DTC": "results-dtc.txt",
    "ETC": "results-etc.txt",
    "GNB": "results-gnb.txt",
    "KNN": "results-knn.txt",
    "LDA": "results-lda.txt",
    "LR": "results-lr.txt",
    "LSVC": "results-lsvc.txt",
    "RFC": "results-rfc.txt",
    "SGD": "results-sgd.txt",
}

ALGO_FULL = {
    "ABC": "AdaBoost",
    "DTC": "Decision Tree",
    "ETC": "Extra Trees",
    "GNB": "Gaussian Naive Bayes",
    "KNN": "K-Nearest Neighbors",
    "LDA": "Linear Discriminant Analysis",
    "LR": "Logistic Regression",
    "LSVC": "Linear SVC",
    "RFC": "Random Forest",
    "SGD": "SGD Classifier",
}

# Output format regex
BLOCK_RE = re.compile(
    r"Running -\w+ with \[(.+?)\] on data_set_2/characteristics_(\d+)_(\d+)\.csv\s*---\s*"
    r"Accuracy:\s*([\d.]+)",
    re.DOTALL,
)


PLOT_PALETTE = [
    "#2196F3", "#E91E63", "#4CAF50", "#FF9800", "#9C27B0",
    "#00BCD4", "#F44336", "#8BC34A", "#FF5722", "#607D8B",
]

# Util to parse file to a list of (params_str, n, m, accuracy) tuples.
def parse_file(path):
    text = open(path).read()
    results = []

    for m in BLOCK_RE.finditer(text):
        params = m.group(1).strip()
        n = int(m.group(2))
        col = int(m.group(3))
        acc = float(m.group(4))
        results.append((params, n, col, acc))
    return results


if __name__ == "__main__":
    os.makedirs(OUTPUT, exist_ok=True)

    # Best algo accuracy for NxM
    algo_grid_best = {}
    # List of algo accuracies for NxM
    algo_grid_all = defaultdict(lambda: defaultdict(list))

    for algo, fname in FILES.items():
        path = os.path.join(EXPERIMENT_RESULTS, fname)
        rows = parse_file(path)

        grid_best = {}
        for params, n, m, acc in rows:
            key = (n, m)
            algo_grid_all[algo][key].append(acc)
            if key not in grid_best or acc > grid_best[key]:
                grid_best[key] = acc

        algo_grid_best[algo] = grid_best

    # Style
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.35,
        "grid.linestyle": "--",
    })

    # Graf 1: Primerjava vseh algoritmov
    # Za vsak algoritem: vzemi najboljšo točnost čez vse NxM kombinacije in zabelži katera NxM je bila to.

    algo_best_acc = {}
    algo_best_grid = {}

    for algo, grid_best in algo_grid_best.items():
        best_key = max(grid_best, key=grid_best.get)
        algo_best_acc[algo] = grid_best[best_key]
        algo_best_grid[algo] = best_key

    algos_sorted = sorted(algo_best_acc, key=algo_best_acc.get, reverse=True)
    accs_sorted = [algo_best_acc[a] for a in algos_sorted]
    grids_sorted = [algo_best_grid[a] for a in algos_sorted]
    labels = [ALGO_FULL[a] for a in algos_sorted]

    fig, ax = plt.subplots(figsize=(14, 7))

    bars = ax.barh(
        range(len(algos_sorted)),
        accs_sorted,
        color=[PLOT_PALETTE[i % len(PLOT_PALETTE)] for i in range(len(algos_sorted))],
        edgecolor="white",
        linewidth=0.8,
        height=0.65,
    )

    for i, (bar, acc, grid) in enumerate(zip(bars, accs_sorted, grids_sorted)):
        n, m = grid
        ax.text(
            acc + 0.001,
            bar.get_y() + bar.get_height() / 2,
            f"{acc:.4f}   ({n}×{m} grid)",
            va="center", ha="left", fontsize=9.5, color="#333333",
        )

    ax.set_yticks(range(len(algos_sorted)))
    ax.set_yticklabels(labels, fontsize=11)
    ax.set_xlabel("Točnost (Accuracy)", fontsize=12)
    ax.set_title(
        "Primerjava algoritmov strojnega učenja\n(najboljša točnost in optimalna NxM porazdelitev)",
        fontsize=14, fontweight="bold", pad=14,
    )
    ax.set_xlim(0, max(accs_sorted) * 1.22)
    ax.invert_yaxis()

    plt.tight_layout()
    out1 = os.path.join(OUTPUT, "splosna_primerjava_algoritmov.png")
    fig.savefig(out1, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out1}")

    # Graf 2: Po-algoritmični grafi (po 1 na algoritem, 10 skupaj)
    # Za vsak algoritem: za vsako NxM vzamemo najboljšo točnost (max čez parametre).
    # X-os: M (stolpci), vsaka linija = N (vrstice).

    for algo_idx, algo in enumerate(FILES.keys()):
        grid_best = algo_grid_best[algo]

        # Zberi vse N in M vrednosti
        all_n = sorted(set(k[0] for k in grid_best))
        all_m = sorted(set(k[1] for k in grid_best))

        fig, ax = plt.subplots(figsize=(9, 6))

        for ni, n in enumerate(all_n):
            x_vals, y_vals = [], []
            for m in all_m:
                key = (n, m)
                if key in grid_best:
                    x_vals.append(m)
                    y_vals.append(grid_best[key])

            color = PLOT_PALETTE[ni % len(PLOT_PALETTE)]
            ax.plot(
                x_vals, y_vals,
                marker="o", linewidth=2, markersize=7,
                color=color, label=f"N={n}",
            )

            # Označi vsako točko z vrednostjo
            for xv, yv in zip(x_vals, y_vals):
                ax.annotate(
                    f"{yv:.4f}",
                    (xv, yv),
                    textcoords="offset points",
                    xytext=(0, 8),
                    ha="center", fontsize=7.5, color=color,
                )

        ax.set_xticks(all_m)
        ax.set_xticklabels([f"M={m}" for m in all_m], fontsize=10)
        ax.set_xlabel("M (število stolpcev v gridu)", fontsize=11)
        ax.set_ylabel("Točnost (Accuracy)", fontsize=11)
        ax.set_title(
            f"{algo} – {ALGO_FULL[algo]}\nTočnost po NxM porazdelitvah",
            fontsize=13, fontweight="bold", pad=12,
        )
        ax.legend(title="N (vrstice)", fontsize=9, title_fontsize=9, loc="lower right")

        plt.tight_layout()
        out2 = os.path.join(OUTPUT, f"{algo.lower()}_po_razmerju_N_M.png")
        fig.savefig(out2, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"Saved: {out2}")

    print("\nVsi grafi so bili uspešno ustvarjeni.")
