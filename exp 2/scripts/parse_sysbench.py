#!/usr/bin/env python3
"""
parse_sysbench.py
=================
Experiment 2: Memory Performance Analysis (VM vs Docker Container)

Extracts and aggregates Sysbench memory benchmark metrics from raw output logs.
Calculates statistical summaries (Mean, Std Dev) and relative performance deltas.
"""

import glob
import os
import re
import statistics as stats
import sys

# Regex patterns matching Sysbench 1.0.x memory output format
METRIC_PATTERNS = {
    "total_ops": (r"Total operations:\s*(\d+)", int),
    "ops_per_sec": (r"Total operations:\s*\d+\s*\(([\d\.]+)\s*per second\)", float),
    "throughput_mib_s": (r"\(([\d\.]+)\s*MiB/sec\)", float),
    "total_time_s": (r"total time:\s*([\d\.]+)s", float),
    "latency_min_ms": (r"min:\s*([\d\.]+)", float),
    "latency_avg_ms": (r"avg:\s*([\d\.]+)", float),
    "latency_max_ms": (r"max:\s*([\d\.]+)", float),
    "latency_p95_ms": (r"95th percentile:\s*([\d\.]+)", float),
    "latency_sum_ms": (r"sum:\s*([\d\.]+)", float),
}


def parse_sysbench_log(file_path):
    """Parses a single Sysbench log file and returns extracted metrics."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    results = {}
    for metric_name, (pattern, dtype) in METRIC_PATTERNS.items():
        match = re.search(pattern, content)
        if match:
            results[metric_name] = dtype(match.group(1))
        else:
            results[metric_name] = None
    return results


def summarize_environment(env_name, base_dir):
    """Summarizes all run logs for a specific environment."""
    pattern = os.path.join(base_dir, "results", "raw", "memory", env_name, "run_*.txt")
    files = sorted(glob.glob(pattern))

    if not files:
        print(f"[-] No logs found for {env_name} matching {pattern}")
        return None

    parsed_runs = [parse_sysbench_log(f) for f in files]
    print(f"\n=======================================================")
    print(f" Summary for {env_name.upper()} ({len(parsed_runs)} run(s) analyzed)")
    print(f"=======================================================")

    summary = {}
    for metric_name in METRIC_PATTERNS:
        valid_vals = [r[metric_name] for r in parsed_runs if r[metric_name] is not None]
        if not valid_vals:
            continue
        mean_val = stats.mean(valid_vals)
        std_val = stats.stdev(valid_vals) if len(valid_vals) > 1 else 0.0
        summary[metric_name] = {"mean": mean_val, "stddev": std_val, "samples": valid_vals}
        print(f"  {metric_name:<20}: Mean = {mean_val:>12.4f} | StdDev = {std_val:>10.4f}")

    return summary


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)

    print("Analyzing Experiment 2 Sysbench Memory logs...")
    vm_summary = summarize_environment("vm", base_dir)
    container_summary = summarize_environment("container", base_dir)

    if vm_summary and container_summary:
        print("\n=======================================================")
        print(" Comparative Performance Analysis (Container vs VM)")
        print("=======================================================")

        # Throughput delta
        vm_tp = vm_summary["throughput_mib_s"]["mean"]
        ct_tp = container_summary["throughput_mib_s"]["mean"]
        tp_diff_pct = ((ct_tp - vm_tp) / vm_tp) * 100.0

        # Max latency delta
        vm_max_lat = vm_summary["latency_max_ms"]["mean"]
        ct_max_lat = container_summary["latency_max_ms"]["mean"]
        lat_diff_pct = ((ct_max_lat - vm_max_lat) / vm_max_lat) * 100.0

        # Total time delta
        vm_time = vm_summary["total_time_s"]["mean"]
        ct_time = container_summary["total_time_s"]["mean"]
        time_diff_pct = ((ct_time - vm_time) / vm_time) * 100.0

        print(f"  Throughput (MiB/s):  VM = {vm_tp:.2f} | Container = {ct_tp:.2f} | Delta = {tp_diff_pct:+.2f}%")
        print(f"  Total Time (sec):    VM = {vm_time:.4f} | Container = {ct_time:.4f} | Delta = {time_diff_pct:+.2f}%")
        print(f"  Max Latency (ms):    VM = {vm_max_lat:.2f} | Container = {ct_max_lat:.2f} | Delta = {lat_diff_pct:+.2f}%")
        print("=======================================================\n")


if __name__ == "__main__":
    main()
