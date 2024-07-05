import pandas as pd

from portal_app.utils.constants import EXCEL_FILE_DIRECTORY

app_data = pd.read_excel(EXCEL_FILE_DIRECTORY)
star_colors_mapping = app_data.set_index('name').to_dict()['star-color']
stored_data = app_data.to_dict('records')

LOCAL_DEV = True
ROUTE_PREFIX = '/portal-dash/'
VERSION = 'v0.7.1'

PAGES = {
    'Home': {
        'path': '/',
        'name': 'Home',
        'icon': 'antd-home',
    },
    'App Catalog': {
        'path': '/app-catalog',
        'name': 'App Catalog',
        'icon': 'antd-catalog',
        'description': 'A catalog of all the apps available to you'
    },
    'My Apps': {
        'path': '/my-apps',
        'name': 'My Apps',
        'icon': 'antd-cluster',
        'description': 'Add and manage your apps'
    },
    'Usage Statistics': {
        'path': '/usage-statistics',
        'name': 'Usage Statistics',
        'icon': 'antd-zoom-in',
        'description': 'View usage statistics for your apps'
    }
}

NAV_ICONS = {k: v['icon'] for k, v in PAGES.items()}


# Function for reading excel data as dictionary
def return_excel_as_dic(df):
    apps = df.set_index('name').T.to_dict('dict')
    # Add 'name' as a value in the inner-dictionary
    for k, v in apps.items():
        v['name'] = k

    return apps


APPS = return_excel_as_dic(app_data)

# extract unique categories from data
categories = sorted(list(set([v['category'] for k, v in APPS.items()])))

defaultColDef = {
    "filter": True,
    "floatingFilter": True,
    "resizable": True,
    "sortable": True,
    "editable": True,
    "minWidth": 150,
}

columnDefs = [
    {
        "headerName": "Category",  # Col. name displayed in  app
        "field": "category",
        "checkboxSelection": True,
        "rowGroup": True,
        'hide': True,
        'filter': 'agMultiColumnFilter'
    },
    {
        "headerName": "App Name",
        "field": "name",
        'filter': 'agMultiColumnFilter',
        'hide': True
    },
    {
        "headerName": "URL",
        "field": "path",
        "cellRenderer": "urlCellRenderer",
        'filter': 'agMultiColumnFilter',
    },
    {
        "headerName": "Description",
        "field": "description",
        'filter': 'agMultiColumnFilter'
    },
]

dashGridOptions = {'pagination': True,
                   "undoRedoCellEditing": True,
                   "rowDragManaged": True,
                   "animateRows": True,
                   "rowDragMultiRow": True,
                   "rowSelection": "multiple",
                   "rowDragEntireRow": True,
                   'singleClickEdit': True,
                   'enableGroupEdit': True,  ############
                   'autoGroupColumnDef': {
                       'headerName': 'App Name',
                       'field': 'name',
                       'filter': 'agMultiColumnFilter',
                       "cellRenderer": 'agGroupCellRenderer',  #####
                       "cellRendererParams": {
                           "suppressCount": False,
                           'checkbox': True
                       },
                   },
                   "stopEditingWhenCellsLoseFocus": True,
                   'groupDefaultExpanded': -1,  # To show items in the group
                   'groupSelectsChildren': True,  # select children when parent selected
                   'suppressScrollOnNewData': True,  # To prevent top scrolling on each action

                   }

DEFAULT_THEME = 'light'
