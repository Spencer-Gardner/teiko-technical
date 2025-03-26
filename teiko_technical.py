import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
from statannotations.Annotator import Annotator


## 1...

## read cell count data
cell_count_df = pd.read_csv('./data/cell-count.csv')

## store cell populations
immune_cell_populations = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']

## copy original data
new_cell_count_df = cell_count_df.copy()

## assign new column total_count; pivot longer; assign new column percentage
new_cell_count_df['total_count'] = new_cell_count_df[immune_cell_populations].sum(axis=1)
new_cell_count_df = new_cell_count_df.melt(id_vars=['sample', 'total_count'], value_vars=immune_cell_populations,
                                   var_name='population', value_name='count')
new_cell_count_df['percentage'] = (new_cell_count_df['count'] / new_cell_count_df['total_count']) * 100

## print df
# print(new_cell_count_df)

## write new data to file
new_cell_count_df.to_csv('./data/new_cell_count.csv', index=False)


## 2...

## merge cell counts; assign new columns
merged_cell_count_df = pd.merge(cell_count_df, new_cell_count_df, on='sample')
merged_cell_count_df = merged_cell_count_df[merged_cell_count_df['treatment'] == 'tr1']
merged_cell_count_df = merged_cell_count_df[merged_cell_count_df['condition'] == 'melanoma']
merged_cell_count_df = merged_cell_count_df[merged_cell_count_df['sample_type'] == 'PBMC']


## loop through cell populations
for pop in immune_cell_populations:

    ## subset cell population
    population_df = merged_cell_count_df[merged_cell_count_df['population'] == pop]

    ## generate boxplot
    ax = sns.boxplot(population_df, x='response', y='percentage')
    plt.xlabel('Response (tr1)')
    plt.ylabel('Relative Frequency (%)')
    plt.title(f"Comparison of Responders/Non-Responders ({pop})")

    ## annotate with p-value
    pairs = [('y', 'n')]
    annotator = Annotator(ax=ax, pairs=pairs, data=population_df, x='response', y='percentage')
    annotator.configure(test='t-test_ind', text_format='simple', loc='inside')
    annotator.apply_and_annotate()

    ## adjust layout
    plt.tight_layout()

    ## output
    # plt.show()
    file_name = f"./figures/{pop}_boxplot.png"
    plt.savefig(file_name, dpi=300)

    ## close
    plt.clf()
