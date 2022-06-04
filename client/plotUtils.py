import pandas as pd
import numpy as np
import fastf1 as ff1
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection

def plotLapSpeedHeatmap(telemetry: dict) -> mpl.figure.Figure:
    # Get telemetry data
    x = telemetry['X']              # values for x-axis
    y = telemetry['Y']              # values for y-axis
    color = pd.Series(telemetry["Speed"])
    #color = telemetry['Speed']     # value to base color gradient on

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    # We create a plot with title and adjust some setting to make it look good.
    fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
    fig.suptitle("Speed in km/h", x=0.5, y=0)
    
    # Adjust margins and turn of axis
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
    ax.axis('off')

    # After this, we plot the data itself.
    # Create background track line
    ax.plot(x, y, color='black', linestyle='-', linewidth=16, zorder=0)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(0, 380)
    lc = LineCollection(segments, cmap=mpl.cm.plasma, norm=norm, linestyle='-', linewidth=5)

    # Set the values used for colormapping
    lc.set_array(color)

    # Merge all line segments together
    line = ax.add_collection(lc)

    # Finally, we create a color bar as a legend.
    cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
    normlegend = mpl.colors.Normalize(vmin=0, vmax=380)
    legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=mpl.cm.plasma, orientation="horizontal")

    # Save and show the plot
    #plt.savefig('prova.png')
    return fig

def plotLapGearsHeatmap(telemetry: dict) -> mpl.figure.Figure:
    #Prepare the data for plotting by converting it to the appropriate numpy data types

    x = np.array(telemetry['X'])
    y = np.array(telemetry['Y'])

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    gear = np.array(telemetry['nGear'], dtype=np.float32)

    #Create a line collection. Set a segmented colormap and normalize the plot to full integer values of the colormap
    cmap = mpl.cm.get_cmap('Paired')
    lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
    lc_comp.set_array(gear)
    lc_comp.set_linewidth(4)

    #Create the plot
    fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(4, 3))
    plt.gca().add_collection(lc_comp)
    plt.axis('equal')
    plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

    #Add a colorbar to the plot. Shift the colorbar ticks by +0.5 so that they are centered for each color segment.
    cbar = plt.colorbar(mappable=lc_comp, label="Gear", boundaries=np.arange(1, 10))
    cbar.set_ticks(np.arange(1.5, 9.5))
    cbar.set_ticklabels(np.arange(1, 9))

    return fig

def plotAnomnalyScores(anomaly_scores: dict, anomaly_threshold: float) -> mpl.figure.Figure:
    keys = anomaly_scores.keys()
    vals = anomaly_scores.values()

    fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(10, 4))

    plt.bar(x=list(anomaly_scores.keys()), height=list(anomaly_scores.values()), label="Anomaly score value")

    plt.axline(xy1=(0, anomaly_threshold), slope=0, color='red', linestyle='--')

    plt.ylim(0,1000)
    plt.ylabel ('Anomaly Score')
    plt.xlabel ('Lap number')
    plt.xticks(list(keys))
    plt.legend (bbox_to_anchor=(1, 1), loc="upper right", borderaxespad=0.)

    return fig