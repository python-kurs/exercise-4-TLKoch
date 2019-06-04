import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

basedir = Path("C:/Users/Kochti/Desktop/Studium/Python/exercise-4-TLKoch/")
data_dir = basedir / "data"


outputdir = basedir / "output"    
# outputdir.mkdir()
    
    
# Import both data tables into python using pandas. Set the index column to "MESS_DATUM" and parse the column values as dates. [1P]
garmisch_dir  = data_dir / "produkt_klima_tag_20171010_20190412_01550.txt"
zugspitze_dir = data_dir / "produkt_klima_tag_20171010_20190412_05792.txt"

garmisch = pd.read_csv(garmisch_dir, parse_dates=["MESS_DATUM"], index_col="MESS_DATUM", sep = ";")
zugspitze = pd.read_csv(zugspitze_dir, parse_dates=["MESS_DATUM"], index_col="MESS_DATUM", sep = ";")

# Clip the tables to the year 2018: [1P]
garmisch  = garmisch.loc["2018"]
zugspitze = zugspitze.loc["2018"]

# Resample the temperature data to monthly averages (" TMK") and store them in simple lists: [1P]
garmisch_agg  = list(garmisch.loc[:, " TMK"].resample("M").mean())
zugspitze_agg = list(zugspitze.loc[:, " TMK"].resample("M").mean())

# Define a plotting function that draws a simple climate diagram
# Add the arguments as mentioned in the docstring below [1P]
# Set the default temperature range from -15°C to 20°C and the precipitation range from 0mm to 370mm [1P]
def create_climate_diagram(
        df,
        temp_col,
        prec_col,
        title,
        filename,
        temp_min = -15,
        temp_max = 20,
        prec_min = 0,
        prec_max = 370):
    """
    Draw a climate diagram.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with values to plot from
    temp_col : str
        Name of temperature column
    prec_col : str
        Name of precipitation column
    title : String
        The title for the figure
    filename : String
        The name of the output figure
    temp_min : Number
        The minimum temperature value to display
    temp_max : Number
        The maximum temperature value to display
    prec_min : Number
        The minimum precipitation value to display
    prec_max : Number
        The maximum precipitation value to display

    Returns
    -------
    The figure
    
    """



    fig = plt.figure(figsize=(10,8))
    plt.rcParams['font.size'] = 16

    ax2 = fig.add_subplot(111)
    ax1 = ax2.twinx()
    
    days = mdates.DayLocator(bymonthday=28)
    monthFmt = mdates.DateFormatter("%b")
    ax2.xaxis.set_major_locator(days)
    ax2.xaxis.set_major_formatter(monthFmt)
    ax1.xaxis.set_major_locator(days)
    ax1.xaxis.set_major_formatter(monthFmt)
    
    
    # Set appropiate limits to each y-axis using the function arguments: [1P]
    
    ax2.set_ylim(prec_min, prec_max)
    ax1.set_ylim(temp_min, temp_max)
    
    

    # Draw temperature values as a red line and precipitation values as blue bars: [1P]
    # Hint: Check out the matplotlib documentation how to plot barcharts. Try to directly set the correct


    # agg sum Regen, mean Temp auf monatlich
    
    df = df.loc[:, [temp_col, prec_col]].resample("M").agg({temp_col: "mean", prec_col: "sum"})
    
    ax2.bar(x = df.index, height = list(df.loc[:, prec_col]), color = "b", width = 25, label = "Precipitation")
    ax1.plot(df.loc[:,temp_col], c="r", label = "Temperature")

    


    
    # Set appropiate labels to each y-axis: [1P]
    ax2.set_ylabel("Precipitation (mm)")
    ax1.set_ylabel("Temperature (°C)")

    # Give your diagram the title from the passed arguments: [1P]
    plt.title(title)

    # Save the figure as png image in the "output" folder with the given filename. [1P]
 
    plt.savefig(filename)
    
    
    
    return fig

# Use this function to draw a climate diagram for 2018 for both stations and save the result: [1P]
create_climate_diagram(df = garmisch,
                       filename = "garmisch.png", 
                       temp_col = " TMK", 
                       prec_col = " RSK", 
                       title = "Garmisch")

create_climate_diagram(df = zugspitze,
                       filename = "zugspitze.png", 
                       temp_col = " TMK", 
                       prec_col = " RSK", 
                       title = "Zugspitze")

