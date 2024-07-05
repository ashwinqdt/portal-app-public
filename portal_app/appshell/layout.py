from portal_app.utils.common import *
from portal_app.utils.component_utils import *
from portal_app.utils.config import *

i = InputComponent()
ui = UIComponent()

header_title = ui.header_title(bigTitle='Mars Snacking App Hub', smallTitle='MSAH', version=VERSION,
                               img_path='assets/logo.png', img_height=None, theme_toggle=True,
                               secondary_logo='assets/light-theme-logo.png')

header_group = ui.group([header_title], position='apart')

app_layout = html.Div(
    [
        ui.appshell_layout(header=header_group, nav_icons=NAV_ICONS, horizontal=False),
        # additional_logo,
        fuc.FefferyKeyPress(
            id='fs-key-press',
            keys='ctrl.s',
            pressedCounts=0
        ),
        dcc.Store(id='theme-store', data=DEFAULT_THEME),
        dcc.Store(id='theme-empty', data=''),
        dcc.Store(id="stored_apps_data", data=stored_data, storage_type='session'),
        dcc.Store(id='stored-star-color', data=star_colors_mapping, storage_type='session'),
        dcc.Store(id='stored-categories', data=categories, storage_type='session')
    ],
    style={'height': '100vh'}
)

app_layout = dmc.MantineProvider(
    id='mantine_provider',
    theme={'colorScheme': DEFAULT_THEME},
    inherit=True,
    withGlobalStyles=True,
    withNormalizeCSS=True,
    children=html.Div(dmc.NotificationsProvider(app_layout)))
