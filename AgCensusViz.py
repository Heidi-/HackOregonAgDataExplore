""" Module to visualize AgCensus data. """

import matplotlib.pyplot as plt
import numpy as np

def histogramfarmsizes(fsdataframe, acreagecat):
    """ Create a histogram for each county showing farmsize categories through
        the years.
        fsdataframe = farmsize dataframe with columns: county_name, year, acres
        acreagecat = dataframe of categoreis with columns: begin, end, label
    """
    # define bin edeges
    bins = list(acreagecat.begin) + list(acreagecat.end[-1:])

    # find and order years
    years = fsdataframe.year.unique()
    years.sort()

    # define bar properties
    width = 0.2
    barx = [np.arange(len(bins)-1)]
    for y in years[1:]:
        barx.append(barx[-1]+width)
    colors = ('k', 'r', 'b', 'c')

    # create a histogram for each county
    for cn in fsdataframe.county_name.unique():
        fig = plt.figure()
        g = fig.add_subplot(111)
        countymask = fsdataframe.county_name == cn
        for i, (y, c) in enumerate(zip(years, colors)):
            yearmask = fsdataframe.year == y
            data = fsdataframe.acres[yearmask & countymask]
            print(barx[i])
            if not data.empty:
                yhist = np.histogram(data, bins)
                g.bar(barx[i], yhist[0], width, color=c, label=y)
        g.legend(fontsize=10, loc="upper center")
        g.set_xlabel("Acreage", fontsize='large', labelpad=15)
        g.set_ylabel("Farm Count", fontsize='large', labelpad=15)
        g.set_xticks(barx[0])
        g.set_xticklabels(acreagecat.label, rotation=30)
        g.set_title(cn, fontsize="xx-large")
        fig.subplots_adjust(bottom=0.2)
        filename = cn + ".png"
        fig.savefig(filename)
        fig.clf()
    return
