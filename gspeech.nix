{ lib
, python3
, gtk3
, wrapGAppsHook
, glibcLocales
, gobject-introspection
, gettext
, pango
, gdk-pixbuf
, atk
, libnotify
, libappindicator-gtk3
, gst_all_1
, sox
}:

python3.pkgs.buildPythonApplication rec {
  pname = "gSpeech";
  version = "0.9.2";

  src = lib.cleanSource ./.;

  nativeBuildInputs = [
    wrapGAppsHook
    gobject-introspection
    pango
    gdk-pixbuf
    atk
    gettext
    glibcLocales
    libnotify
    libappindicator-gtk3
    gst_all_1.gstreamer
    gst_all_1.gst-plugins-base
    gst_all_1.gst-plugins-good
  ];

  buildInputs = [
    gtk3
    python3
  ];

  propagatedBuildInputs = with python3.pkgs; [
    pygobject3
  ];

  meta = with lib; {
    description = "A minimal GUI for the Text To Speech 'Svox Pico'. Read clipboard or selected text in different languages and manage it : pause, stop, replay.";
    homepage = "https://github.com/mothsART/gSpeech";
    maintainers = with maintainers; [ mothsart ];
    license = licenses.gpl3;
    platforms = platforms.unix;
  };
}
