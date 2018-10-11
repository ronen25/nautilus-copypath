# nautilus-copypath
A small Nautilus extension for quickly copying file/Samba paths.

![Screenshot](https://github.com/ronen25/nautilus-copypath/blob/master/nautilus_copypath_screenshot.png)

## General
This repository contains two plugins for Nautilus:
1. `nautilus-copypath` - Quickly copy file/folder paths.
2. `nautilus-copywinpath` - Quickly copy Samba file/folder paths, converting them to Windows
paths on-the-fly.

You may choose to install both of the plugins, or only one of them, as you see fit.

## Installation from Source
To successfully install the plugin you need:
1. Python >= 3.2
2. GNOME >= 3.18 (tested on Ubuntu 16.04-18.04, Fedora 25-28, Arch Linux)
3. GObject Python bindings (development libraries)
4. nautilus-python

### Installing the Dependencies
Simply copy and paste the appropriate command for your distro:

| Distro | Command|
|--------|--------|
| Fedora | ``` $ sudo dnf install nautilus-python python3-gobject ``` |
| Ubuntu | ``` $ sudo apt-get install python-nautilus python3-gi ``` |
| Arch Linux | ``` $ sudo pacman -S python-gobject python-nautilus ``` |

### Installing the Extension
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

Restart Nautilus and the extension will be available.
