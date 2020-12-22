#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Impact of commits performance

from matplotlib.patches import Patch

file_path = '../data/dataset_round1.csv'


df = pd.read_csv(file_path)
refactorings = df.columns[5:-5]
change_threshold = 0.01 / (10 ** 20)


def degradations(series):
    return len([x for x in series if x >= change_threshold])


def improvements(series):
    return len([x for x in series if x <= -change_threshold])


def nochange(series):
    return len([x for x in series if abs(x) < change_threshold])


g = df.groupby(['project', 'sha']).agg({'ratio_effsize': [degradations, improvements, nochange]})


def effect(row):
    deg, impr, nc = row['ratio_effsize']['degradations'], row['ratio_effsize']['improvements'], row['ratio_effsize'][
        'nochange']
    if deg == 0 and impr == 0:
        return 'nochange'
    elif deg > 0 and impr == 0:
        return 'degradation'
    elif deg == 0 and impr > 0:
        return 'improvements'
    else:
        return 'mixed'


sns.set_style('whitegrid')
g['effect'] = g.apply(effect, axis=1)
fontsize = 14

plt.figure(figsize=(10, 2.5))
sns.set_style('whitegrid')
colors = ["gray", "white", "silver", "whitesmoke"]
palette = {'Regression': 'gray', 'Improvement': 'white', 'Mixed': 'silver', 'Unchanged': 'whitesmoke'}

y = ['degradation', 'improvements', 'mixed', 'nochange']
ylabels = ['Regression', 'Improvement', 'Mixed', 'Unchanged']

x = [((g[g['effect'] == y_].shape[0]) / g.shape[0]) * 100
     for y_ in y]

sns.barplot(x=x, y=ylabels, palette=palette, edgecolor='k', linewidth=0.5);
plt.tick_params(
    axis='both',  # changes apply to the x-axis
    which='both',  # both major and minor ticks are affected
    labelsize=fontsize)  # labels along the bottom edge are of

plt.xlabel('% Commits', fontsize=fontsize)

plt.tight_layout()

plt.savefig('../figures/rq2_commit_impact.pdf')


plt.figure(figsize=(10, 2))

y = ['Regression', 'Improvement', 'Unchanged'
     ]
x = [df[df['ratio_effsize'] > change_threshold].shape[0], df[df['ratio_effsize'] < -change_threshold].shape[0]]
x.append(df.shape[0] - x[0] - x[1])

x = [(x_ / df.shape[0]) * 100 for x_ in x]
sns.barplot(x=x, y=y, palette=palette, edgecolor='k', linewidth=0.5)

plt.tick_params(
    axis='both',  # changes apply to the x-axis
    which='both',  # both major and minor ticks are affected
    labelsize=fontsize)  # labels along the bottom edge are of

plt.xlabel('% Benchmarks', fontsize=fontsize)
plt.tight_layout()
plt.savefig('../figures/rq2_benchmarks_impact.pdf')

regressions = pd.Series([(ci[0] + ci[1]) / 2 - 1 for ci in map(eval, df.ratio_ci) if ci[0] >= 1 + change_threshold])
improvements = pd.Series(
    [abs((ci[0] + ci[1]) / 2 - 1) for ci in map(eval, df.ratio_ci) if ci[1] <= 1 - change_threshold])

vizdf = pd.concat([pd.DataFrame([(x, 'improvement') for x in improvements], columns=['magnitude', 'effect']),
                   pd.DataFrame([(x, 'regression') for x in regressions], columns=['magnitude', 'effect'])])

palette = {'improvement': 'whitesmoke', 'regression': 'gray'}

plt.figure(figsize=(12.8, 4.8))
ax = sns.boxplot(y='effect', x='magnitude', data=vizdf, order=['regression', 'improvement'], width=0.3,
                 palette=palette, showmeans=True,
                 meanprops={"marker": "D", "markerfacecolor": "white", "markeredgecolor": "black"},
                 )

xlim = 0.395
plt.xlim(-0.01, xlim)

plt.ylabel('')
plt.xlabel('Relative performance change', fontsize=fontsize)
ax.set(yticklabels=[])

ax.text(xlim - 0.01, 0 + 0.04, '{} >'.format(len([x for x in regressions if x > xlim])), fontsize=fontsize - 1)
ax.text(xlim - 0.01, 1 + 0.04, '{} >'.format(len([x for x in improvements if x > xlim])), fontsize=fontsize - 1)

legend_elements = [Patch(facecolor=palette['regression'], edgecolor='gray', label='Regression'),
                   Patch(facecolor=palette['improvement'], edgecolor='gray', label='Improvement')]
plt.legend(handles=legend_elements, loc='center right', fontsize=fontsize)
plt.tick_params(
    axis='both',  # changes apply to the x-axis
    which='both',  # both major and minor ticks are affected
    labelsize=fontsize)  # labels along the bottom edge are of

plt.tight_layout()
plt.savefig('../figures/rq2_performance_change.pdf')
