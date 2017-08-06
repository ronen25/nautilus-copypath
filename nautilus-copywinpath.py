#----------------------------------------------------------------------------------------
# nautilus-copywinpath
#
# Redistributed under the Unlicense license.
# See LICENSE file for more information.
#----------------------------------------------------------------------------------------

import os
import gi
gi.require_version('Nautilus', '3.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Nautilus, GObject, Gtk, Gdk

class CopySambaToWindowsPathExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        # Initialize clipboard
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

    def __copy_windows_path(self, menu, files):
        pathstr = files[0].get_uri()

        # Strip 'smb://' and convert slashes to backslashes
        if 'smb://' in pathstr:
            pathstr = pathstr.replace('smb://', '\\\\').replace('/', '\\')

        # Set clipboard text
        self.clipboard.set_text(pathstr, -1)

    def get_file_items(self, window, files):
        item_copy_windows_path = Nautilus.MenuItem(
            name='PathUtils::CopySambaPathAsWindows',
            label='Copy Windows path',
            tip='Converts the Samba path to a valid Windows path'
        )
        item_copy_windows_path.connect('activate', self.__copy_windows_path, files)

        return [ item_copy_windows_path, ]

    def get_background_items(self, window, files):
        return self.get_file_items(window, files)

