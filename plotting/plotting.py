# Data I/O
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None

# Bokeh
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.layouts import layout, widgetbox
from bokeh.models.widgets import Select
from bokeh.io import output_notebook
from bokeh.palettes import d3, viridis
import bokeh.models as bmo


# matplotlib-venn
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3

# Seaborn
import seaborn as sns

np.random.seed(12)

# Convert xlsx to csv for performance, only needed once per session.
def convert_xlsx(xlsx_path):
    data = pd.read_excel('data/download.xlsx')
    data.to_csv('data/download.csv')

data = pd.read_csv('data/download.csv', low_memory=False)


def clicks_v_impressions(data, click_lower_bound=5, output=False, semantic_term = 'PriceResearch'):
    """
    :param data: The dataframe of download.csv
    :param click_lower_bound: Records with clicks fewer than this number are excluded from the plot (for performance).
    :param output: If false, assumes the function is running from a Jupyter notebook, if a path as a string, will write
    the plot as a .html file to the supplie path.
    """

    # Generate random portfolio values
    # TODO remove this after the classification package is operable
    test_portfolio_vals = np.array(['paid', 'paid | organic', 'none', 'organic'])
    data['Portfolio Classification'] = test_portfolio_vals[np.random.randint(0, len(test_portfolio_vals), len(data))]

    palette = d3['Category10'][len(data['Portfolio Classification'].unique())]

    # First, plot impressions vs. clicks and the tooltip will be the search query itself
    data = data[data['Clicks'] > click_lower_bound]

    bool_col = data['Semantic Classification'].str.contains(semantic_term)
    booleanDictionary = {True: 'Contains {}'.format(semantic_term), False: 'Does not Contain {}'.format(semantic_term)}
    data['bool'] = bool_col.map(booleanDictionary)

    color_map = bmo.CategoricalColorMapper(factors=data['bool'].unique(), palette = palette)
    source = ColumnDataSource(data=data)

    # Now we will generate the binary category

    TOOLTIPS = [('Search Term', '@{Search term}'),
                ('Cost', '@Cost')]

    if output == False:
        output_notebook()
    elif type(output) == str:
        output_file(output)

    p = figure(plot_width=800, plot_height=400, tooltips=TOOLTIPS)
    p.circle(x='Clicks', y='Impressions', source=source, color={'field': 'bool', 'transform': color_map}, legend='bool')
    p.xaxis.axis_label = 'Paid Clicks'
    p.yaxis.axis_label = 'Paid Impressions'

    # Plotting parameters
    show(p)


def venn_diagram2(data, semantic_terms, click_lower_bound=5):
    """
    Plots a venn diagram for shared semantic terms.

    :param data: The dataframe of download.csv
    :param semantic_terms: A list of 2 semantic terms to match.
    :param click_lower_bound: Records with clicks fewer than this number are excluded from the plot (for performance).
    """
    data = data[data['Clicks'] > click_lower_bound]

    #data['Clicks'] = data['Clicks'].astype(np.int64)
    # Create a new row for each click, in preparation for the set methodology of venn2
    #data = data.reindex(data.index.repeat(data['Clicks']))

    term_sets = [set(data[data['Semantic Classification'].str.contains(term)]['Semantic Classification'].values) for term in semantic_terms]
    venn2([term_sets[0], term_sets[1]], ('Contains {}'.format(semantic_terms[0]), 'Contains {}'.format(semantic_terms[1])))
    plt.title('Semantic Classification Overlap')
    plt.show()

def venn_diagram3(data, semantic_terms, click_lower_bound=5):
    """
    Plots a venn diagram for shared semantic terms.

    :param data: The dataframe of download.csv
    :param semantic_terms: A list of 2 semantic terms to match
    :param click_lower_bound: Records with clicks fewer than this number are excluded from the plot (for performance).
    """
    data = data[data['Clicks'] > click_lower_bound]
    term_sets = [set(data[data['Semantic Classification'].str.contains(term)]['Semantic Classification'].values) for term in semantic_terms]
    venn3([term_sets[0], term_sets[1], term_sets[2]], ('Contains {}'.format(semantic_terms[0]), 'Contains {}'.format(semantic_terms[1]), 'Contains {}'.format(semantic_terms[2])))
    plt.title('Semantic Classification Overlap')
    plt.show()

def volume_histogram(data, n_best = 20):
    """
    Plots a histogram of impressions grouped by semantic classifcation.

    :param data: The dataframe of download.csv
    :param n_best: The number of columns to include, ranked by # of impressions.
    :return:
    """
    grp = data.groupby('Semantic Classification')
    totals = grp.agg({'Impressions': np.sum})
    totals = totals.sort_values('Impressions', ascending=False)
    totals = totals.reset_index()
    totals = totals.iloc[0:n_best, :]

    source = ColumnDataSource(data=totals)
    TOOLTIPS = [('Semantic Classifcation', '@{Semantic Classification}')]

    p = figure(x_range = totals['Semantic Classification'], tooltips=TOOLTIPS)
    p.xaxis.visible = False
    p.xaxis.axis_label = 'Semantic Classification'
    p.yaxis.axis_label = 'Paid Impressions'
    p.vbar(x = 'Semantic Classification', top='Impressions', width=0.8, source=source)
    output_notebook()
    show(p)

def click_volume2(data, semantic_terms):
    grp = data.groupby('Semantic Classification')
    totals = grp.agg({'Clicks': np.sum})
    totals = totals.sort_values('Clicks', ascending=False)
    totals = totals.reset_index()

    # Exclusives
    exclusives = [totals[totals['Semantic Classification'].str.contains(term)] for term in semantic_terms]
    exclusives_sum = [np.sum(totals['Clicks']) for totals in exclusives]

    # Inclusive
    inclusives = totals[totals['Semantic Classification'].str.contains(semantic_terms[0]) & totals['Semantic Classification'].str.contains(semantic_terms[1])]

    plot_frame = pd.DataFrame({'Clicks': exclusives_sum, 'Contains': semantic_terms})
    plot_frame.loc[2] = [np.sum(inclusives['Clicks']), 'Both {} and {}'.format(*semantic_terms)]

    source = ColumnDataSource(data=plot_frame)
    p = figure(x_range = plot_frame['Contains'])
    p.vbar(x='Contains', top = 'Clicks', width = 0.5, source=source)
    output_notebook()
    show(p)

def search_raster(data):
    # Now we need all unique semantic classifications
    # TODO this should come from upstream, I hacked a solution here, it is a list of all possible Semantic Classifcations
    unique_class = data[~data['Semantic Classification'].str.contains('\+')]['Semantic Classification'].unique()

    # Subset to values that only have non-zero / non-nan conversion and click values
    data = data.dropna(subset=['Total conv. value', 'Clicks'])
    data = data[data['Clicks']!=0]
    data = data[data['Total conv. value']!=0]
    data['Value per Click'] = data['Total conv. value'] / data['Clicks']

    # Group by classification and start adding it up
    grp = data.groupby('Semantic Classification')
    sum_vpc = grp.agg({'Value per Click': np.sum})
    sum_vpc = sum_vpc.reset_index()
    n = len(unique_class)**2

    # TODO probably a bit slow, but it gets the job done
    container = pd.DataFrame(np.nan, index=np.arange(n), columns=['Term_i', 'Term_j', 'Value per Click'])
    i = 0
    for term_i in unique_class:
        for term_j in unique_class:
            inclusives = sum_vpc[sum_vpc['Semantic Classification'].str.contains(term_i) & sum_vpc['Semantic Classification'].str.contains(term_j)]
            aggregated_sum = np.sum(inclusives['Value per Click'])
            container.loc[i] = [term_i, term_j, aggregated_sum]
            i+=1

    # Plot parameters
    ## Color Mapper
    mapper = bmo.LogColorMapper(palette=viridis(256), low=container['Value per Click'].min(), high=container['Value per Click'].max())

    ## Plot Construction
    p = figure(x_range = unique_class, y_range = unique_class, tooltips=[('Total Value', '@{Value per Click}{int}'),
                                                                         ('Contains', '@Term_i, @Term_j')])
    p.rect(x='Term_j', y='Term_i', width=0.98, height=0.98, source=container,
           fill_color={'field': 'Value per Click', 'transform': mapper},
           line_color=None)
    p.xaxis.major_label_orientation = np.pi / 3
    output_notebook()
    show(p)
