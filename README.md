# Performance Analysis: Type-1 (Proxmox VE) vs Type-2 (VMware Workstation) Hypervisors

This repository contains the lab procedure, benchmark configuration, and comparative performance analysis between a **bare-metal Type-1 hypervisor (Proxmox VE)** and a **hosted Type-2 hypervisor (VMware Workstation)** using **Sysbench**.

---

## 📌 Overview

The experiment evaluates virtualization overhead by running identical Ubuntu guest virtual machines across both hypervisors and measuring CPU computing performance under a prime number generation workload.

### Test Environment Specifications (Per VM)

* **Guest OS:** Ubuntu (64-bit)
* **vCPUs:** 2 vCPU (1 socket, 2 cores)
* **Memory:** 2 GB RAM (2048 MiB)
* **Virtual Disk:** 20 GB
* **Network:** Bridge (`vmbr0` on Proxmox) / NAT (VMware Workstation)

---

## 🚀 Benchmark Methodology

1. **System Resource Verification:**
```bash
hostnamectl
lscpu
free -h
df -h
top

```


2. **Sysbench Installation:**
```bash
sudo apt update
sudo apt install sysbench -y

```


3. **CPU Benchmark Command:**
```bash
sysbench cpu --cpu-max-prime=20000 run

```





```
