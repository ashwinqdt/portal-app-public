import os

from portal_app.utils.config import ROUTE_PREFIX
from portal_app.utils.common import *
from portal_app.appshell.layout import app_layout
from portal_app.appshell.callbacks import register_appshell_callbacks
from portal_app.pages.catalog.callbacks import catalog_callbacks
from portal_app.pages.apps.callbacks import apps_callbacks

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DSS_APP_DIR = os.path.join(CURRENT_DIR, 'portal_app')
PAGES_DIR = os.path.join(DSS_APP_DIR, 'pages')
ASSETS_DIR = os.path.join(DSS_APP_DIR, 'assets')

app = dash.Dash(__name__, use_pages=True, pages_folder=PAGES_DIR, assets_folder = ASSETS_DIR, routes_pathname_prefix=ROUTE_PREFIX)

app.title = 'Mars Snacking App Portal'
app.layout = app_layout
app.config.suppress_callback_exceptions = True

register_appshell_callbacks(app)
catalog_callbacks(app)
apps_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=False, port=8051, host='0.0.0.0', threaded=True)