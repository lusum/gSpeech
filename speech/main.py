import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk, Gst, Gtk

from . import pid
from .conf import Conf
from .i18n import (
    _languages, _pause, _read_clipboard, _read_selected,
    _tooltip, _voice_speed
)
from .widgets import notify
from .widgets.events import (
    changed_cb, changed_speed, on_execute, on_left_click,
    on_play_pause, on_player, on_stop
)
from .widgets.menu import on_right_click
from .widgets.save import on_save


Gst.init('')

# load configuration
conf = Conf()

try:
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import AppIndicator3 as appindicator
except (ValueError, ImportError):
    pass


def generic_button(
    hbox,
    button,
    accel_group,
    key,
    label,
    callback,
    window,
    conf,
    menu_play_pause,
    win_play_pause,
    player,
    start=True
):
    button.add_accelerator(
        'clicked',
        accel_group,
        ord(key),
        Gdk.ModifierType.SHIFT_MASK,
        Gtk.AccelFlags.VISIBLE
    )
    if label:
        button.set_label(label)
    button.connect(
        'clicked',
        callback,
        window,
        conf,
        menu_play_pause,
        win_play_pause,
        player
    )
    if start:
        hbox.pack_start(button, False, False, 0)
        return
    hbox.pack_end(button, False, False, 0)


def lang_combobox(hbox, ind, tray, conf):
    combobox = Gtk.ComboBoxText.new()
    label = Gtk.Label(_languages)
    hbox.pack_start(label, False, False, 0)
    hbox.pack_start(combobox, False, False, 0)
    count = 0
    for lang in conf.list_langs:
        combobox.append_text(lang)
        if lang == conf.lang:
            combobox.set_active(count)
        count += 1
    combobox.connect('changed', changed_cb, ind, tray, conf)


def voice_speed_box(hbox, conf):
    combobox = Gtk.ComboBoxText.new()
    label = Gtk.Label(_voice_speed)
    hbox.pack_end(combobox, False, False, 0)
    hbox.pack_end(label, False, False, 0)
    count = 0
    for speed in conf.list_voice_speed:
        combobox.append_text(str(speed))
        if speed == conf.voice_speed:
            combobox.set_active(count)
        count += 1
    combobox.connect('changed', changed_speed, conf)


class MainApp:
    """The main class of the software"""
    def __init__(self, conf):
        notify.init(conf)
        window = Gtk.Window(title=conf.app_name, modal=True)
        player = on_player(conf.temp_path)
        win_play_pause = Gtk.Button(stock=Gtk.STOCK_MEDIA_PAUSE)

        # Play item menu
        menu_play_pause = Gtk.CheckMenuItem.new_with_label(_pause)

        ind = None
        tray = None
        if conf.has_app_indicator:
            ind = appindicator.Indicator.new(
                conf.app_name,
                conf.icon_path,
                appindicator.IndicatorCategory.APPLICATION_STATUS
            )
            ind.set_status(appindicator.IndicatorStatus.ACTIVE)
            on_right_click(
                window,
                ind,
                tray,
                conf,
                menu_play_pause,
                win_play_pause,
                player
            )
        else:
            tray = Gtk.StatusIcon()
            tray.set_from_file(conf.icon_path)
            tray.connect(
                'popup-menu',
                on_right_click,
                window,
                ind,
                tray,
                conf,
                menu_play_pause,
                win_play_pause,
                player
            )
            tray.connect(
                'activate',
                on_left_click,
                conf,
                menu_play_pause,
                win_play_pause,
                player
            )
            tray.set_tooltip_text(_tooltip)
        window.set_border_width(10)
        window.set_keep_above(True)
        window.set_icon_from_file(conf.icon_path)
        window.connect(
            'delete-event',
            lambda w, e: w.hide() or True
        )
        vbox = Gtk.VBox()
        hbox = Gtk.HBox()
        # Create an accelerator group
        accel_group = Gtk.AccelGroup()
        # Add the accelerator group to the toplevel window
        window.add_accel_group(accel_group)

        button = Gtk.Button()
        button.set_image(
            Gtk.Image.new_from_stock(
                Gtk.STOCK_EXECUTE,
                Gtk.IconSize.MENU
            )
        )
        generic_button(
            hbox,
            button,
            accel_group,
            'p',
            _read_clipboard,
            on_execute,
            window,
            conf,
            menu_play_pause,
            win_play_pause,
            player
        )
        button = Gtk.Button()
        button.set_image(
            Gtk.Image.new_from_stock(
                Gtk.STOCK_EXECUTE,
                Gtk.IconSize.MENU
            )
        )
        generic_button(
            hbox,
            button,
            accel_group,
            'c',
            _read_selected,
            on_execute,
            window,
            conf,
            menu_play_pause,
            win_play_pause,
            player
        )
        vbox.pack_start(hbox, False, False, 0)

        hbox = Gtk.HBox()
        generic_button(
            hbox,
            win_play_pause,
            accel_group,
            'x',
            None,
            on_play_pause,
            window,
            conf,
            menu_play_pause,
            win_play_pause,
            player
        )

        button = Gtk.Button(stock=Gtk.STOCK_MEDIA_STOP)
        generic_button(
            hbox,
            button,
            accel_group,
            'q',
            None,
            on_stop,
            window,
            conf,
            menu_play_pause,
            win_play_pause,
            player
        )

        button = Gtk.Button(stock=Gtk.STOCK_SAVE)
        generic_button(
            hbox,
            button,
            accel_group,
            's',
            None,
            on_save,
            window,
            conf,
            menu_play_pause,
            win_play_pause,
            player,
            False
        )
        vbox.pack_start(hbox, False, False, 0)

        hbox = Gtk.HBox()
        lang_combobox(hbox, ind, tray, conf)
        voice_speed_box(hbox, conf)
        vbox.pack_start(hbox, False, False, 0)

        window.add(vbox)

    def main(self):
        Gtk.main()


def main():
    pid.kill_if_already_exist(conf.app_name, conf.pid)
    gSpeech = MainApp(conf)
    gSpeech.main()
