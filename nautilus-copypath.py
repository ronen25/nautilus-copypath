#----------------------------------------------------------------------------------------
# nautilus-copypath
#
# Redistributed under the Unlicense license.
# See LICENSE file for more information.
#----------------------------------------------------------------------------------------

import os
import gi
gi.require_version('Nautilus', '3.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Nautilus, GObject, Gtk, Gdk

class PathUtilsExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        # Initialize clipboard
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

    def __copy_path(self, menu, files):
        pathstr = ''

        # Get the paths for all the files.
        # Also, strip any protocol headers, if required.
        locations = [fileinfo.get_uri().replace('file://', '') for fileinfo in files]
        
        # Append to the path string
        if len(files) > 1:
            pathstr = '\n'.join(locations)
        else:
            pathstr = locations[0]

        # Set clipboard text
        self.clipboard.set_text(pathstr, -1)

    def __copy_windows_path(self, menu, files):
        pathstr = files[0].get_uri()

        # Strip 'smb://' and convert slashes to backslashes
        if 'smb://' in pathstr:
            pathstr = pathstr.replace('smb://', '\\\\').replace('/', '\\')

        # Set clipboard text
        self.clipboard.set_text(pathstr, -1)

    def get_file_items(self, window, files):
        items = []

        item_copy_path = Nautilus.MenuItem(
            name='PathUtils::CopyPath',
            label='Copy file path',
            tip='Copy the file\'s full path to the clipboard'
        )
        item_copy_path.connect('activate', self.__copy_path, files)
        items.append(item_copy_path)

        # If we have only one file, and it's has a samba file path, add an
        # other menu item.
        item_copy_windows_path = Nautilus.MenuItem(
            name='PathUtils::CopySambaPathAsWindows',
            label='Copy Windows path',
            tip='Converts the Samba path to a valid Windows path'
        )
        item_copy_windows_path.connect('activate', self.__copy_windows_path, files)
        items.append(item_copy_windows_path)

        return items

    def get_background_items(self, window, files):
        return self.get_file_items(window, files)

