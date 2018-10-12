#----------------------------------------------------------------------------------------
# nautilus-copywinpath - Quickly copy file paths to the clipboard from Nautilus.
# Copyright (C) Ronen Lapushner 2017-2018.
# Distributed under the GPL-v3+ license. See LICENSE for more information
#----------------------------------------------------------------------------------------

import gi

gi.require_version('Nautilus', '3.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Nautilus, GObject, Gtk, Gdk

class CopySambaToWindowsPathExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        # Initialize clipboard
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

    def __sanitize_path(self, path):
        return path.replace('smb://', '\\\\').replace('/', '\\')

    def __copy_windows_path(self, menu, files):
        pathstr = None

        # Get the paths for all the files.
        paths = [fileinfo.get_location().get_path() for fileinfo in files]

        # Append to the path string
        if len(files) > 1:
            pathstr = '\n'.join(paths)
        elif len(files) == 1:
            pathstr = paths[0]

        # Set clipboard text
        if pathstr is not None:
            self.clipboard.set_text(pathstr, -1)

    def __copy_windows_dir_path(self, menu, path):
        if path is not None:
            pathstr = path.get_location().get_path()
            self.clipboard.set_text(self.__sanitize_path(pathstr), -1)

    def get_file_items(self, window, files):
        # If there are multiple items to copy, change the label
        # to reflect that.
        if len(files) > 1:
            item_label = 'Copy Windows Paths'
        else:
            item_label = 'Copy Windows Path'

        item_copy_windows_path = Nautilus.MenuItem(
            name='PathUtils::CopySambaPathAsWindows',
            label=item_label,
            tip='Copy the Samba path as a Windows path to the clipboard'
        )
        item_copy_windows_path.connect('activate', self.__copy_windows_path, files)

        return item_copy_windows_path,

    def get_background_items(self, window, file):
        item_copy_windows_dir_path = Nautilus.MenuItem(
            name='PathUtils::CopySambaDirPathAsWindows',
            label='Copy Directory Windows Path',
            tip='Copy the Samba path of the current directory, as a Windows path, to the clipboard'
        )

        item_copy_windows_dir_path.connect('activate', self.__copy_windows_dir_path, file)

        return item_copy_windows_dir_path,

