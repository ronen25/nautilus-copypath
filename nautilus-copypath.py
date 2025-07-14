# ----------------------------------------------------------------------------------------
# nautilus-copypath - Quickly copy file paths to the clipboard from Nautilus.
# Copyright (C) Ronen Lapushner 2017-2025.
# Copyright (C) Fynn Freyer 2023.
# Distributed under the GPL-v3+ license. See LICENSE for more information
# ----------------------------------------------------------------------------------------

from gi.repository import Nautilus, GObject, Gdk, Gtk
import os
from platform import system

import gi

# Import the correct GI version
gi_version_major = 3 if 30 <= gi.version_info[1] < 40 else 4
gi.require_versions({
    'Nautilus': '3.0' if gi_version_major == 3 else '4.0',
    'Gdk': '3.0' if gi_version_major == 3 else '4.0',
    'Gtk': '3.0' if gi_version_major == 3 else '4.0'
})


class CopyPathExtensionSettings:
    """
    Configuration object for the nautilus-copypath extension.
    Can be automatically populated from ``NAUTILUS_COPYPATH_*`` environment variables.
    """

    @staticmethod
    def __cast_env_var(name, default=None):
        """
        Try to cast the value of ${name} to a python object.

        :param name: The name of the environment variable. E.g., "``NAUTILUS_COPYPATH_WINPATH``".
        :param default: Optionally, a default value if the environment variable is not set. Standard is ``None``.
        :return: The value of the environment variable. Will be cast to bool for integers and certain strings.
        """

        value = os.environ.get(name, default)

        # define a mapping for common boolean keywords
        cast_map = {
            'true': True,
            'yes': True,
            'y': True,
            'false': False,
            'no': False,
            'n': False,
        }

        # if the env var is defined, i.e. different from the default
        if value != default:
            # we try two different casts to boolean
            # first we cast to bool via int, if this fails,
            # secondly we fall back to our cast map,
            # otherwise just return the string
            try:
                value = bool(int(value))
            except ValueError:
                try:
                    value = cast_map[value.lower()]
                except KeyError:
                    pass

        return value

    def __init__(self):
        is_windows = system() == 'Windows'
        self.winpath = self.__cast_env_var(
            'NAUTILUS_COPYPATH_WINPATH', default=is_windows)
        self.sanitize_paths = self.__cast_env_var(
            'NAUTILUS_COPYPATH_SANITIZE_PATHS', default=True)
        self.quote_paths = self.__cast_env_var(
            'NAUTILUS_COPYPATH_QUOTE_PATHS', default=False)

        # use system default for line breaks
        line_break = '\r\n' if is_windows else '\n'
        # we want to avoid casting to bool here, so we take the value from env directly
        path_separator = os.environ.get(
            'NAUTILUS_COPYPATH_PATH_SEPARATOR', line_break)
        # enable using os.pathsep
        self.path_separator = os.pathsep if path_separator == 'os.pathsep' else path_separator

    winpath = False
    """
    Whether to assume Windows-style paths. Default is determined by result of ``platform.system()``.

    Controlled by the ``NAUTILUS_COPYPATH_WINPATH`` environment variable.
    """

    sanitize_paths = True
    """
    Whether to escape paths. Defaults to true.

    Controlled by the ``NAUTILUS_COPYPATH_SANITIZE_PATHS`` environment variable.
    """

    quote_paths = False
    """
    Whether to surround paths with quotes. Defaults to false.

    Controlled by the ``NAUTILUS_COPYPATH_QUOTE_PATHS`` environment variable.
    """

    path_separator = ''
    r"""
    The symbol to use for separating multiple copied paths.
    Defaults to LF (line feed) on *nix and CRLF on Windows.

    Another possible value is ``os.pathsep`` to use the default path separator for the system.

    Controlled by ``NAUTILUS_COPYPATH_PATH_SEPARATOR``.
    """


class CopyPathExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        # Initialize clipboard
        if gi_version_major == 4:
            self.clipboard = Gdk.Display.get_default().get_clipboard()
        else:
            self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        self.config = CopyPathExtensionSettings()

        # Determine appropriate sanitization function
        self.__sanitize_path = self.__sanitize_nix_path
        if self.config.winpath:
            self.__sanitize_path = self.__sanitize_win_path

    def __transform_paths(self, paths):
        """Modify paths based on config values and transform them into a string."""
        if self.config.sanitize_paths:
            paths = [self.__sanitize_path(path) for path in paths]

        if self.config.quote_paths:
            paths = ['"{}"'.format(path) for path in paths]

        return paths

    @staticmethod
    def __sanitize_nix_path(path):
        # Replace spaces and parenthesis with their Linux-compatible equivalents.
        return path.replace(' ', '\\ ').replace('(', '\\(').replace(')', '\\)')

    @staticmethod
    def __sanitize_win_path(path):
        return path.replace('smb://', '\\\\').replace('/', '\\')

    def __copy_files_path(self, menu, files):
        pathstr = None

        # Get the paths for all the files.
        # Also, strip any protocol headers, if required.
        # TODO confirm with author:
        #  windows function doesn't sanitize file names here.
        #  is this correct? if so this behavior needs to change
        #  also, this would probably a lot cleaner with pathlib
        paths = self.__transform_paths([
            fileinfo.get_location().get_path()
            for fileinfo in files
        ])

        # Append to the path string
        if len(files) > 1:
            pathstr = self.config.path_separator.join(paths)
        elif len(files) == 1:
            pathstr = paths[0]

        # Set clipboard text
        if pathstr is not None:

            if gi_version_major == 4:
                self.clipboard.set(pathstr)
            else:
                self.clipboard.set_text(pathstr, -1)

    def __copy_dir_path(self, menu, path):
        if path is not None:
            pathstr = self.__transform_paths([path.get_location().get_path()])

            if gi_version_major == 4:
                self.clipboard.set(pathstr)
            else:
                self.clipboard.set_text(pathstr, -1)

    def get_file_items(self, *args, **kwargs):
        files = args[0] if gi_version_major == 4 else args[1]

        # Pluralize label if needed
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

    def get_background_items(self, *args, **kwargs):
        file = args[0] if gi_version_major == 4 else args[1]

        item_copy_dir_path = Nautilus.MenuItem(
            name='PathUtils::CopyCurrentDirPath',
            label='Copy Directory Path',
            tip='''Copy the current directory's path to the clipboard'''
        )

        item_copy_dir_path.connect('activate', self.__copy_dir_path, file)

        return item_copy_dir_path,
