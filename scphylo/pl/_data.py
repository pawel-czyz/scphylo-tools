import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.cluster import hierarchy
from scipy.spatial import distance

import scphylo as scp


def _colors(alist):
    return mcolors.LinearSegmentedColormap.from_list("", alist)


def heatmap(
    adata,
    color_attrs=None,
    layer="X",
    figsize=(12, 7),
    vmin=0,
    vmax=2,
    rvb=None,
    sorting_by_chroms=True,
):
    """Plot HeatMap.

    For flips: rvb=["#FFFFFF", "#D92347", "#A9D0F5"]
    For CNV: rvb="RdBu_r", vmin=-0.5, vmax=0.5

    Parameters
    ----------
    adata : [type]
        [description]
    color_attrs : [type], optional
        [description], by default None
    layer : str, optional
        [description], by default "X"
    figsize : tuple, optional
        [description], by default (12, 7)
    vmin : [type], optional
        [description], by default None
    vmax : [type], optional
        [description], by default None
    rvb : [type], optional
        [description], by default None
    """
    if color_attrs is not None:
        row_colors = []
        if isinstance(color_attrs, list):
            for attr in color_attrs:
                row_colors.append(adata.obs[attr])
        else:
            row_colors.append(adata.obs[color_attrs])
    else:
        row_colors = None

    if layer == "X":
        rvb = _colors(["#FFFFFF", "#000000", "#bfbfbf"])
        if sorting_by_chroms:
            adatac = adata[:, adata.var.sort_values(["CHROM", "POS"]).index].copy()
        else:
            adatac = adata.copy()
        df = adatac.to_df().copy()
        distance_array = scp.ul.hclustering(df, return_dist=True)
        df[df == 3] = 2
        df.index.name = "cells"
        df.columns.name = "mutations"
        row_linkage = hierarchy.linkage(
            distance.pdist(distance_array), method="average"
        )
        if sorting_by_chroms:
            chromosoms = {}
            for i in list(range(1, 23, 2)) + ["Y"]:
                chromosoms[f"chr{i}"] = "#969696"
            for i in list(range(2, 23, 2)) + ["X"]:
                chromosoms[f"chr{i}"] = "#252525"
            adatac.var["chrom_color"] = adata.var["CHROM"].map(chromosoms)
            scp.logg.info(adatac.var.CHROM.value_counts().sort_index().to_frame())
            adatac.var["chrom_color"].name = ""
            column_colors = adatac.var["chrom_color"]
        else:
            column_colors = None
    else:
        df = adata.obsm[layer].copy()
        if isinstance(rvb, list):
            rvb = _colors(rvb)
        column_colors = None

    sns.clustermap(
        df,
        vmin=vmin,
        vmax=vmax,
        metric="euclidean",
        cmap=rvb,
        row_cluster=True,
        col_cluster=False,
        row_colors=row_colors,
        col_colors=column_colors,
        cbar_pos=None,
        figsize=figsize,
        xticklabels=False,
        yticklabels=False,
        colors_ratio=(0.02, 0.02),
        dendrogram_ratio=0,
        row_linkage=row_linkage,
    )
    plt.xlabel("")
    plt.ylabel("")
    # plt.savefig(filepath, bbox_inches="tight", pad_inches=0)


def plot_dist(adata, attr):
    x = adata.obsp[attr][np.triu_indices(adata.shape[0], 1)]
    plt.hist(x, bins=50)
