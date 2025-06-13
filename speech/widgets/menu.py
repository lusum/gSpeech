import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .about import on_about
from .events import (
    changed_lang_menu, changed_speed_menu,
    on_destroy, on_execute, on_media_dialog,
    on_play_pause, on_reload, on_stop
)
from .option import on_options
from .save import on_save
from ..i18n import (
    _about, _languages, _multimedia_window, _options, _quit,
    _read_clipboard, _read_selected, _refresh,
    _save, _stop, _voice_speed
)


def generic_item(
    menu,
    label,
    callback,
    window=None,
    conf=None,
    menu_play_pause=None,
    win_play_pause=None,
    player=None
):
    """Generic item menu"""
    item = Gtk.MenuItem.new_with_label(label)
    item.connect(
        'activate',
        callback,
        window,
        conf,
        menu_play_pause,
        win_play_pause,
        player
    )
    menu.append(item)


def separator_item(menu):
    """Separator item"""
    item = Gtk.SeparatorMenuItem()
    menu.append(item)


def langs_item(menu, ind, tray, conf, lang_combobox, menu_langs):
    item = Gtk.MenuItem.new_with_label(_languages)
    item.show()
    item.set_submenu(menu_langs)
    # Creating languages items in submenu
    sub_item = Gtk.RadioMenuItem()
    for index, lang in enumerate(conf.list_langs):
        sub_item = Gtk.RadioMenuItem.new_with_label_from_widget(
            sub_item,
            lang
        )
        menu_langs.append(sub_item)
        sub_item.connect(
            'toggled',
            changed_lang_menu,
            ind,
            tray,
            lang,
            conf,
            lang_combobox,
            index
        )
        if lang == conf.lang:
            sub_item.set_active(True)
        sub_item.show()
    menu.append(item)


def voice_speed_item(menu, conf, voice_combobox, menu_voice_speed):
    item = Gtk.MenuItem.new_with_label(_voice_speed)
    item.show()
    item.set_submenu(menu_voice_speed)
    # Creating voice speed items in submenu
    sub_item = Gtk.RadioMenuItem()
    for index, speed in enumerate(conf.list_voice_speed):
        sub_item = Gtk.RadioMenuItem.new_with_label_from_widget(
            sub_item,
            str(speed)
        )
        menu_voice_speed.append(sub_item)
        sub_item.connect(
            'toggled',
            changed_speed_menu,
            speed,
            conf,
            voice_combobox,
            index
        )
        if speed == conf.voice_speed:
            sub_item.set_active(True)
        sub_item.show()
    menu.append(item)


def on_right_click(
    icon,
    event_button,
    event_time,
    window,
    ind,
    tray,
    conf,
    menu_play_pause,
    win_play_pause,
    player,
    lang_combobox,
    menu_langs,
    voice_combobox,
    menu_voice_speed
):
    """action on right click : create menu"""
    menu = Gtk.Menu()
    generic_item(
        menu,
        _read_clipboard,
        on_execute,
        window,
        conf,
        menu_play_pause,
        win_play_pause,
        player
    )
    generic_item(
        menu,
        _read_selected,
        on_execute,
        window,
        conf,
        menu_play_pause,
        win_play_pause,
        player
    )
    menu_play_pause.connect(
        'activate',
        on_play_pause,
        window,
        conf,
        menu_play_pause,
        win_play_pause,
        player
    )
    menu.append(menu_play_pause)
    generic_item(
        menu,
        _stop,
        on_stop,
        menu_play_pause=menu_play_pause,
        win_play_pause=win_play_pause,
        player=player
    )
    generic_item(menu, _save, on_save, window, conf)
    separator_item(menu)
    generic_item(menu, _multimedia_window, on_media_dialog, window)
    separator_item(menu)
    langs_item(menu, ind, tray, conf, lang_combobox, menu_langs)
    voice_speed_item(menu, conf, voice_combobox, menu_voice_speed)
    generic_item(menu, _refresh, on_reload)
    generic_item(menu, _about, on_about, window, conf)
    generic_item(menu, _options, on_options, window, conf)
    generic_item(menu, _quit, on_destroy, conf=conf)
    if conf.has_app_indicator:
        menu.show_all()
        ind.set_menu(menu)
        return
    menu.popup(
        None,
        None,
        None,
        tray,
        event_button,
        event_time
    )
