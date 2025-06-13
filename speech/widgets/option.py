import gi
from gi.repository import Gtk

gi.require_version('Gtk', '3.0')

from ..i18n import _acces_denied_path, _active_notification


def on_checked(checkBox, conf):
    conf.show_notification = checkBox.get_active()
    conf.update()


def option_content(box, conf):
    vbox = Gtk.VBox()
    box.add(vbox)
    hbox = Gtk.HBox()
    notification_check = Gtk.CheckButton(_active_notification)
    notification_check.set_active(conf.show_notification)
    notification_check.connect('toggled', on_checked, conf)
    hbox.add(notification_check)
    vbox.pack_start(hbox, False, False, 0)


class OptionWarningDialog(Gtk.MessageDialog):
    """ the options dialog class """

    def __init__(self, parent, conf, title):
        Gtk.MessageDialog.__init__(
            self,
            parent=parent,
            title=title,
            type=Gtk.MessageType.WARNING,
            message_format=_acces_denied_path % conf.path
        )
        self.set_border_width(10)
        box = self.get_content_area()
        option_content(box, conf)
        self.show_all()


class OptionDialog(Gtk.Dialog):
    """ the options dialog class """

    def __init__(self, parent, conf, title):
        Gtk.Dialog.__init__(
            self,
            parent=parent,
            title=title
        )
        self.set_border_width(10)
        box = self.get_content_area()
        option_content(box, conf)
        self.show_all()


def on_options(
    widget,
    window=None,
    conf=None,
    menu_play_pause=None,
    win_play_pause=None,
    player=None
):
    """show options dialog"""
    title = 'gSpeech : options'
    if conf.update():
        OptionDialog(window, conf, title)
        return
    OptionWarningDialog(window, conf, title)
