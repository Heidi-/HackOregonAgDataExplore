""" Module to visualize AgCensus data. """

import matplotlib.pyplot as plt
import numpy as np
import pandas

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

def shannonentropy(pdist):
    """ Return Shannon Entropy of the probability pdist """
    return -sum(pdist * np.log2(pdist))

def countcrops(area):
    counties = area.county_name.unique()
    crops = {}
    for cn in counties:
        crops[cn] = len(area[area.county_name == cn].commodity_desc.unique())
    return crops
     
def cropdiversity(areadata):
    """ Return the Shannon Entropy for each county, as well as the total land
        area growing crops in each county.
        areadata - dataframe with columns county_name, commodity_desc, and acres

        Returns two dicts, Shannon Entropy and total crop area, both with
        county names for keys.
    """
    counties = areadata.county_name.unique()
    # Remove redundant categories - "TOTALS" and "HAY & HAYLAGE"
    areadata = areadata[areadata.commodity_desc.str.contains("TOTALS")==False]
    areadata = areadata[areadata.commodity_desc != "HAY & HAYLAGE"]
    diversity = {}
    #stdiversity = {}
    cnacres = {}
    for cn in counties:
        print(cn)
        crop = areadata[areadata.county_name == cn][["commodity_desc", "acres"]]
        croparea = crop.groupby(crop.commodity_desc).sum()
        diversity[cn] = shannonentropy(croparea.acres/sum(croparea.acres))
        #stdiversity[cn] = shannonentropy(croparea.acres/sum(areadata.acres))
        cnacres[cn] = sum(croparea.acres)
        print(diversity[cn])
    return(diversity, cnacres) 

def dictstodataframe(colnames, *ds):
    """ All dictiories passed should have the same keys, which will become
        the index of the dataframe. Column names are in a list colnames.
    """
    df = pandas.DataFrame.from_dict(ds[0], orient='index')
    df.columns = [colnames[0]]
    for d,n in zip(ds[1:], colnames[1:]):
        df[n] = df.index.map(d.get)
    return df

def plotdiversity(div):
    """ Create a barchart of diversity measures. 

        div is dataframe with columns Entropy, CropLand, CropCount
        Plot saved in file "Entropy.png"
    """
    left = np.arange(len(div))

    fig = plt.figure(figsize=(6.5, 9))
    nplots = 3
    gs = [fig.add_subplot(nplots, 1, i+1) for i in range(nplots)]
    colors = ['seagreen', 'lightsage']
        
    gs[0].bar(left, div.Entropy.values, color=colors)
    gs[1].bar(left, div.CropLand.values/100000, color=colors)
    gs[2].bar(left, div.CropCount.values, color=colors)
   
    gs[0].set_ylabel("Crop Diversity", fontsize='medium', labelpad=15)
    gs[1].set_ylabel("Crop Area\n(100,000 acres)",fontsize='medium',labelpad=15)
    gs[2].set_ylabel("Crop Count", fontsize='medium', labelpad=15)

    for g in gs:
        g.set_xlim(0,len(left)) 
        g.set_xticklabels([])

    gs[-1].set_xticks(left+0.5)
    gs[-1].set_xticklabels(div.index.values, rotation=90, fontsize='small')

    fig.subplots_adjust(bottom=0.2)
    filename = "Entropy.png"
    fig.savefig(filename)
    fig.clf()
    return
