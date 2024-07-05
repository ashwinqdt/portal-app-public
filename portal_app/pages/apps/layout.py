from .utils import *
from portal_app.utils.config import *

ui = UIComponent()
ic = InputComponent()

page_header_container = fac.AntdText("My Apps", className='title')

apps_table = dag.AgGrid(
    id="apps-table",
    #rowData=stored_data,
    columnDefs=columnDefs,
    columnSize="responsiveSizeToFit",
    defaultColDef=defaultColDef,
    dashGridOptions=dashGridOptions,
    enableEnterpriseModules=True,
    style=dict(height='100%')
)

apps_table_div = html.Div(apps_table, style=dict(height='60vh', width='100%'))

add_btn = ui.button_dmc("Add App", id='add-app-btn', className='add_app_icon', icon="material-symbols:add",
                        style={'backgroundColor': 'var(--add_button)'})
delete_btn = ui.button_dmc("Delete App", id='delete-app-btn', className='delete_app_icon',
                           icon="material-symbols:remove", style={'backgroundColor': 'var(--delete_button'})

apps_delete_alert = dmc.Alert(
    children='Please select one or more apps before pressing on delete button',
    title="No Apps Selected!",
    id="no_apps_selected_alert",
    color="red",
    withCloseButton=True,
    duration=5000,
    hide=True
)

card_content = fac.AntdCard(
    headStyle={"display": "none"},
    children=[
        apps_table_div,
        dmc.Group([
            add_btn,
            delete_btn,
            apps_delete_alert
        ], style={'padding-top': '20px'})
    ],
    className='antd-tile',
    style={'width': '95%'}
)

layout = html.Div([
    dmc.Space(h=20),
    html.Div(page_header_container),
    dmc.Space(h=20),
    dmc.Center(card_content),
    html.Div(id='page-content'),
    delete_app_popup(),
    add_app_popup(),
    html.Div(id='apps_notifications')
])
