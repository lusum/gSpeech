import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify
from gi.repository.Notify import Notification

from ..i18n import _no_text_selected, _reading_text_loading


def init(conf):
    Notify.init(conf.app_name)


def get(conf, text):
    if text is None:
        try:
            Notification.new(
                conf.app_name,
                _no_text_selected,
                conf.icon_path
            ).show()
        except Exception:
            pass
        return
    try:
        Notification.new(
            conf.app_name,
            _reading_text_loading,
            conf.icon_path
        ).show()
    except Exception:
        pass
