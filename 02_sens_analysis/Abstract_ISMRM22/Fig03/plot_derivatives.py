#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 17:02:05 2020

@author: nscho

Edited on Wed March 29 12:52:30 2022
@editor: erg
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.offsetbox import AnchoredText
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

import sys
import os
sys.path.insert(0, os.path.join(os.environ['TOOLBOX_PATH'], 'python'))
import cfl

FS=20
MS=10
LW=4

DARK = 0 #dark layout?

COLOR=('darkgray', 'g', 'b', 'cyan', 'teal', 'darkorange')

BCOLOR='white'  # Background color
TCOLOR='black'  # Text color


if __name__ == "__main__":
        
        #Error if wrong number of parameters
        if( (len(sys.argv) < 4) or (1 == len(sys.argv)%2) ):
                print( "Files need to be passed in the cfl format and in pairs (see round brackets)!" )
                print( "Usage: plot_derivatives.py <savename> (<SA dR1> <finite dR1>) (<SA dR2> <finite dR2>) (<SA dB1> <finite dR1>)" )
                exit()
        
        sysargs = sys.argv

        filename = sysargs[1]

        #hdata = np.loadtxt(sysargs[2], unpack=True)

        # Import flexible number of files

        sa_data = []
        finite_data = []

        for i in range(2, len(sysargs), 2):

                print("Import file pair: "+sysargs[i]+", "+sysargs[i+1])

                # Information stored in real part
                sa_data.append(np.imag(cfl.readcfl(sysargs[i]).squeeze()))

                finite_data.append(np.imag(cfl.readcfl(sysargs[i+1]).squeeze()))

        # Define data characteristics! Hard coded!
        para = ['$\partial M/\partial R_1$', '$\partial M/\partial R_2$', '$\partial M/\partial B_1$']

        inset_loc = [(.4, .1), (.4, .5), (.4, .1)]

        #number_h_values=np.shape(finite_data[0])[1]


        """
        ------------------------------------
        ---------- Visualization -----------
        ------------------------------------
        """

        plt.rc('font', family='serif')

        if "DARK_LAYOUT" in os.environ:
                DARK = int(os.environ["DARK_LAYOUT"])

        if(DARK):
                plt.style.use(['dark_background'])
                BCOLOR='black'
                TCOLOR='white'
        else:
                plt.style.use(['default'])
        
        
        fig = plt.figure(figsize=(10, 15), dpi=120, edgecolor='w')

        axes = fig.subplots(nrows=3, ncols=1)
        
        # Main Slice-Profile Visualization

        for f in range(0,len(finite_data)):

                # Plot with visualization of DERIVATIVE

                ax1 = axes[f]

                c=0
                ax1.plot(finite_data[f], '-', color='b', alpha=1, linewidth=LW, label="DQ(h=1.00%)")
                c+=1
                
                ax1.plot(sa_data[f], '-', color='r', alpha=1, linewidth=LW, label="$\\bf{SAB}$")

                # Axis layout
                ax1.tick_params(axis='both', which='major', labelsize=FS)
                ax1.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
                ax1.yaxis.set_major_locator(plt.MaxNLocator(5))
                ax1.set_xlabel('Repetitions', fontsize=FS)
                ax1.set_ylabel(para[f], fontsize=FS)
                ax1.grid("on", color=TCOLOR, alpha=.1, linewidth=.5)

                # ZOOM IN DERIVATIVE

                axin = ax1.inset_axes((inset_loc[f][0], inset_loc[f][1],.4,.4))

                c=0
                axin.plot(finite_data[f], '-', color='b', alpha=1, linewidth=LW, label="H=1%")
                c+=1
                
                axin.plot(sa_data[f], '-', color='r', linewidth=LW, alpha=1, label="$\\bf{SAB}$")
                
                x1, x2 = 810, 1010 # specify the limits

                if (0 < np.max(np.array(finite_data[f][x1:x2]))):
                        y1 = np.min(np.array(finite_data[f][x1:x2]))*0.98
                        y2 = np.max(np.array(finite_data[f][x1:x2]))*1.005
                else:
                        y2 = np.min(np.array(finite_data[f][x1:x2]))*0.98
                        y1 = np.max(np.array(finite_data[f][x1:x2]))*1.035

                axin.set_xlim(x1, x2) # apply the x-limits
                axin.set_ylim(y1, y2) # apply the y-limits
                axin.grid("on", color=TCOLOR, alpha=.1, linewidth=.5)
                
                if (1 == f):
                        mark_inset(ax1, axin, loc1=3, loc2=4, fc="none", ec="0.5")
                else:
                        mark_inset(ax1, axin, loc1=1, loc2=2, fc="none", ec="0.5")


                # Plot with visualization of ERROR to reference

                #ax2 = axes[f, 1]

                # Scaling to convert to ppm
                #to_ppm = 1000

                # Second y-axis
                ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

                # Plot num. diff. scaled to maximum value
                # & divide by np.max value
                c=0
                ax2.plot(np.abs(finite_data[f]-sa_data[f]), '-', color='g', alpha=0.45, linewidth=LW, label='|DQ - SAB|')
                ax2.set_ylabel('|DQ - SAB|', fontsize=FS)
                c+=1
                
                # Plot SA error scaled to maximum value
                #ax1.plot(np.abs(sa_data[f]-deriv[f])*to_ppm, '-', color='r', alpha=1, linewidth=LW)

                # Axis layout
                #ax2.locator_params(axis='y', nbins=5)
                #ax2.tick_params(axis='both', which='major', labelsize=FS)
                #ax2.set_xlabel('Repetitions', fontsize=FS)
                # ax2.set_ylabel(para[f], color='k', fontsize=FS)
                #ax2.tick_params(axis='y', labelcolor=TCOLOR)
                #ax2.grid("on", color=TCOLOR, alpha=0.1, linewidth=.5)


                # ZOOM IN ERROR

                #axin2 = ax2.inset_axes((.4, .4,.4,.4))

                # Plot num. diff. scaled to maximum value
                #c=0
                #axin2.plot(np.abs(deriv[f]-finite_data[f][:,h])*to_ppm, '-', color=COLOR[c], alpha=1, linewidth=LW)
                #c+=1
                
                # Plot SA error scaled to maximum value
                #axin2.plot(np.abs(sa_data[f]-deriv[f])*to_ppm, '-', color='r', alpha=1, linewidth=LW)
                
                #x1, x2, y1, y2 = 810, 1010, -0.0001*to_ppm, 0.0005*to_ppm # specify the limits

                #axin2.set_xlim(x1, x2) # apply the x-limits
                #axin2.set_ylim(y1, y2) # apply the y-limits
                #axin2.grid("on", color=TCOLOR, alpha=.1, linewidth=.5)
                
                #mark_inset(ax2, axin2, loc1=3, loc2=4, fc="none", ec="0.5")

                # Add figure titles

                if(0 == f):
                        ax1.set_title("$\\bf{Partial}$ $\\bf{Derivative}$\n", fontsize=FS+5)
                        #ax2.set_title("$\\bf{|Error|}$ / ppm\n", fontsize=FS+5)

        # Add legend
        ax1Line, ax1Label = ax1.get_legend_handles_labels()
        ax2Line, ax2Label = ax2.get_legend_handles_labels()

        fig.legend(ax1Line + ax2Line, ax1Label + ax2Label, loc=8, bbox_to_anchor=(0.5, 0.9), fontsize=FS-5, fancybox=True, shadow=True, ncol=len(ax1Line+ax2Line))

        plt.tight_layout(pad=5)
        # plt.show(block = False)

        fig.savefig(filename+".png", transparent=False)
