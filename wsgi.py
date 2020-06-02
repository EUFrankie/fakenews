# *- coding: utf-8 -*-
from application import create_app
import os

port = int(os.environ.get("PORT", 5000))
debug = bool(os.environ.get("DEBUGING_ENABLED", True))

app = create_app()

if __name__ == "__main__":
    app.run(debug=debug, host="0.0.0.0", port=port)

