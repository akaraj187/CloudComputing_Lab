#!/usr/bin/env python3
"""
generate_plots.py
=================
Experiment 2: Memory Performance Visualization (VM vs Docker Container)

Generates comparative multi-panel bar charts visualizing:
1. Memory Throughput (MiB/sec) - Higher is better
2. Total Execution Time (seconds) - Lower is better
3. Maximum Latency Spikes (milliseconds) - Lower is better

Saves output figure to ../images/memory-comparison.png
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.dirname(script_dir)
    images_dir = os.path.join(exp_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    # Benchmark results from experimental runs
    labels = ["Ubuntu VM\n(VMware Workstation)", "Docker Container\n(Ubuntu 24.04)"]
    colors = ["#2b5c8f", "#2e7d32"]  # High-contrast professional palette

    # Key metrics
    throughput = [108900.87, 123725.89]   # MiB/sec
    total_time = [0.0931, 0.0819]         # Seconds
    max_latency = [3.04, 1.13]            # Milliseconds

    # Create 3-panel figure
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.8), dpi=150)
    plt.subplots_adjust(wspace=0.35)

    metrics_config = [
        (throughput, "Memory Throughput", "MiB/sec", "(Higher is Better)", "{:,.2f}"),
        (total_time, "Total Execution Time", "Seconds", "(Lower is Better)", "{:.4f}"),
        (max_latency, "Maximum Latency Spike", "Milliseconds (ms)", "(Lower is Better)", "{:.2f}"),
    ]

    for ax, (data, title, ylabel, subtitle, fmt) in zip(axes, metrics_config):
        bars = ax.bar(labels, data, color=colors, width=0.55, edgecolor="#1a1a1a", linewidth=1.2)
        ax.set_title(f"{title}\n{subtitle}", fontsize=11, fontweight="bold", pad=10)
        ax.set_ylabel(ylabel, fontsize=10, fontweight="semibold")
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        ax.set_axisbelow(True)

        # Annotate values on top of bars
        for bar, val in zip(bars, data):
            height = bar.get_height()
            ax.annotate(
                fmt.format(val),
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=9.5,
                fontweight="bold"
            )

        # Set subtle headroom for labels
        y_max = max(data) * 1.15
        ax.set_ylim(0, y_max)

    fig.suptitle(
        "Experiment 2: Sysbench Memory Benchmark — VM vs Docker Container\n(Workload: 1 MiB Block Size | 10 GiB Total Transfer | 4 Threads | Global Write)",
        fontsize=12,
        fontweight="bold",
        y=1.03
    )

    out_file = os.path.join(images_dir, "memory-comparison.png")
    plt.savefig(out_file, bbox_inches="tight", dpi=150)
    plt.close()
    print(f"[+] Successfully generated benchmark chart: {out_file}")

if __name__ == "__main__":
    main()
