# nautilus-copypath
A small Nautilus extension for quickly copying file/Samba paths.

[]

## General
This plugin adds two new menu items in Nautilus' context menu: `Copy file path` and `Copy Windows path`.
The `Copy file path` option will quickly copy the file's full path.
The `Copy Windows path` will attempt to convert a Samba path to a valid Windows path.

## Installation
To successfully install the plugin you need:
1. Python >= 3.2
2. GNOME >= 3.18 (tested on Ubuntu GNOME 16.04, Fedora 25/26)
3. GObject Python bindings (development libraries)
4. nautilus-python

To install dependencies on Fedora simply use:
```
$ sudo dnf install nautilus-python python3-gobject
```

Clone the repository:
```
git clone https://github.com/ronen25/nautilus-copypath
```

Copy the file to the appropriate folder, creating it if needed:
```
mkdir ~/.local/share/nautilus-python
mkdir ~/.local/share/nautilus-python/extensions
cp nautilus-copypath.py ~/.local/share/nautilus-python/extensions/
```

Restart Nautilus.
