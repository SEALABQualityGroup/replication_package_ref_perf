# How Software Refactoring Impacts Execution Time

Replication package of the work "How Software Refactoring Impacts Execution Time".

## Requirements
- Python >= 3.6

Use the following command to install dependencies

```
pip install --upgrade pip
pip install -r scripts/requirements.txt
```

## Content
#### Data
The `data` folder contains the two dataset collected from the two rounds of data collection (`dataset_round1.csv` and `dataset_round1.csv`, respectively).
Each row of the datasets represents a data point, and it contains:
- `project`: the name of the project
- `sha`: SHA of the commit
- `benchmark`: the signature of the benchmark 
- `params`: the parameters used by the benchmarks
- `unit`: the unit defined by developers to measure execution time
- `[ref_type]`: the number of refactoring operation of type `ref_type` performed in the code executed by the benchmark.
- `perf_before`: raw measurements of the benchmark before the commit `sha` is performed. Inner lists represents different JVM invocations, while each item represents the observed execution time in a given measurement iteration.
- `perf_after`: raw measurements of the benchmark after the commit `sha` is performed.
- `rpc_ci`: 95% confidence interval for the relative performance change.

