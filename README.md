# Experimental constraint generator

# General Overview
## Each given interface is governed by one set of equations to determine its input and output delays.
## We store them in the tool so that you only have to provide hardware measurements that are actually per design.
## As a bonus, we can store part numbers and their info for when parts are reused across designs
## Offers ability to map standard equations to your specific design to generate the constraints needed 
## Stored in a text format for easy diff tracking - no more annoying binary excel sheets or (gasp) powerpoints
## Easily hooks into python - hardware team can either edit directly or they edit excel and we auto-update yaml

# File Overview
## /core contains the parsers/generators
## /interfaces contains interface definitions - RGMII, SPI, etc.
## /parts contains part definitions - reference by some global part number and add properties of its interfaces to be stored
## /tmp for now houses what would be stored with a project, the minimum data required to generate the set of constraints given interfaces and parts

# Please provide any suggestions at all!  test.sdc is left as a first example of what is generated when running on this checkout