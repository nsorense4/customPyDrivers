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


def plot_custom(xsize, ysize, x_label, y_label, equal=False, ncol=1, nrow=1, 
                sharex=False, labHor = False, hSpaceSetting = 0.4, 
                wSpaceSetting = 0.4, labelPad = 15, axefont = 30, numsize = 25,
                legfont = 25, 
                commonX = False, commonY = False,
                spineColor = 'black', tickColor = 'black', axew = 2, axel = 2, widthBool = False,
                widthRatios = 1):
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

    # set the distance to offset the numbers from the ticks
    numpad = 10

    # set global tick parameters
    majw = axew  # major tick width
    majl = axel  # major tick length
    minw = axew  # minor tick width
    minl = axel  # minor tick length

    # set global font sizes
      # axis number font size
      # legend font size
    
    # set label rotations
    if labHor is True:
        ylabelRot = 0    
    else:
        ylabelRot = 90

    if commonX is True and commonY is False:
        if widthBool == False:
            fig, ax = plt.subplots(nrows=nrow, ncols=ncol, figsize=(xsize, ysize), sharex = 'col')
        else:
            fig, ax = plt.subplots(nrows=nrow, ncols=ncol, figsize=(xsize, ysize), sharex = 'col', 
                                   gridspec_kw={'width_ratios': widthRatios})
    elif commonY is True and commonX is False:
        if widthBool == False:
            fig, ax = plt.subplots(nrows=nrow, ncols=ncol, figsize=(xsize, ysize), sharey = 'row')
        else:
            fig, ax = plt.subplots(nrows=nrow, ncols=ncol, figsize=(xsize, ysize), sharey = 'row', 
                                   gridspec_kw={'width_ratios': widthRatios})
    elif commonY is True and commonX is True:
        if widthBool == False:
            fig, ax = plt.subplots(nrows=nrow, ncols=ncol, figsize=(xsize, ysize), sharey = 'row',
                                   sharex = 'col')
        else:
            fig, ax = plt.subplots(nrows=nrow, ncols=ncol, figsize=(xsize, ysize), sharey = 'row',
                                   sharex = 'col', gridspec_kw={'width_ratios': widthRatios})
    else:
        if widthBool == False:
            fig, ax = plt.subplots(nrows=nrow, ncols=ncol, figsize=(xsize, ysize))
        else:
            fig, ax = plt.subplots(nrows=nrow, ncols=ncol, figsize=(xsize, ysize), 
                                   gridspec_kw={'width_ratios': widthRatios})

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
            color=tickColor
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
            color=tickColor
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
            color=tickColor
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
            color=tickColor
        )
        ax.spines['bottom'].set_color(spineColor)
        ax.spines['top'].set_color(spineColor) 
        ax.spines['right'].set_color(spineColor)
        ax.spines['left'].set_color(spineColor)
        ax.set_ylabel(y_label, fontsize=axefont, color="black", rotation = ylabelRot, 
                      ha = 'center', va = 'center', labelpad=labelPad)
        ax.set_xlabel(x_label, fontsize=axefont, color="black", labelpad=labelPad)
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
                color=tickColor
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
                color=tickColor
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
                color=tickColor
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
                color=tickColor
            )
            ax[i].spines['bottom'].set_color(spineColor)
            ax[i].spines['top'].set_color(spineColor) 
            ax[i].spines['right'].set_color(spineColor)
            ax[i].spines['left'].set_color(spineColor)
        
        if commonX is False and commonY is False:
            for i in range(max([ncol, nrow])):
                ax[i].set_xlabel(x_label[i], fontsize=axefont, color="black", labelpad=labelPad)
                ax[i].set_ylabel(y_label[i], fontsize=axefont, color="black", labelpad=labelPad)
                if equal is True:
                    ax[i].axis("equal")
        elif commonX is True:
            for i in range(max([ncol, nrow])):
                plt.subplots_adjust(hspace = 0, wspace = 0)
                ax[i].set_ylabel(y_label[i], fontsize=axefont, color="black", rotation = ylabelRot,  
                                 ha = 'center', va = 'center',labelpad=labelPad)
            ax[-1].set_xlabel(x_label, fontsize=axefont, color="black", labelpad=labelPad)
        elif commonY is True:
            for i in range(max([ncol, nrow])):
                plt.subplots_adjust(hspace = 0, wspace = 0)
                ax[i].set_xlabel(x_label[i], fontsize=axefont, color="black",  
                                 ha = 'center', va = 'center',labelpad=labelPad)
            ax[0].set_ylabel(y_label, fontsize=axefont, color="black", labelpad=labelPad)
        

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
                    color=tickColor
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
                    color=tickColor
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
                    color=tickColor
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
                    color=tickColor
                )
                ax[i, j].spines['bottom'].set_color(spineColor)
                ax[i, j].spines['top'].set_color(spineColor) 
                ax[i, j].spines['right'].set_color(spineColor)
                ax[i, j].spines['left'].set_color(spineColor)
        if commonX is False and commonY is False:
            for i in range(nrow):
                for j in range(ncol):
                    ax[i,j].set_xlabel(x_label[nrow*i+j], fontsize=axefont, color="black", labelpad=labelPad)
                    ax[i,j].set_ylabel(y_label[nrow*i+j], fontsize=axefont, color="black", labelpad=labelPad)
                    if equal is True:
                        ax[i,j].axis("equal")
        elif commonX is True and commonY is False:
            for i in range(nrow):
                for j in range(ncol):
                    ax[i,j].set_ylabel(y_label[nrow*i+j], fontsize=axefont, color="black", labelpad=labelPad)
                    ax[-1, j].set_xlabel(x_label[j], fontsize=axefont, color="black", labelpad=labelPad)
                    if equal is True:
                        ax[i,j].axis("equal")
                    
        elif commonY is True and commonX is False:
            for i in range(nrow):
                for j in range(ncol):
                    ax[i,j].set_xlabel(x_label[nrow*i+j], fontsize=axefont, color="black", labelpad=labelPad)
                    if equal is True:
                        ax[i,j].axis("equal")
                ax[0,j].set_ylabel(y_label[i], fontsize=axefont, color="black", labelpad=labelPad)

        elif commonY is True and commonX is True:
            for i in range(ncol):
                ax[-1,i].set_xlabel(x_label[i], fontsize=axefont, color="black", labelpad=labelPad)
            for i in range(nrow):
                ax[i,0].set_ylabel(y_label[i], fontsize=axefont, color="black", labelpad=labelPad)
            if equal is True:
                for i in range(nrow):
                    for j in range(ncol):
                        ax[i,j].axis("equal")
                
        plt.subplots_adjust(hspace = hSpaceSetting, wspace = wSpaceSetting)

    plt.tight_layout()

    return fig, ax
