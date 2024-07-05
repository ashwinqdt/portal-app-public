from portal_app.pages.home.utils import *
from portal_app.utils.config import *
from portal_app.utils.constants import *

ic = InputComponent()
ui = UIComponent()


def delete_app_popup():
    header = dmc.Title('Delete App', order=4)

    header_icon = DashIconify(icon='mingcute:delete-line', inline=True
                              )

    header_div = dmc.Group(children=[header_icon, header],
                           align='center',
                           spacing=8
                           )

    confirm_btn = dmc.Button(
        children='Delete',
        id='confirm_delete_app',
        disabled=False,
        n_clicks=0,
        size="sm",
        leftIcon=DashIconify(icon='material-symbols:check')
    )

    cancel_btn = dmc.Button(
        children='Cancel',
        id='cancel_delete_app',
        disabled=False,
        n_clicks=0,
        size="sm",
        leftIcon=DashIconify(icon='material-symbols:cancel-outline'),
        style=dict(backgroundColor="transparent", color='var(--topHover)',
                   borderColor="grey")
    )
    confirm_msg = dmc.Text('Are you sure you want to delete the selected apps?',
                           size='1.1rem', weight=550
                           )

    warning_msg = dmc.Text('Warning: this action cant be undone',
                           size='1rem', weight=550, color='var(--default_red)'
                           )

    main_div = dmc.Stack([confirm_msg, warning_msg], spacing=15, align='center',
                         style=dict(paddingTop='1rem'))
    action_buttons = dmc.Group([confirm_btn, cancel_btn], position='center',
                               style=dict(paddingRight='0.5rem', paddingTop='1.5rem'))
    popup_dummy_output1 = dcc.Store(id='delete_app_success', data=False)
    popup_content = html.Div([main_div, action_buttons, popup_dummy_output1])

    popup_content = dmc.LoadingOverlay(popup_content,
                                       loaderProps={"color": "blue", "size": "lg", "variant": "dots"},
                                       overlayOpacity=0.6
                                       )

    modal = dmc.Modal(
        title=header_div,
        id="delete_app_popup",
        centered=True,
        fullScreen=False,
        zIndex=10000,
        children=popup_content,
        opened=False,
        size='lg'
    )

    return modal


def add_app_popup():
    # Header Section
    header = dmc.Title('Add App', order=4)

    header_icon = DashIconify(icon='mingcute:add-line', inline=True)

    header_div = dmc.Group(children=[header_icon, header],
                           align='center',
                           spacing=8
                           )
    # Input Section
    add_category_toggle = ic.segmented(id='add-cat-toggle',
                                       default_value='existing_category',
                                       options=[{'label': 'Select Category', 'value': 'existing_category', 'icon': ''},
                                                {'label': 'Add Category', 'value': 'new_category',
                                                 'icon': 'antd-plus'}])

    exist_category = dmc.Select(id='existing-category-select', data=categories, value=None,
                                label='Category',
                                placeholder='Select category from available options',
                                clearable=True,
                                style={'display': ''},
                                required=True)

    new_category = dmc.TextInput(id='new-category-input',
                                 label='Category',
                                 placeholder='Enter name of the new category...',
                                 style={'display': 'none'},
                                 required=True)

    input_app_name = dmc.TextInput(id='add-app_name',
                                   label='App Name',
                                   placeholder='Enter a unique name to identify your app...',
                                   required=True)

    input_app_url = dmc.TextInput(id='add-app_url',
                                  label='App Path',
                                  placeholder='Enter a path of your app...')

    input_app_desc = dmc.Textarea(id='add-app_desc',
                                  label='App Description',
                                  placeholder='Enter a description of your app...')

    input_section = dmc.Stack(
        [add_category_toggle, exist_category, new_category, input_app_name, input_app_url, input_app_desc],
        spacing=15,
        style=dict(paddingTop='1rem')
    )

    # Action Section
    confirm_btn = dmc.Button(
        children='Add',
        id='confirm_add_app',
        disabled=True,
        n_clicks=0,
        size="sm",
        leftIcon=DashIconify(icon='material-symbols:check')
    )

    cancel_btn = dmc.Button(
        children='Cancel',
        id='cancel_add_app',
        disabled=False,
        n_clicks=0,
        size="sm",
        leftIcon=DashIconify(icon='material-symbols:cancel-outline'),
        style=dict(backgroundColor="transparent", color='var(--topHover)',
                   borderColor="grey")
    )

    action_buttons = dmc.Group([confirm_btn, cancel_btn], position='center',
                               style=dict(paddingRight='0.5rem', paddingTop='1.5rem'))

    # PopUp Content
    popup_store_action = dcc.Store(id='add_app_success', data=False)
    popup_content = html.Div([input_section, action_buttons, popup_store_action])

    popup_content = dmc.LoadingOverlay(popup_content,
                                       loaderProps={"color": "blue", "size": "lg", "variant": "dots"},
                                       overlayOpacity=0.6
                                       )

    modal = dmc.Modal(
        title=header_div,
        id="add_app_popup",
        centered=True,
        fullScreen=False,
        zIndex=10000,
        children=popup_content,
        opened=False,
        size='lg'
    )

    return modal
