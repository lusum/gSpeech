import gettext

import gi
from gi.repository import GdkPixbuf, Gtk

from speech import __version__

gi.require_version('Gtk', '3.0')

_ = gettext.gettext


class AboutDialog(Gtk.AboutDialog):
    """ the about dialog class """

    def __init__(self, parent, conf):
        Gtk.AboutDialog.__init__(self, parent=parent)
        self.set_logo(GdkPixbuf.Pixbuf.new_from_file(conf.icon_path))
        self.set_name(conf.app_name)
        self.set_version(__version__)
        self.set_copyright(conf.copyrights)
        self.set_license(conf.license)
        self.set_authors([mail for name, mail in conf.developers])
        self.set_comments(conf.comment)
        self.set_translator_credits('\n'.join(conf.translators))
        self.set_website(conf.website)
        self.set_website_label(_("""%s's Website""") % conf.app_name)
        self.connect('response', lambda self, *f: self.destroy())
        self.show_all()


def on_about(
    widget,
    window=None,
    conf=None,
    menu_play_pause=None,
    win_play_pause=None,
    player=None
):
    """Show about dialog"""
    AboutDialog(window, conf)
