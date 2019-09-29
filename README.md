# Universal picker (Maya and Nuke)

Color picker that works both in Maya and Nuke (Pyside2) and includes custom buttons for specific Nuke-related and Maya-related actions. It lets the user pick a custom color, with different color system available to do so:

- Rgb (with optional alpha)
- Hsv
- Hexadecimal
- 3 different pantone libraries

### Nuke functionalities

| Button | Functionality|
| ------ | ------ |
|Button 1| "Painting" selected nodes (tile_color) with current color|
|Button 2| Creation of Constant node with current rgb(a) color|
|Button 3| Creation of Backdrop node with current color|
|SET button| Sets color-related knobs to current color|
|GET button| Retrieves any kind of knob value|
|Input/output line| Accepts single-line nuke commands|

### Maya functionalities

| Button | Functionality|
| ------ | ------ |
|Button 1| Creation of Lambert shader with current color|
|Button 2| Creation of aiStandardSurface shader with current color|
|Button 3| Creation of colorConstant node with current rgb(a) color|
|SET button| Sets color-related attributes to current color|
|GET button| Retrieves any kind of attribute value|
|Input/output line| Accepts single-line maya commands|

### Recommended way to launch
Install the module to your desired location and run:
```
from universal_picker import picker_launcher
picker_launcher.get_picker()
```

This module has been tested successfully in **Maya 2018.** and **Nuke 11.1v1**
***

For more info: www.jaimervq.com