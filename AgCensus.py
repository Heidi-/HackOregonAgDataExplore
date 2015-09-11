""" Module to download and simplify AgCensus data via NASS quickstats API."""

import locale
import pandas

APILINK = 'http://quickstats.nass.usda.gov/api/api_GET/?key={key}&format=CSV'

def set_api(key):
    """ Set API link template with key """
    global APILINK
    APILINK = APILINK.format(key=key)
    return

def query(**args):
    """ Query API according with following filters, return dataframe.
        Filters must include the operator (e.g. "=CENSUS" or "__LIKE=LAND")
        source_desc = "CENSUS" or "SURVEY"
        sector_desc = "CROPS", "ANIMALS & PRODUCTS", "ECONOMICS",
                      "DEMOGRAPHICS", or "ENVIRONMENTAL"
        year = Census year, integer
        state_alpha = Two letter abbreviation
        agg_level_desc = Aggregation level: "STATE", "AG DISTRICT", "COUNTY",
                         "REGION", "ZIP CODE"
        freq_desc = Length of time covered: "ANNUAL", "SEASON", "MONTHLY",
                    "WEEKLY", "POINT IN TIME"
    """
    if "{key}" in APILINK:
        raise NameError("API key not set. Call set_api(key) before query.")
    link = APILINK
    for k, v in args.items():
        link += '&' + k + v
    print("API link is:")
    print(link)
    data = pandas.read_csv(link)
    return data

def dropcolumns(dataframe, list_columns):
    """ Drop list_columns from the dataframe df """
    for c in list_columns:
        dataframe = dataframe.drop(c, 1)
    return dataframe

def write_data(data, filename):
    """ Write dataframe data to filename as csv. """
    data.to_csv(filename, index=False)
    return

def get_farmsizes():
    """ Return farmsize for all years for each farm in Oregon"""
    # define query
    filters = {}
    filters["state_alpha"] = "=OR"
    filters["group_desc"] = "__LIKE=FARMS"
    filters["commodity_desc"] = "__LIKE=LAND"
    # query and isolate only desired columns
    fs = query(**filters)
    fs.rename(columns={"Value":"acres"}, inplace=True)
    fs = fs[["county_name", "year", "acres"]]
    # remove values with null county
    fs = fs[fs.county_name.notnull()]
    # remove non-numeric values in acres column and convert to numeric value
    fs = fs[fs.acres != ' (D)']
    locale.setlocale(locale.LC_NUMERIC, '')
    fs.acres = fs.acres.apply(locale.atoi)
    return fs

def get_areairrigated():
    """ Return query results for "area irrigated".
        This is still in exploratory phase.
    """
    # define query
    filters = {}
    filters["state_alpha"] = "=OR"
    filters["statisticcat_desc"] = "=AREA%20IRRIGATED"
    # query
    areairr = query(**filters)
    return areairr

def get_farmincome():
    """ Return query results for farm income.
        This is still in exploratory phase.
    """
    # define query
    filters = {}
    filters["state_alpha"] = "=OR"
    filters["commodity_desc"] = "=INCOME,%20NET%20CASH%20FARM"
    filters["unit_desc"] = "=$%20/%20OPERATION"
    # query
    areairr = query(**filters)
    return areairr
