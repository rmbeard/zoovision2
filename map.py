# Written by Rachel Beard: last updated 1/6/20
# map.py contains several methods to assist in the rendering and saving of images to display in the zoovision webpage
# from lisa_test import moran_gen, moran_inverse_test
import matplotlib.pyplot as plt
from matplotlib import colors
import geopandas as gpd
import pandas as pd
import os, time, glob


# method to display a map for a specific year, week, and strain
def maps1(shapefile, selected_risk, selected_strain, selected_season, selected_week):
    df = pd.read_csv('C:\zoovision\data\weeklydata1_test1.csv')
    rg1 = gpd.read_file(shapefile)
    target = df['ILI POSITIVE']
    minima = min(target)
    maxima = max(target)
    print(maxima)
    # add the colorbar to the figure
    norm = colors.Normalize(vmin=minima, vmax=maxima)
    sm = plt.cm.ScalarMappable(cmap='OrRd', norm=norm)
    # sm = plt.cm.ScalarMappable(cmap='OrRd', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    # empty array for the data range
    sm._A = []
    df1 = df['SEASON'] == selected_season
    df = df[df1]
    df1 = df['WEEK'] == selected_week
    df = df[df1]
    df = df[['SEASON', 'H3N2', 'H1N1', 'ILI POSITIVE', 'STATE_NAME', 'WEEK', 'PERCENT POSITIVE', '%UNWEIGHTED ILI']]
    rg1 = rg1.merge(df, on='STATE_NAME')
    cs = rg1.centroid
    fig, ax = plt.subplots(1, figsize=(13, 8))
    title = selected_season + " " + selected_risk + " " + 'WEEK' + " " + str(selected_week)
    ax.set_title(title, y=1.08, fontsize=20)
    ax.set_axis_off()
    rg1.plot(column=selected_risk, norm=norm, cmap='OrRd', linewidth=0.3, ax=ax,
                           edgecolor='white', legend=False)
    cs[rg1[selected_strain] == 1].plot(ax=ax, markersize=30, color="blue", label="Pos Avian cases")
    cs[rg1[selected_strain] == 2].plot(ax=ax, markersize=30, color="black", label="Pos Swine cases")
    cs[rg1[selected_strain] == 3].plot(ax=ax, markersize=30, color="orange", label="Pos Avian and Swine cases")
    cs[rg1[selected_strain] == 4].plot(ax=ax, markersize=30, color="yellow", label="Pos Human cases")
    cs[rg1[selected_strain] == 5].plot(ax=ax, markersize=30, color="green", label="Pos Human and Swine cases")
    cs[rg1[selected_strain] == 6].plot(ax=ax, markersize=30, color="red", label="Pos Human and Avian cases")
    plt.legend(title=selected_strain + " Confirmed strain typing", loc='lower left', prop={'size': 14})
    # vmin, vmax = 0, 0
    # for i in df[selected_risk]:
    #     if i >= vmax:
    #        vmax = i

    cbar = fig.colorbar(sm)
    #plt.colorbar(label='ILI positive rate')
    # plt.clim(0, 5)
    if not os.path.isdir('static'):
        os.mkdir('static')
    else:
        # Remove old plot files

        for filename in glob.glob(os.path.join('static', '*.png')):
            os.remove(filename)
    plotfile = os.path.join('static', str(time.time()) + '.png')
    plt.savefig(plotfile)
    # global tempMap
    # tempMap = plotfile
    plt.close()
    return plotfile


def maps2(shapefile, selected_strain, selected_risk, selected_season, selected_week):
    df = pd.read_csv('C:\zoovision\data\weeklydata1_test1.csv')
    rg1 = gpd.read_file(shapefile)
    df1 = df['SEASON'] == selected_season
    df = df[df1]
    df1 = df['WEEK'] == selected_week
    df = df[df1]
    df = df[['SEASON', 'H3N2', 'H1N1', 'STATE_NAME', 'WEEK', 'ILI POSITIVE', 'PERCENT POSITIVE', '%UNWEIGHTED ILI']]
    rg1 = rg1.merge(df, on='STATE_NAME')
    cs = rg1.centroid
    fig, ax = plt.subplots(1, figsize=(13, 8))
    title = selected_season + " " + selected_risk + " " + 'WEEK' + " " + str(selected_week)
    ax.set_title(title, y=1.08, fontsize=20)
    ax.set_axis_off()
    rg1.plot(column=selected_risk, categorical=True, k=10, cmap='OrRd', linewidth=0.3, ax=ax,
                           edgecolor='white', legend=False)
    cs[rg1[selected_strain] == 1].plot(ax=ax, markersize=20, color="blue", label="Positive Avian cases")
    cs[rg1[selected_strain] == 2].plot(ax=ax, markersize=20, color="black", label="Positive Swine cases")
    cs[rg1[selected_strain] == 3].plot(ax=ax, markersize=20, color="orange", label="Positive Avian and Swine cases")
    cs[rg1[selected_strain] == 4].plot(ax=ax, markersize=20, color="yellow", label="Positive Human cases")
    cs[rg1[selected_strain] == 5].plot(ax=ax, markersize=20, color="green", label="Positive Human and Swine cases")
    cs[rg1[selected_strain] == 6].plot(ax=ax, markersize=20, color="red", label="Positive Human and Avian cases")
    plt.legend(title=selected_strain + " Confirmed strain typing", loc='lower left', prop={'size': 16})
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
    plt.close()
    return plotfile1


def precalc_moran(shapefile, selected_season, selected_val, selected_weight):
    df = pd.read_csv('C:\zoovision\data\cluster_results.csv')
    # df = pd.read_csv('C:\zoovision\data\cluster_results_seg2.csv')
    # df = pd.read_csv('C:\zoovision\data\weeklydata1_test1.csv')
    # read in shapefile
    rg1 = gpd.read_file(shapefile)
    df1 = df['SEASON'] == selected_season
    df = df[df1]
    df1 = df['WEEK'] == selected_val
    df = df[df1]
    rg1 = rg1.merge(df, on='STATE_NAME')
    # 1=HH 2=LH 3=LL 4= HL
    cluster_labels = ['No clustering', 'High-High', 'Low-High', 'Low-Low', 'High-Low']
    colors5 = {0: 'lightgrey',
               1: '#d7191c',
               2: '#abd9e9',
               3: '#2c7bb6',
               4: '#fdae61'}
    colorlist = [colors5[i] for i in rg1['sig_clust']]  # for Bokeh
    colors5 = (['#d7191c', '#fdae61', '#abd9e9', '#2c7bb6', 'lightgrey'])
    # spot_labels = ['0 ns', '1 hot spot', '2 doughnut', '3 cold spot', '4 diamond']
    selected_col = "sig_clust"
    if selected_weight == "Distance":
        labels = [cluster_labels[i] for i in rg1['sig_clust']]
    else:
        labels = [cluster_labels[i] for i in rg1['sig_clust']]
    fig, ax = plt.subplots(1, figsize=(13, 8))
    title = "Local Indicators of Spatial Association " + 'WEEK' + " " + str(selected_val)
    ax.set_title(title, y=1.08, fontsize=20)
    ax.set_axis_off()
    hmap = colors.ListedColormap(['#d7191c', '#fdae61', '#abd9e9', '#2c7bb6', 'lightgrey'])
    rg1.assign(cl=labels).plot(column='cl', categorical=True, k=2, cmap=hmap, linewidth=0.3, ax=ax,
                               edgecolor='white', legend=True)
    plt.legend(title='Cluster types', loc='lower left', prop={'size': 15})
    # if not os.path.isdir('static'):
    #     os.mkdir('static')
    # else:
    #     # Remove old plot files
    #     for filename in glob.glob(os.path.join('static', '*.png')):
    #         os.remove(filename)
    plotfile = os.path.join('static', str(time.time()) + '.png')
    plt.savefig(plotfile)
    plt.close()
    return plotfile


# method to display seasonal ili  rate for individual states
def sum_chart1(selected_week, selected_season, selected_state):
    df = pd.read_csv('C:\zoovision\data\weeklydata1_test1.csv')
    df.set_index(df['WEEKEND'], inplace=True)
    df['WEEKEND'] = pd.to_datetime(df['WEEKEND'], format='%m/%d/%Y')
    df = df[["WEEKEND", '%UNWEIGHTED ILI', "STATE_NAME", "SEASON", "WEEK"]]
    df1 = df['SEASON'] == selected_season
    df = df[df1]
    df1 = df['STATE_NAME'] == selected_state
    df = df[df1]
    store_week = selected_week
    if selected_week < 40:
        selected_week = selected_week+12
    else:
        selected_week = selected_week-40
    ILI = df[['%UNWEIGHTED ILI']]
    fig, ax = plt.subplots(1, figsize=(12, 8))
    plt.axvline(x=selected_week, color='r', linestyle='-', lw=7)
    plt.title('Seasonal Influenza Like illness rate by state', fontsize=20)
    ILI.plot(color='black', linewidth=4, ax=ax, fontsize=10)# display week
    plt.xlabel(selected_state + " " + 'week ' + str(store_week) + ":  " + str(df.index[selected_week]), fontsize=15)
    plt.xlim(0, 52)
    plt.ylabel("%UNWEIGHTED ILI", fontsize=18)
    plotfile = os.path.join('static', str(time.time()) + '.png')
    plt.savefig(plotfile)
    plt.close()
    return plotfile


if __name__ == '__main__':
    print(mapper(files, title))
    print(mapper2(files, title))
