# nautilus-copypath
A small Nautilus extension for quickly copying file/Samba paths.

![Screenshot](https://github.com/ronen25/nautilus-copypath/blob/master/nautilus_copypath_screenshot.png)

## General
This repository contains two plugins for Nautilus: `nautilus-copypath.py`, for quickly copying file paths,
and `nautilus-copywinpath`, for converting a copied Samba path to a Windows path.

You may choose to either install both of the plugins, or only one of them, as you see fit.

## Installation from Source
To successfully install the plugin you need:
1. Python >= 3.2
2. GNOME >= 3.18 (tested on Ubuntu 18.04, Fedora 25-28)
3. GObject Python bindings (development libraries)
4. nautilus-python

### Dependency Installation
| Distro | Command|
|--------|--------|
| Fedora | ``` $ sudo dnf install nautilus-python python3-gobject ``` |
| Ubuntu | ``` $ sudo apt-get install python-nautilus python3-gi ``` |

Clone the repository:
```
git clone https://github.com/ronen25/nautilus-copypath
```

Copy the file/s to the appropriate folder, creating it if needed:
```
mkdir ~/.local/share/nautilus-python
mkdir ~/.local/share/nautilus-python/extensions
cp nautilus-copypath.py ~/.local/share/nautilus-python/extensions/
cp nautilus-copywinpath.py ~/.local/share/nautilus-python/extensions/
```

Restart Nautilus.
