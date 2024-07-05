import dash
from dash import clientside_callback, ClientsideFunction
from .utils import *


def apps_callbacks(app):
    # Call for updating data of ag-grid table directly
    @app.callback(
        Output('apps-table', 'rowData'),
        Input('stored_apps_data', 'data')
    )
    def loading_table_data(data):
        return data

    # Call style ag-grid table on light and dark mode
    app.clientside_callback(
        ClientsideFunction(namespace='clientside',
                           function_name='table_style'),
        Output('apps-table', 'className'),
        Input('theme-store', 'data')
    )

    @app.callback(
        Output('stored_apps_data', 'data', allow_duplicate=True),
        Output('stored-star-color', 'data', allow_duplicate=True),
        Output('stored-categories', 'data', allow_duplicate=True),
        Input('apps-table', 'cellValueChanged'),
        State('apps-table', 'rowData'),
        State('stored-categories', 'data'),
        prevent_initial_call=True
    )
    def storing_edit_tabledata(cell_changed, tabledata, stored_cat):
        print('Cell Changed', cell_changed)

        if cell_changed:
            if 'row-group' in cell_changed['rowId']:  # Check that changed happened in group cell
                old_value = cell_changed['oldValue']
                new_value = cell_changed['data']['name']
                for row in tabledata:
                    if row['category'] == old_value:
                        row['category'] = new_value

                stored_cat = [new_value if cat == old_value else cat for cat in stored_cat]

            updated_star_color = pd.DataFrame(tabledata).set_index('name').to_dict()['star-color']
            return tabledata, updated_star_color, stored_cat
        else:
            return dash.no_update, dash.no_update, dash.no_update

    # Controlling open and close Delete PopUp screen
    @app.callback(
        [Output('delete_app_popup', 'opened'),
         Output('no_apps_selected_alert', 'hide')],
        [Input('delete-app-btn', 'n_clicks'),
         Input('cancel_delete_app', 'n_clicks')],
        State('apps-table', 'selectedRows'),
        prevent_initial_call=True
    )
    def delete_apps_popup(dlt_click, cancel_clicks, selected_rows):
        if dlt_click == 0 and cancel_clicks == 0:
            raise PreventUpdate

        if not selected_rows:
            return dash.no_update, False

        clicked_btn = ctx.triggered_id

        if clicked_btn == 'delete-app-btn':
            return True, True

        elif clicked_btn == 'cancel_delete_app':
            return False, dash.no_update

    # Delete selected app and trigger a flag to show notification
    @app.callback(
        [Output('apps-table', 'deleteSelectedRows'),
         Output('delete_app_success', 'data')],
        Input('confirm_delete_app', 'n_clicks'),
        State('delete_app_success', 'data'),
        prevent_initial_call=True
    )
    def confirm_delete_apps(confirm_clicks, delete_success_trigger):
        if not confirm_clicks:
            raise PreventUpdate

        return True, not delete_success_trigger

    # Store data after deleting and show success notification for deleting
    @app.callback(
        [Output('apps_notifications', 'children'),
         Output('delete_app_popup', 'opened', allow_duplicate=True),
         Output('stored_apps_data', 'data', allow_duplicate=True),
         Output('delete_app_success', 'data', allow_duplicate=True)
         ],
        Input('delete_app_success', 'data'),
        State('apps-table', 'rowData'),
        prevent_initial_call=True
    )
    def table_action_success(delete_success_trigger, tabledata):
        if delete_success_trigger:
            table_action_completed = dmc.Notification(
                id="apps_table_notification",
                title="Selected Apps were Deleted Successfully",
                message="Data is updated..",
                color="green",
                action="show",
                autoClose=3000,
                icon=DashIconify(icon="akar-icons:circle-check"),
            )
            return table_action_completed, False, tabledata, False

        else:
            raise PreventUpdate

    # Controlling open and close ADD PopUp screen
    @app.callback(
        Output('add_app_popup', 'opened'),
        Output('existing-category-select', 'data', allow_duplicate=True),
        [Input('add-app-btn', 'n_clicks'),
         Input('cancel_add_app', 'n_clicks'),
         State('stored-categories', 'data')],
        prevent_initial_call=True
    )
    def add_apps_popup(add_click, cancel_clicks, stored_cat):
        if add_click == 0 and cancel_clicks == 0:
            raise PreventUpdate

        clicked_btn = ctx.triggered_id

        if clicked_btn == 'add-app-btn':
            return True,  stored_cat

        elif clicked_btn == 'cancel_add_app':
            return False, dash.no_update

    # Toggling between add exist category or add new
    @app.callback(
        [Output('existing-category-select', 'style'),
         Output('new-category-input', 'style'),
         Output('confirm_add_app', 'disabled')],

        [Input('add-cat-toggle', 'value'),
         Input('existing-category-select', 'value'),
         Input('new-category-input', 'value'),
         Input('add-app_name', 'value')],
        prevent_initial_call=True
    )
    def select_category_input(select_value, category_dropdown, add_category, add_app):
        if select_value == 'existing_category':
            if not category_dropdown or not add_app:
                return {'display': ''}, {'display': 'none'}, True
            return {'display': ''}, {'display': 'none'}, False

        elif select_value == 'new_category':
            if not add_category or not add_app:
                return {'display': 'none'}, {'display': ''}, True
            return {'display': 'none'}, {'display': ''}, False

    # show success notification for adding app
    @app.callback(
        Output('apps_notifications', 'children', allow_duplicate=True),
        Output('add_app_success', 'data', allow_duplicate=True),
        Input('add_app_success', 'data'),
        prevent_initial_call=True
    )
    def table_action_success(add_success_trigger):
        if add_success_trigger:
            table_action_completed = dmc.Notification(
                id="apps_table_notification",
                title="New Apps were Added Successfully",
                message="Data is updated..",
                color="green",
                action="show",
                autoClose=3000,
                icon=DashIconify(icon="akar-icons:circle-check"),
            )
            return table_action_completed, False

        else:
            raise PreventUpdate

    @app.callback(
        [Output('add_app_success', 'data'),
         Output('add_app_popup', 'opened', allow_duplicate=True),
         Output('stored_apps_data', 'data', allow_duplicate=True),
         Output('stored-star-color', 'data', allow_duplicate=True),
         Output('existing-category-select', 'value'),
         Output('new-category-input', 'value'),
         Output('add-app_name', 'value'),
         Output('add-app_url', 'value'),
         Output('add-app_desc', 'value'),
         Output('stored-categories', 'data'),
         ],
        [Input('confirm_add_app', 'n_clicks'),
         State('add_app_success', 'data'),
         State('existing-category-select', 'value'),
         State('new-category-input', 'value'),
         State('add-app_name', 'value'),
         State('add-app_url', 'value'),
         State('add-app_desc', 'value'),
         State('stored_apps_data', 'data'),
         State('stored-categories', 'data'),
         State('add-cat-toggle', 'value')],
        prevent_initial_call=True
    )
    def store_adding_apps(click, add_success_trigger, chosen_category, new_category, appname, appurl, appdesc, data,
                          stored_cat, toggle_category_add):
        if not click:
            raise PreventUpdate

        new_app = {
            "category": "",
            "name": appname,
            "path": appurl,
            "description": appdesc,
            "star-color": ["gray"]
        }

        if toggle_category_add == 'existing_category':
            new_app['category'] = chosen_category

        else:
            new_app['category'] = new_category
            if new_category not in stored_cat:
                stored_cat.append(new_category)

        updated_table_data = pd.concat([pd.DataFrame(data), pd.DataFrame(new_app)])
        updated_star_color = updated_table_data.set_index('name').to_dict()['star-color']

        return (not add_success_trigger,
                False,
                updated_table_data.to_dict('records'),
                updated_star_color,
                None, None, None, None, None,
                stored_cat)
