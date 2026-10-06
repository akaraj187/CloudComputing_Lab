# Experiment 2: Host & Virtual Machine Specifications

This document records the baseline telemetry, CPU topology, memory layout, and virtualization parameters used during the benchmark.

---

## 1. CPU Configuration (`lscpu`)
* **Architecture:** `x86_64`
* **CPU op-mode(s):** 32-bit, 64-bit
* **Byte Order:** Little Endian
* **Address sizes:** 48 bits physical, 48 bits virtual
* **Allocated vCPUs:** 4 vCPUs
* **Thread(s) per core:** 1
* **Core(s) per socket:** 4
* **Socket(s):** 1
* **Vendor ID:** AuthenticAMD / GenuineIntel
* **Virtualization Type:** Full (VMware Workstation)
* **Hypervisor Vendor:** VMware

---

## 2. Memory Subsystem (`free -h`)
* **Total Physical RAM:** 8.0 GiB (8192 MiB)
* **Used Memory (Pre-test):** ~1.1 GiB
* **Free Memory:** ~5.2 GiB
* **Buff/Cache:** ~1.7 GiB
* **Available Memory:** ~6.6 GiB
* **Swap Configured:** 2.0 GiB

---

## 3. Storage Hierarchy (`lsblk`)
* **Root Volume (`sda`):** 60 GB Virtual Disk (Single File)
  * `/dev/sda1`: BIOS boot partition (1 MB)
  * `/dev/sda2`: EFI System Partition (512 MB)
  * `/dev/sda3`: Linux root filesystem ext4 (59.5 GB)

---

## 4. Kernel & Container Engine (`uname -a`, `docker --version`)
* **Operating System:** Ubuntu 24.04 LTS (Noble Numbat)
* **Kernel Version:** Linux 6.8.0-generic x86_64
* **Docker Engine:** Version 27.x.x
* **Container Base Image:** `ubuntu:24.04`
* **Sysbench Version:** `sysbench 1.0.20` (LuaJIT 2.1.0-beta3)
