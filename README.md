# Welfare Bounds for Linear-Quadratic Network Games

This repository contains replication materials for the paper **"[Welfare bounds for linear-quadratic network games](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5706124)"**.  
The purpose of this repository is to provide code and data to reproduce the results presented in the **Table 1** of the paper.

---

## 🧩 Environment

Below is the output of the environment check script:

```
Package versions:
Python:     3.13.2 | packaged by conda-forge | (main, Feb 17 2025, 14:02:48) [Clang 18.1.8 ]
NumPy:      2.1.3
Pandas:     2.2.3
Matplotlib:  3.10.1
NetworkX:   3.4.2
Graph-tool:  2.92 (commit , )
Standard libraries (time, json, pickle, datetime, typing): built-in modules
```

To install `graph-tool` via conda-forge, run:
```bash
conda create --name gt -c conda-forge graph-tool
conda activate gt
```
For more details, visit the [official installation guide](https://graph-tool.skewed.de/installation.html).

## 📊 Notebook Dependency Diagram

To reproduce **Table 1**, the main outputs are `out/welfare_bounds.csv` and `out/welfare_bounds_CI.csv`.  
The following diagram summarizes the dependencies among the notebooks and the intermediate data files used in the analysis.

```mermaid
flowchart TD
  node_1["empirical_data.ipynb"]
  node_2[("data/graph_adj_csr.pkl")]
  subgraph Null models
  node_3["chunglu_model_spectra.ipynb"]
  node_4[("data/FB_spectra.npz<br>data/FB1_spectra.npz<br>data/Jazz_spectra.npz<br>data/Karate_spectra.npz<br>data/NetSci_spectra.npz<br>data/Student_spectra.npz")]
  end
  node_5["welfare_bounds_emp_ER.ipynb"]
  node_6[["out/network_stats.csv"]]
  node_7[["out/welfare_bounds.csv"]]
  node_8["welfare_bounds_stat_test.ipynb"]
  node_9[["out/welfare_bounds_CI.csv"]]
  node_3 --"Generate 10,000 expected degree<br>graphs to compute spectra"--> node_4
  node_2 -.-> node_5
  node_1 --"Compute basic statistics of<br>the largest connected component"--> node_6
  node_5 --"Compute empirical<br>welfare bounds"--> node_7
  node_6 -.-> node_5
  node_7 -.-> node_8
  node_4 -.-> node_8
  node_8 --"Hypothesis tests"--> node_9
  node_1 --"Extract the largest<br>connected components"--> node_2
  node_2 -.- node_3
```
