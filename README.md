# nautilus-copypath
A small Nautilus extension for quickly copying file/Samba paths.

![Screenshot](https://github.com/ronen25/nautilus-copypath/blob/master/screenshots/screenshot.png)

## Installation from Source
To successfully install the plugin you need:
1. Python >= 3.2
2. GNOME >= 3.18 (tested on Debian 10-12, Ubuntu 16.04-22.04, Fedora 25-37, Arch Linux)
3. GObject Python bindings (development libraries)
4. nautilus-python

### Installing the Dependencies
Simply copy and paste the appropriate command for your distro:

| Distro | Command|
|--------|--------|
| Fedora | ``` $ sudo dnf install nautilus-python python3-gobject ``` |
| Debian >= 12 | ``` $ sudo apt install python3-nautilus python3-gi ``` |
| Ubuntu | ``` $ sudo apt-get install python-nautilus python3-gi ``` |
| Arch Linux | ``` $ sudo pacman -S python-gobject python-nautilus ``` |

### Installing the Extension
Clone the repository:
```
git clone https://github.com/ronen25/nautilus-copypath
```

Copy the file/s to the appropriate folder, creating it if needed:
```bash
$ mkdir ~/.local/share/nautilus-python
$ mkdir ~/.local/share/nautilus-python/extensions
$ cp nautilus-copypath.py ~/.local/share/nautilus-python/extensions/
```

Restart Nautilus and the extension will be available:
```bash
$ nautilus -q
```

If that doesn't work try logging out and back in. 
