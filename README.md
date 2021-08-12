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

### Examples

Both of the following plots used the same values for room and source characteristics. 
Example 2 has the inclusion of a shield.

**Details**
* Room is 5m wide, 4m long
* Source is 50cm across and 3m from left wall and 1.5m from bottom wall
* Scatter reading is 5 µSv/hr taken at 1m and assumed to have an energy of 50 kV
* Shield start position is located at 1m from left wall and 3m from bottom wall
* Shield is tilted at 45 degrees to the normal (bottom wall)
* Shield is 1m long and is Code 3

![Example 1](https://github.com/colemaro/scatter_map/blob/main/examples/example1_noshield.png)

![Example_2](https://github.com/colemaro/scatter_map/blob/main/examples/example2_shield.png)

Take note how the diagrams look distinctly different even though it's the same dose at each point in front of the shield.
The colour map will be skewed by extremes created by shielding. 

_Created by Ronan Coleman for MMUH Physics Department, Dublin, Ireland_
