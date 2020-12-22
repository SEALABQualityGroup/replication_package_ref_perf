#!/usr/bin/env python
# coding: utf-8

from functools import reduce
from scipy.stats import variation


class Filter:
    def __init__(self, df_, refactorings):
        self.df = df_
        self.refactorings = refactorings

    def _wforkcov_lt(self, row, threshold):
        forks = [f for f in eval(row['perf_before'])]
        forks += [f for f in eval(row['perf_after'])]
        return reduce(lambda bool_, f: bool_ and variation(f) < threshold, forks, True)

    def _overallcov_lt(self, row, threshold):
        iterations_before = [it for f in eval(row['perf_before']) for it in f]
        iterations_after = [it for f in eval(row['perf_after']) for it in f]
        return variation(iterations_before) < threshold and variation(iterations_after) < threshold

    def _singlereftype(self, row):
        res = False
        for ref in self.refactorings:
            if res == False:
                res = row[ref] > 0
            elif res == True and row[ref] > 0:
                return False
        return res

    def cov(self, ub=0.05, withinfork=False):
        fun = self._overallcov_lt if not withinfork else self._wforkcov_lt
        return self.df.apply(lambda r: fun(r, ub), axis=1)

    def singlereftype(self):
        return self.df.apply(self._singlereftype, axis=1)
