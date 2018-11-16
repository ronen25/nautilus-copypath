#----------------------------------------------------------------------------------------
# nautilus-copypath - Quickly copy file paths to the clipboard from Nautilus.
# Copyright (C) Ronen Lapushner 2017-2018.
# Distributed under the GPL-v3+ license. See LICENSE for more information
#----------------------------------------------------------------------------------------

import gi

gi.require_version('Nautilus', '3.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Nautilus, GObject, Gtk, Gdk

class CopyPathExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        # Initialize clipboard
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

    def __sanitize_path(self, path):
        # Replace spaces and parenthesis with their Linux-compatible equivalents. 
        return path.replace(' ', '\\ ').replace('(', '\\(').replace(')', '\\)')

    def __copy_files_path(self, menu, files):
        pathstr = None

        # Get the paths for all the files.
        # Also, strip any protocol headers, if required.
        paths = [self.__sanitize_path(fileinfo.get_location().get_path())
                for fileinfo in files]
        
        # Append to the path string
        if len(files) > 1:
            pathstr = '\n'.join(paths)
        elif len(files) == 1:
            pathstr = paths[0]

        # Set clipboard text
        if pathstr is not None:
            self.clipboard.set_text(pathstr, -1)

    def __copy_dir_path(self, menu, path):
        if path is not None:
            pathstr = self.__sanitize_path(path.get_location().get_path())
            self.clipboard.set_text(pathstr, -1)

    def get_file_items(self, window, files):
        # If there are many items to copy, change the label
        # to reflect that.
        if len(files) > 1:
            item_label = 'Copy Paths'
        else:
            item_label = 'Copy Path'

        item_copy_path = Nautilus.MenuItem(
            name='PathUtils::CopyPath',
            label=item_label,
            tip='Copy the full path to the clipboard'
        )
        item_copy_path.connect('activate', self.__copy_files_path, files)
        
        return item_copy_path,

    def get_background_items(self, window, file):
        item_copy_dir_path = Nautilus.MenuItem(
            name='PathUtils::CopyCurrentDirPath',
            label='Copy Directory Path',
            tip='''Copy the current directory's path to the clipboard'''
        )

        item_copy_dir_path.connect('activate', self.__copy_dir_path, file)

        return item_copy_dir_path,

