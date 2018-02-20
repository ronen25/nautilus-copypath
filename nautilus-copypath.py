#----------------------------------------------------------------------------------------
# nautilus-copypath
#
# Redistributed under the Unlicense license.
# See LICENSE file for more information.
#----------------------------------------------------------------------------------------

import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Nautilus', '3.0')
except Exception as e:
    print(e)
    exit(-1)
import os

from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Nautilus

class CopyPathExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        # Initialize clipboard
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

    def __copy_path(self, menu, files):
        pathstr = None

        # Get the paths for all the files.
        # Also, strip any protocol headers, if required.
        locations = [fileinfo.get_uri().replace('file://', '') for fileinfo in files]
        
        # Append to the path string
        if len(files) > 1:
            pathstr = '\n'.join(locations)
        elif len(files) == 1:
            pathstr = locations[0]

        # Set clipboard text
        if pathstr != None:
            self.clipboard.set_text(pathstr, -1)

    def get_file_items(self, window, files):
        item_copy_path = Nautilus.MenuItem(
            name='PathUtils::CopyPath',
            label='Copy file path',
            tip='Copy the file\'s full path to the clipboard'
        )
        item_copy_path.connect('activate', self.__copy_path, files)

        return item_copy_path,

    def get_background_items(self, window, files):
        return self.get_file_items(window, files)
