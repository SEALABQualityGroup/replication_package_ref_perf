import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import fisher_exact
import matplotlib.patches as mpatches

df = pd.read_csv("../data/ref_info.csv")




max_commits_per_project = 50

g = df.groupby('project').sum()
g['count'] = df.groupby(['project']).count()['perf_methods']
g = g.reset_index()
g.project = g.apply(lambda row: row.project.lower() if row['count'] >= 50 else 'others', axis=1)
g = g.groupby('project').sum()
g = g.reindex(index=[i for i in g.index if i != 'others'] + ['others'])
g['noperf_density'] = g['ref_noperf_methods'] / g['noperf_methods']
g['perf_density'] = g['ref_perf_methods'] / g['perf_methods']

vizdf = g[(g['count'] > max_commits_per_project)][['noperf_density', 'perf_density']].reset_index().melt('project')


fontsize = 14

def plotfisher(g):
    ypos = 0
    for proj, row in g.iterrows():
        perf_critical = row['perf_methods']
        non_perf_critical = row['noperf_methods']
        refactored_perf_critical = row['ref_perf_methods']
        refactored_non_perf_critical = row['ref_noperf_methods']
        non_refactored_perf_critical = (perf_critical - refactored_perf_critical)
        non_refactored_non_perf_critical = (non_perf_critical - refactored_non_perf_critical)

        table = [[refactored_non_perf_critical, refactored_perf_critical],
                 [non_refactored_non_perf_critical, non_refactored_perf_critical]]

        oddsratio, pvalue = fisher_exact(table)
        p = '{:.4f}'.format(pvalue) if pvalue >= 0.0001 else '{:.3e}'.format(pvalue)
        or_ = '{:.4f}'.format(oddsratio)
        info = 'p-value={}\nodds ratio={}'.format(p, or_)
        xpos = max(row['noperf_density'], row['perf_density']) + 0.0005
        plt.text(xpos, ypos, info, fontsize=fontsize - 2, va='center', weight='bold' if pvalue < 0.05 else 'normal')
        ypos += 1


palette = {'perf_density': 'gray', 'noperf_density': 'whitesmoke'}
sns.set_style('whitegrid')
plt.figure(figsize=(10, 10))
sns.barplot(x='value', y='project', hue='variable', data=vizdf, hue_order=['perf_density', 'noperf_density'],
            palette=palette, edgecolor='k', linewidth=0.5)
plt.xlabel('Refactoring Density', fontsize=fontsize)
plt.ylabel('')

p1 = mpatches.Patch(facecolor=palette['perf_density'], label='Performance relevant methods', edgecolor='k',
                    linewidth=0.5)
p2 = mpatches.Patch(facecolor=palette['noperf_density'], label='Other methods', edgecolor='k', linewidth=0.5)

leg = plt.legend(handles=[p1, p2], edgecolor='k', fontsize=fontsize - 2, loc='lower right')

plt.tick_params(
    axis='both',  # changes apply to the x-axis
    which='both',  # both major and minor ticks are affected
    labelsize=fontsize)  # labels along the bottom edge are of

leg.get_frame().set_linewidth(0.5)
plotfisher(g)
plt.xlim(0, 0.03)
plt.tight_layout()

plt.savefig('../figures/rq1.pdf')
