# Written by Rachel Beard: last updated 5/16/19
# map.py contains several methods to assist in the rendering and saving of images to display in the zoovision webpage
from lisa_test import moran_gen, moran_inverse_test
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import numpy as np
import os, time, glob


def maps1(files, selected_risk, selected_season, selected_week):
    df = pd.read_csv('./data/weeklydata1_test.csv')
    # df = pd.read_csv('C:\zoovision\data\weeklydata1_test.csv')
    fp = files
    rg1 = gpd.read_file(fp)

    # df = df[['SEASON'] == '2015-16']
    df1 = df['SEASON'] == selected_season
    # print(df1)
    df = df[df1]
    # print(df)

    df1 = df['WEEK'] == selected_week
    # print(df1)
    df = df[df1]

    df = df[['SEASON', 'ILI POSITIVE', 'STATE_NAME', 'WEEK', 'PERCENT POSITIVE', '%UNWEIGHTED ILI']]
    # print(df)
    # rg1 = rg1.to_crs(epsg=2163)
    rg1 = rg1.merge(df, on='STATE_NAME')
    # print(rg1)
    # print(rg1.dtypes)
    fig, ax = plt.subplots(1, figsize=(13, 8))
    title = selected_season + " " + selected_risk + " " + 'WEEK' + " " + str(selected_week)
    ax.set_title(title, y=1.08, fontsize=20)
    ax.set_axis_off()
    rg1.plot(column=selected_risk, categorical=True, k=10, cmap='OrRd', linewidth=0.3, ax=ax,
                           edgecolor='black', legend=False)
    vmin, vmax = 0, 0
    for i in df[selected_risk]:
        if i >= vmax:
            vmax = i

    sm = plt.cm.ScalarMappable(cmap='OrRd', norm = plt.Normalize(vmin=vmin, vmax=vmax))
    # empty array for the data range
    sm._A = []
    # add the colorbar to the figure
    cbar = fig.colorbar(sm)
    if not os.path.isdir('static'):
        os.mkdir('static')
    else:
        # Remove old plot files
        for filename in glob.glob(os.path.join('static', '*.png')):
            os.remove(filename)
    # Use time of filename in order make a unique filename that the browser has not chached
    plotfile = os.path.join('static', str(time.time()) + '.png')
    plt.savefig(plotfile)
    #plt.close()
    plotfile1 = plotfile
    # plt.show()
    return plotfile1


def maps2(files, selected_risk, selected_season, selected_week):
    df = pd.read_csv('./data/weeklydata1_test.csv')
    # df = pd.read_csv('C:\zoovision\data\weeklydata1_test.csv')
    fp = files
    rg1 = gpd.read_file(fp)

    # df = df[['SEASON'] == '2015-16']
    df1 = df['SEASON'] == selected_season
    # print(df1)
    df = df[df1]
    # print(df)

    df1 = df['WEEK'] == selected_week
    # print(df1)
    df = df[df1]

    df = df[['SEASON', 'STATE_NAME', 'WEEK', 'ILI POSITIVE', 'PERCENT POSITIVE', '%UNWEIGHTED ILI']]
    # print(df)
    # rg1 = rg1.to_crs(epsg=2163)
    rg1 = rg1.merge(df, on='STATE_NAME')
    # print(rg1)
    # print(rg1.dtypes)
    fig, ax = plt.subplots(1, figsize=(13, 8))
    title = selected_season + " " + selected_risk + " " + 'WEEK' + " " + str(selected_week)
    ax.set_title(title, y=1.08, fontsize=20)
    ax.set_axis_off()
    rg1.plot(column=selected_risk, categorical=True, k=10, cmap='OrRd', linewidth=0.3, ax=ax,
                           edgecolor='black', legend=False)
    vmin, vmax = 0, 0
    for i in df[selected_risk]:
        if i >= vmax:
            vmax = i
    sm = plt.cm.ScalarMappable(cmap='OrRd', norm = plt.Normalize(vmin=vmin, vmax=vmax))
    # empty array for the data range
    sm._A = []
    cbar = fig.colorbar(sm)
    plotfile = os.path.join('static', str(time.time()) + '.png')
    plt.savefig(plotfile)
    plotfile1 = plotfile
    # plt.show()
    return plotfile1


def local_moran_test(files, selected_risk, selected_season, selected_val, selected_weight, selected_week):
    df = pd.read_csv('./data/weeklydata1_test.csv')
    # df = pd.read_csv('C:\zoovision\data\weeklydata1_test.csv')
    # shapefile
    fp = files
    rg1 = gpd.read_file(fp)
    print(rg1)
    # df = df[['SEASON'] == '2015-16']
    df1 = df['SEASON'] == selected_season
    # print(df1)
    df = df[df1]
    # print(df)
    df1 = df['WEEK'] == selected_val
    # print(df1)
    df = df[df1]
    df = df[['SEASON', "ILI POSITIVE", 'STATE_NAME', 'WEEK', 'PERCENT POSITIVE', '%UNWEIGHTED ILI']]

    print(df)
    rg1 = rg1.merge(df, on='STATE_NAME')
    # retrieve cluster classifications
    print(rg1)
    print(selected_weight)
    if selected_weight == 'Distance':
        moran_inverse_test(rg1, selected_risk, selected_val)
    else:
        moran_gen(rg1)
    if not os.path.isdir('static'):
        os.mkdir('static')
    else:
        # Remove old plot files
        for filename in glob.glob(os.path.join('static', '*.png')):
            os.remove(filename)
    # Use time since Jan 1, 1970 in filename in order make
    # a unique filename that the browser has not chached
    plotfile = os.path.join('static', str(time.time()) + '.png')
    plt.savefig(plotfile)
    return plotfile

fig, ax = plt.subplots(1, figsize=(15, 10))


def sum_chart():
    n = 3
    H1N1 = (16, 21, 23)
    H3N2 = (21, 11, 21)
    x = np.arange(n)
    width = 0.35
    fig, ax = plt.subplots(1, figsize=(7, 4))
    p1 = plt.bar(x, H3N2, width, color='black')
    p2 = plt.bar(x, H1N1, width, color='firebrick', bottom=H3N2)
    plt.ylabel('Percent')
    plt.title('Proportion of Circulating viral sequences by species', fontsize=10)
    plt.xticks(x, ('Human', 'Avian', 'Swine'))
    plt.yticks(np.arange(0, 60, 10))
    plt.legend((p2[0], p1[0]), ('H1N1', 'H3N2'))
    plotfile = os.path.join('static', str(time.time()) + '.png')
    plt.savefig(plotfile)
    #plt.close()
    return plotfile


if __name__ == '__main__':
    print(mapper(files, title))
    print(mapper2(files, title))
