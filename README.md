# Scatter Map

This script is designed to create a map depicting the radiation levels due to scatter around a source.
The room, source and shield characteristics are determined by the user.
The resultant plot is to be used for **demonstration / illustration purposes only** - the radiation dose at specific points is based on a naive estimate and should not be used for determining appropriate shielding measures.

## Using the Script

Navigate to the folder containing scatter_map.py and run the program in command prompt / powershell. You will be asked for the following information:
_Note: See diagram further below for description of how distances / location of objects are defined._

* Room dimensions, width and length of the room
* Size and position of the source of scatter
* Magnitude of scatter radiation and the distance it was recorded
* Shield characteristics; dimensions, angle, code, etc
* Estimated energy of scatter.

After answering the all the prompts the script will generate a plot and save it in .png format in the same folder as scatter_map.png.
The plot is Log Normalized to take into account the full range of scatter readings.

### Layout Diagram

![Layout Diagram for Scatter Map](https://github.com/colemaro/scatter_map/blob/main/layout_diagram.png)
