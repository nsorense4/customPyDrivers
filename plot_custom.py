"""
 @file    phy5340_lab3_nicholassorensen.ipynb
 @author  Nicholas Sorensen
 @date    2022-02-09
"""
import time as time
import warnings
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def plot_custom(xsize, ysize, x_label, y_label, equal=True, ncol=1, nrow=1, sharex=False, 
                labHor = False, hSpaceSetting = 0.4, wSpaceSetting = 0.4, labelPad = 15, axefont = 20):
    """Initiates and plots a figure and a set of axes.

    Parameters
    ----------
    xsize : float
        size of the figure's x-dimension
    ysize : float
        size of the figure's y-dimension
    xlabel : string
        label for the x-axis
    ylabel : string
        label for the y-axis
    equal : boolean
        (optional) true if the axis relative dimensions are to be the same

    Returns
    -------
    fig
        the figure variable
    ax
        the axis variable
    """

    plt.rc("text", usetex=True)
    plt.rc("font", family="serif")
    matplotlib.rcParams["text.latex.preamble"] = r"\usepackage{amsmath, xcolor, siunitx}"

    # set global plotting parameters
    linew = 5.0  # line width
    # msize = 14 #marker size
    axew = 1.0  # axes width

    # set the distance to offset the numbers from the ticks
    numpad = 10

    # set global tick parameters
    majw = axew  # major tick width
    majl = 2.0  # major tick length
    minw = axew  # minor tick width
    minl = 2.0  # minor tick length

    # set global font sizes
    numsize = 20  # axis number font size
    legfont = 20  # legend font size
    
    # set label rotations
    if labHor is True:
        ylabelRot = 0    
    else:
        ylabelRot = 90

    fig, ax = plt.subplots(nrows=nrow, ncols=ncol, figsize=(xsize, ysize))

    if ncol == 1 and nrow == 1:
        ax.tick_params(
            axis="x",
            which="major",
            width=majw,
            length=majl,
            labelsize=numsize,
            zorder=1,
            direction="in",
            pad=numpad,
            top="off",
        )
        ax.tick_params(
            axis="x",
            which="minor",
            width=minw,
            length=minl,
            labelsize=numsize,
            zorder=1,
            direction="in",
            pad=numpad,
            top="off",
        )
        ax.tick_params(
            axis="y",
            which="major",
            width=majw,
            length=majl,
            labelsize=numsize,
            zorder=1,
            direction="in",
            pad=numpad,
            right="off",
        )
        ax.tick_params(
            axis="y",
            which="minor",
            width=minw,
            length=minl,
            labelsize=numsize,
            zorder=1,
            direction="in",
            pad=numpad,
            right="off",
        )
        ax.set_ylabel(y_label, fontsize=axefont, color="black", rotation = ylabelRot,  labelpad=labelPad)
        ax.set_xlabel(x_label, fontsize=axefont, color="black")
        if equal == True:
            ax.axis("equal")
        plt.subplots_adjust(hspace = hSpaceSetting, wspace = wSpaceSetting)

    elif ncol == 1 or nrow == 1:
        fig.subplots_adjust(right=0.75)
        for i in range(max([ncol, nrow])):
            ax[i].tick_params(
                axis="x",
                which="major",
                width=majw,
                length=majl,
                labelsize=numsize,
                zorder=1,
                direction="in",
                pad=numpad,
                top="off",
            )
            ax[i].tick_params(
                axis="x",
                which="minor",
                width=minw,
                length=minl,
                labelsize=numsize,
                zorder=1,
                direction="in",
                pad=numpad,
                top="off",
            )
            ax[i].tick_params(
                axis="y",
                which="major",
                width=majw,
                length=majl,
                labelsize=numsize,
                zorder=1,
                direction="in",
                pad=numpad,
                right="off",
            )
            ax[i].tick_params(
                axis="y",
                which="minor",
                width=minw,
                length=minl,
                labelsize=numsize,
                zorder=1,
                direction="in",
                pad=numpad,
                right="off",
            )

            ax[i].set_ylabel(y_label[i], fontsize=axefont, color="black", rotation = ylabelRot,  labelpad=labelPad)
            ax[i].set_xlabel(x_label[i], fontsize=axefont, color="black")
            if equal == True:
                ax[i].axis("equal")
        plt.subplots_adjust(hspace = hSpaceSetting, wspace = wSpaceSetting)

    else:
        fig.subplots_adjust(right=0.75)
        for i in range(nrow):
            for j in range(ncol):
                ax[i, j].tick_params(
                    axis="x",
                    which="major",
                    width=majw,
                    length=majl,
                    labelsize=numsize,
                    zorder=1,
                    direction="in",
                    pad=numpad,
                    top="off",
                )
                ax[i, j].tick_params(
                    axis="x",
                    which="minor",
                    width=minw,
                    length=minl,
                    labelsize=numsize,
                    zorder=1,
                    direction="in",
                    pad=numpad,
                    top="off",
                )
                ax[i, j].tick_params(
                    axis="y",
                    which="major",
                    width=majw,
                    length=majl,
                    labelsize=numsize,
                    zorder=1,
                    direction="in",
                    pad=numpad,
                    right="off",
                )
                ax[i, j].tick_params(
                    axis="y",
                    which="minor",
                    width=minw,
                    length=minl,
                    labelsize=numsize,
                    zorder=1,
                    direction="in",
                    pad=numpad,
                    right="off",
                )
                ax[i, j].set_ylabel(
                    y_label[2*i+j], fontsize=axefont, color="black", rotation = ylabelRot,  labelpad=labelPad)
                ax[i, j].set_xlabel(
                    x_label[2*i+j], fontsize=axefont, color="black")
                if equal == True:
                    ax[i, j].axis("equal")
        plt.subplots_adjust(hspace = hSpaceSetting, wspace = wSpaceSetting)

    plt.tight_layout()

    return fig, ax
