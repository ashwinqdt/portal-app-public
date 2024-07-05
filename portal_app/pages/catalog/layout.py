from .utils import *

ui = UIComponent()
ic = InputComponent()

app_list_toggle = ic.segmented(id='app-list-toggle', options=[{'label': '', 'value': 'all', 'icon': 'antd-catalog'},
                                                              {'label': '', 'value': 'favorties', 'icon': 'antd-star'}],
                               default_value='all', style={'width': '100px'})
search_bar = ic.text(id='app-search-bar', default_value=None, placeholder='Search for an app', style={'width': '250px'},
                     mode='search')
right_side_group = dmc.Group([search_bar, app_list_toggle], position='right',
                             style={'margin-bottom': '10px', 'margin-top': '0px'}, spacing=10)

check_button = dmc.Center(
    dmc.Group([
        html.Div(id='chips-categories-div', style={}, className="categories-chips-div"),
        html.Div(
            dmc.Tooltip(
                dmc.ActionIcon(DashIconify(icon="fluent:select-all-on-16-regular", width=30, id='selectAll-icon'),
                               id='selectAll-button',
                               n_clicks=0,
                               variant='subtle',
                               className="all-selected"),
                position='top',
                label='UnSelect All',
                id='tooltip-selectall-cat'
            ),
            style={'display': 'inline-block'}
        )
    ]),
    style={'margin-bottom': '20px'})

header_container = dmc.Container(
    size="lg",
    mt=10,
    children=[
        dmc.Group(
            [
                fac.AntdText("App Catalog", className='title'),
                right_side_group
            ],
            position="apart",
        ),
        # ),
    ],
)

# Top part of category and app name filters
filters_section = html.Div([
    header_container,
    check_button
],
    className="filter_sec",
)

tile_container = dmc.Container(
    size="lg",
    px=0,
    py=0,
    # my=40,
    children=[
        dmc.SimpleGrid(
            cols=3,
            # mt=100,
            breakpoints=[
                {"maxWidth": "xs", "cols": 1},
                {"maxWidth": "xl", "cols": 1},
            ],
            children="",  # initial call happen for the children in callback func.
            style={'justify-content': 'center'},
            id="apps-cards"
        ),
    ], style={'height': '100%', 'zIndex': 0, 'overlay': 'none'},
    className="content"
)

layout = html.Div(
    [
        dmc.Center(html.Div([filters_section, tile_container]), style={'padding': '10px'}),
        html.Div(id='page-content', style={'padding': '10px'}),
    ],
)
