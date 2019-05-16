# Created by Rachel Beard: last updated on 1/11/19
# Purpose: to take in a shapefile, perform spattial autcorrelation
# using pysal's functionality for Local Moran's I

# %pip install matplotlib inline
import matplotlib.pyplot as plt
import pysal as ps
from splot.esda import lisa_cluster, plot_moran, plot_local_autocorrelation, moran_scatterplot
from esda.moran import Moran_Local
import numpy as np
import pandas as pd
import geopandas as gpd


# required variables to implement local moran:
# w = weights file, df= file with spatial data,
# y = column to perform analysis on

# First method will compute an inverse distance band weighting scheme

def moran_inverse_test(file, selected_risk, selected_val):
    # Read in shapefile merged with csv
    df = file
    # print(df)
    y = df[selected_risk]
    # print(y)
    thresh = ps.min_threshold_dist_from_shapefile("C:\zoovision\data\Export_Output.shp")
    print(thresh)
    # thresh = 1.1
    # weight based on fixed distance,(0 if not in threshold)
    w = ps.weights.DistanceBand.from_shapefile("C:\zoovision\data\Export_Output.shp", threshold=thresh, binary=False)
    # print(w)
    # weight based on non fixed distance,(0 if not in threshold)
    # w = ps.weights.DistanceBand.from_shapefile("C:\zoovision\data\Region1.shp", binary=False)

    # transform r= standardize
    moran_loc = ps.Moran_Local(y, w, transformation="r", permutations=9999)
    print(moran_loc.p_sim)
    fig, ax = lisa_cluster(moran_loc, df, p=0.05, figsize=(20, 15))
    title = "Local Indicators of Spatial Association " + 'WEEK' + " " + str(selected_val)
    ax.set_title(title, fontsize=35)  # plot_moran(moran_loc, zstandard=True, figsize=(10, 4))


def moran_gen(file):
    # Read in shapefile
    df = file
    # df = gpd.read_file(file)
    # print(df.dtypes)
    y = df['ind_100t']
    # Calculate weight
    # First calculate minimum threshold distance to nearest neightbor
    thresh = ps.min_threshold_dist_from_shapefile("C:\zoovision\data\Region1.shp")
    # thresh = 1
    # print(thresh)
    # weight based on fixed distance, for binary(0 or 1 if within threshold)
    # arcgis_swm = ps.open('C:\zoovision\data\weightfiles\week1test.swm', 'r')
    # w = arcgis_swm.read()
    # arcgis_swm.close()
    # e = open('C:\zoovision\data\Region1_count.txt')
    # x = e.readlines()
    # print(x.head())
    # gwt = ps.open('C:\zoovision\weights.gwt', 'r')
    # w = gwt.read()
    # gwt.close()
    # w = ps.open('C:\zoovision\data\Region1_count.txt', 'r', 'Region1_count').read()
    testfile = ps.open('C:\zoovision\data\Region1_count.txt', 'r', 'arcgis_text')
    testfile = ps.open('C:\zoovision\data\Region1_count.txt', 'r', 'arcgis_text')
    w = testfile.read()
    testfile.close()
    # testfile = ps.open('C:\zoovision\data\weightfiles\Region1_genweights.swm', 'r')
    # w = testfile.read()
    testfile.close()

    w.n
    # f = tempfile.NamedTemporaryFile(suffix='.txt')
    # fname = f.name
    # f.close()
    # o = ps.open(fname, 'w', 'Region1_count')
    # o.write(w)
    # o.close()
    # wnew = ps.open(fname, 'r', 'Region1_count').read()
    # wnew.pct_nonzero == w.pct_nonzero
    # os.remove(fname)
    # arcgis_txt.close()
    # w = ps.queen_from_shapefile("C:\zoovision\data\Region1.shp")
    # w = ps.weights.DistanceBand.from_shapefile("C:\zoovision\data\Region1.shp",  threshold=thresh, binary=False)
    # print(tuple(w1))
    # f = ps.open(ps.examples.get_path("stl_hom.txt"))
    # y = np.array(f.by_col['HR8893'])
    # w = ps.open(ps.examples.get_path("stl.gal")).read()
    # np.random.seed(12345)
    # moran_loc = ps.Moran_Local(y, w)
    # print(tuple(w))
    # w2 = ps.lat2W(6, 4)
    # w = ps.w_union(w1, w2)
    # w = w1.multiply(w2)

    moran_loc = Moran_Local(y, w, transformation='r', permutations=999)

    # moran_loc = ps.Moran_Local(y, w, permutations=999)
    fig, ax = plt.subplots(figsize=(15, 10))

    fig, ax = lisa_cluster(moran_loc, df, p=0.05, figsize=(15, 10))

    ax.set_title("Local Indicators of Spatial Association ",
                 fontsize=35)  # plot_moran(moran_loc, zstandard=True, figsize=(10, 4))
    # moran_scatterplot(moran_loc, ax=ax2)
    # plot_local_autocorrelation(moran_loc, df, y, p=0.05, figsize=(18, 6))


if __name__ == '__main__':
    print(moran_inverse(file))
