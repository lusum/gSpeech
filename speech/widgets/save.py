import os
import shutil

import gi
from gi.repository import Gtk

from ..i18n import _save_speech, _wave_file

gi.require_version('Gtk', '3.0')


class SaveFileDialog(Gtk.FileChooserDialog):
    """ the class to save the speech .wav file """

    def __init__(self, parent, temp_path):
        Gtk.FileChooserDialog.__init__(
            self,
            _save_speech,
            parent,
            Gtk.FileChooserAction.SAVE,
            (
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OK,
                Gtk.ResponseType.OK
            )
        )
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_current_folder(os.path.expanduser('~'))

        _filter = Gtk.FileFilter()
        _filter.set_name(_wave_file)
        _filter.add_mime_type('audio/x-wav')
        _filter.add_pattern('*.wav')
        self.add_filter(_filter)

        response = self.run()
        if response == Gtk.ResponseType.OK:
            dest_path = self.get_filename() + '.wav'
            shutil.copy(temp_path, dest_path)
        self.destroy()


def on_save(
    widget,
    window=None,
    conf=None,
    menu_play_pause=None,
    win_play_pause=None,
    player=None
):
    """Saving file speech on clicking Save item"""
    SaveFileDialog(window, conf.temp_path)
