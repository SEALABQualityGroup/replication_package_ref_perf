#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# Table RQ_1

ref_info = pd.read_csv('../data/ref_info.csv')

rows = []
for p in set(ref_info.project):
    ref_info_ = ref_info[ref_info.project == p]
    commits = ref_info_.commit
    ref_no = ref_info_.ref_no.sum()
    ref_perf_no = ref_info_.ref_per_no.sum()
    mean_methods_no_ = int(round((ref_info_.perf_methods + ref_info_.noperf_methods).mean()))
    mean_perf_methods_no_ = int(round(ref_info_.perf_methods.mean()))
    row = [p, len(commits),
           ref_no,mean_methods_no_ , mean_perf_methods_no_]
    rows.append(row)


table_rq1 = pd.DataFrame(rows, columns=['project', 'Analyzed Commits', 'Refactorings',
                                        'Methods (mean)', 'Performance-relevant Methods (mean)'])


table_rq1.iloc[table_rq1.project.str.lower().argsort()].to_csv('../tables/rq1.csv', index=False)
