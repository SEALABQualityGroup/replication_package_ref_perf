#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils import Filter
import warnings

warnings.filterwarnings("ignore")
import warnings

warnings.filterwarnings("ignore")
# ## Impact of commits performance
file_path = '../data/dataset_round1.csv'

df = pd.read_csv(file_path)
refactorings = df.columns[5:-5]

# Consider only datapoints with a single refactoring type
f = Filter(df, refactorings)
df = df[f.singlereftype()]


# Include addition dataset (second round data collection)
df_singleref = pd.read_csv('../data/dataset_round2.csv')
df = pd.concat([df_singleref, df])
refactorings = df.columns[5:-5]

## performance relative change threshold
change_threshold = 0.01 / (10 ** 20)


def which_refactoring(row):
    num_ref = max(row[r] for r in refactorings)
    assert (num_ref > 0)
    assert (sum(row[r] for r in refactorings) == num_ref)

    for r in refactorings:
        if row[r] == num_ref:
            return r


df[refactorings] = df[refactorings].fillna(0)
df['refactoring'] = df.apply(which_refactoring, axis=1)
df['ratio_mean'] = (df.ratio_ci.map(lambda ci: eval(ci))
                    .map(lambda ci: (ci[0] + ci[1]) / 2 - 1))
df['effect'] = df.ratio_effsize.map(lambda x: 'regression' if x >= change_threshold
else 'improvement' if x <= -change_threshold else 'unchanged')

threshold = 50

# create df_enough : refactorings with enough data points
refactorings_enough = {r for r in refactorings if df[df[r] > 0].shape[0] >= threshold}
df_enough = df[df.refactoring.map(lambda r: r in refactorings_enough)]
df_enough['abs_ratio_mean'] = df_enough.ratio_mean.map(abs)

## create visualization dataframe bar chart
rows = []
for ref in refactorings_enough:
    df_ = df[df[ref] > 0]
    form_ref = ref.replace(' ', '\n')
    regr = df_[df_['ratio_effsize'] >= change_threshold].shape[0]
    impr = df_[df_['ratio_effsize'] <= -change_threshold].shape[0]
    unchanged = df_.shape[0] - regr - impr
    rows.append([form_ref, 'Regression', (regr / df_.shape[0]) * 100])
    rows.append([form_ref, 'Improvement', (impr / df_.shape[0]) * 100])

vizdf = pd.DataFrame(rows, columns=['refactoring', 'effect', 'value'])

sns.set_style('whitegrid')
colors = ["gray", "white", "whitesmoke"]
palette = sns.color_palette(colors)
fontsize = 14
plt.figure(figsize=(9, 5))

ax = sns.barplot(y='value', x='refactoring', hue='effect', data=vizdf, order=sorted(set(vizdf.refactoring)),
                 palette={'Regression': 'grey', 'Improvement': 'whitesmoke', 'Unchanged': 'silver'}, edgecolor='k',
                 linewidth=0.5)

ax.legend().set_title('')
plt.setp(ax.get_legend().get_texts(), fontsize=fontsize)
plt.xlabel('')
plt.ylabel('% Benchmarks', fontsize=fontsize)

plt.tick_params(
    axis='both',  # changes apply to the x-axis
    which='both',  # both major and minor ticks are affected
    labelsize=fontsize)  # labels along the bottom edge are of

plt.tight_layout()
plt.savefig('../figures/rq3_reftypes_impact.pdf')

reftypes_regr = {r.replace('\n', ' ') for r in
                 set(vizdf[(vizdf.effect == 'Regression') & (vizdf.value >= 5)].refactoring)}
reftypes_impr = {r.replace('\n', ' ') for r in
                 set(vizdf[(vizdf.effect == 'Improvement') & (vizdf.value >= 5)].refactoring)}

regr_query = df_enough.refactoring.map(lambda r: r in reftypes_regr) & (df_enough.effect == 'regression')
impr_query = df_enough.refactoring.map(lambda r: r in reftypes_impr) & (df_enough.effect == 'improvement')

vizdf_regr = df_enough[regr_query]
vizdf_impr = df_enough[impr_query]


def boxplot_intensity(vizdf_, filename, width):
    vizdf_['refactoring_label'] = vizdf_.refactoring.map(lambda r: r.replace(' ', '\n'))
    plt.figure(figsize=(10, 5))

    ax = sns.boxplot(x='refactoring_label', y='abs_ratio_mean', hue='effect', data=vizdf_, width=width,
                     order=sorted(set(vizdf_.refactoring_label)),
                     palette={'regression': 'gray', 'improvement': 'whitesmoke'},
                     showmeans=True, meanprops={"marker": "D", "markerfacecolor": "white", "markeredgecolor": "black"}
                     )

    ax.legend_.remove()

    for i, ticklabel in enumerate(ax.xaxis.get_ticklabels()):
        r = ticklabel.get_text()
        outliers = len([x for x in vizdf_[vizdf_.refactoring_label == r].abs_ratio_mean if x > 0.5])
        if outliers > 0:
            plt.text(i, 0.47, "{} >".format(outliers), rotation=90, fontsize=fontsize - 1)

    plt.ylim(0, 0.5)
    plt.tick_params(
        axis='both',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        labelsize=fontsize)  # labels along the bottom edge are of

    plt.ylabel('Relative performance change', fontsize=fontsize)
    plt.xlabel('')
    plt.savefig(filename)


boxplot_intensity(vizdf_regr, '../figures/rq3_reftypes_regr_perfchange.pdf', width=0.27)
boxplot_intensity(vizdf_impr, '../figures/rq3_reftypes_impr_perfchange.pdf', width=0.4)
