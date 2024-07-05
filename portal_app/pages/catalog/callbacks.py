from .utils import *

from dash import MATCH, ALL
from dash.exceptions import PreventUpdate

from portal_app.pages.apps.utils import *


def catalog_callbacks(app):
    # For create chips for each category in stored-categories data
    @app.callback(
        Output('chips-categories-div', 'children'),
        Input('stored-categories', 'data'),
    )
    def chips_categoties_data(stored_categories):
        print(stored_categories)
        return CheckButton(stored_categories)

    # Callback for category and app filtering
    @app.callback(
        Output("apps-cards", "children"),
        Input("categories-chips-values", "value"),
        Input("app-search-bar", "value"),
        Input('app-list-toggle', 'value'),
        State('stored-star-color', 'data'),
        State('stored_apps_data', 'data'),
        State('stored-categories', 'data'),
    )
    def show_selected_categories_apps(selected_categories, app_name, selected_tab, stored_color, stored_data,
                                      stored_category):
        stored_df = pd.DataFrame(stored_data)
        stored_dic = return_excel_as_dic(stored_df)
        apps = extract_data_by_categories(stored_dic, selected_categories)

        if app_name:
            apps = {key: value for key, value in apps.items() if
                    app_name.lower() in value['name'].lower()}

        if selected_tab == 'favorties':
            fav_apps = [k for k, v in stored_color.items() if v == 'yellow']
            apps = {k: v for k, v in apps.items() if k in fav_apps}

        tiles = return_app_cards_list(apps, stored_color, stored_category)

        if not apps:
            return search_not_found("No app sets match your search")
        return tiles

    # call for controlling star-color
    @app.callback(
        Output({'type': 'card-star', 'index': MATCH}, 'color'),
        Input({'type': 'card-star', 'index': MATCH}, 'n_clicks'),
        State({'type': 'card-star', 'index': MATCH}, 'color'),
        prevent_initial_call=True
    )
    def changing_star_color(nclick, color):
        if not nclick:
            raise PreventUpdate
        if color == 'gray':
            return 'yellow'
        else:
            return 'gray'

    # Call for storing StarColor
    @app.callback(
        Output('stored-star-color', 'data'),
        Output('stored_apps_data', 'data', allow_duplicate=True),
        Input({'type': 'card-star', 'index': ALL}, 'n_clicks'),
        State('stored-star-color', 'data'),
        State('stored_apps_data', 'data'),
        prevent_initial_call=True
    )
    def storing_star_color(click, stored_color, stored_data):
        if all(not n for n in click):
            raise PreventUpdate

        ctx = dash.callback_context
        trigger_id = ctx.triggered_id

        selected_name = trigger_id['index']

        if stored_color[selected_name] == 'gray':
            stored_color[selected_name] = 'yellow'


        else:
            stored_color[selected_name] = 'gray'

        # Update the 'star-color' in each dictionary data
        for app in stored_data:
            app['star-color'] = stored_color[app['name']]

        return stored_color, stored_data

    # Controlling select and unselect categories
    @app.callback(
        Output('categories-chips-values', 'value', allow_duplicate=True),
        Input('selectAll-button', 'n_clicks'),
        State('categories-chips-values', 'value'),
        State('stored-categories', 'data'),
        prevent_initial_call=True
    )
    def select_all_categories_fun(click, selected_cat, stored_cat):
        if len(selected_cat) == len(stored_cat):
            return []
        else:
            return stored_cat

    @app.callback(
        Output('tooltip-selectall-cat', 'label'),
        Output('selectAll-icon', 'icon'),
        Output('selectAll-button', 'className'),
        Input('categories-chips-values', 'value'),
        State('stored-categories', 'data')
    )
    def styling_select_icon(selected_cat, stored_cat):
        if len(selected_cat) == len(stored_cat):
            return 'Unselect All', 'fluent:select-all-on-16-regular', 'all-selected'
        else:
            return 'Select All', 'fluent:select-all-off-20-regular', 'all-unselected'
