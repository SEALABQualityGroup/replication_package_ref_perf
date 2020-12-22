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
#### Datasets
The `data` folder contains the two datasets collected from the two rounds of data collection (`dataset_round1.csv` and `dataset_round2.csv`, respectively).
Each row of the datasets represents a data point, and it contains:
- `project`: the name of the project
- `sha`: the SHA of the commit
- `benchmark`: the signature of the benchmark 
- `params`: the parameters used by the benchmarks
- `unit`: the unit defined by developers to measure execution time
- `[ref_type]`: the number of refactoring operation of type `ref_type` performed in the code executed by the benchmark.
- `perf_before`: raw measurements of the benchmark before the commit `sha` is performed. Inner lists represents different JVM invocations, while each item represents the observed execution time in a given measurement iteration.
- `perf_after`: raw measurements of the benchmark after the commit `sha` is performed.
- `rpc_ci`: 95% confidence interval for the relative performance change.

#### Other data
The `data/repositories` folder contains the scripts used to gather Java projects with JMH benchmarks suites, and the collected projects (`repositories_stars_fork.txt`).

The `ref_info.csv` file contains, for each commit considered in the study:
- `commit`: the SHA of the commit
- `project`: the name of the project
- `perf_methods`: the number of performace relevant methods (covered by at least one benchmark)
- `noperf_methods`: the number of other methods in the project (not covered by any benchmark)
- `ref_perf_methods`: the number of performace relevant methods subject to refactoring
- `ref_noperf_methods	`: the number of other methods subject to refactoring
- `ref_no`: the number of refactoring operations performed in the commit


The folder `data/ref_bench` contains one folder per round of data collection.
Each file `[project].csv` in these folders contains the data used to identify benchmarks suitable to evaluate the performace impact of refactoring operations, and it contains:
- `(Benchmark_method, commit)`: the benchmark signature and the SHA of the commit
- `[ref_type]`: the number of refactoring operations of type `ref_type` performed in the code executed by the benchmark.

#### Scripts
The `scripts` folder contains the Python scripts used to generate the figures and tables of the paper.






