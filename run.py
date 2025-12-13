import streamlit
import streamlit_autorefresh

import streamlit.web.cli as stcli
import os, sys


def resolve_path(path):
    resolved_path = os.path.join(sys._MEIPASS, path)
    return resolved_path


if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        resolve_path("streamlit_app/streamlit_app.py"),
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())
