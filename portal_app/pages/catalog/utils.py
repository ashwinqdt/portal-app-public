from portal_app.pages.home.utils import *
from portal_app.utils.config import *
from portal_app.utils.constants import *

import matplotlib.colors as mcolors
import random


def random_color_generator():
    color = random.choice(list(mcolors.CSS4_COLORS.keys()))
    return color


# Function create a specific style for each category
def category_color_styles(category_list, category):
    """
    Style categories chips based on given category.

    Args:
        category_list (list): List of the user categories.
        category (string): category name that will be styled.

    Returns:
        dict: A new dictionary containing style of the given category.
    """

    if len(category_list) > len(COLOR_LIST):
        random_color = random_color_generator()
        COLOR_LIST.append(random_color)

    category_color_dic = {category_list[i]: COLOR_LIST[i] for i in range(len(category_list))}

    chip_styles = {"label": {
        "&[data-checked][data-variant='filled']":  # Styles for selected chips
            {
                "backgroundColor": category_color_dic.get(category),
                'borderColor': '',
                'color': 'white',
                ":hover": {'filter': 'brightness(0.9)',
                           "backgroundColor": category_color_dic.get(category),
                           'color': 'white'},
            },
    },
        "checkIcon": {"color": 'white',
                      ":hover": {"color": 'white !important'},
                      }
    }

    return chip_styles


def CheckButton(cat: list):
    return dmc.ChipGroup([
        dmc.Chip(
            x,
            value=x,
            radius='md',
            size='md',
            variant='filled',
            styles=category_color_styles(cat, x),
        )
        for x in cat
    ],
        id='categories-chips-values',
        value=cat,
        multiple=True,
    )


def extract_data_by_categories(data, desired_categories):
    """
    Extracts data from the dictionary based on selected categories.

    Args:
        data (dict): The input dictionary.
        desired_categories (list): List of category names to extract.

    Returns:
        dict: A new dictionary containing data of the selected categories.
    """
    extracted_data = {}
    for key, value in data.items():
        if value['category'] in desired_categories:
            extracted_data[key] = value
    return extracted_data


def AntDTileCatalog(category, heading, description, href, stored_category, star_color=star_colors_mapping):
    category_color_dic = {stored_category[i]: COLOR_LIST[i] for i in range(len(stored_category))}
    return fac.AntdCard(
        headStyle={"display": "none"},
        title=None,
        hoverable=True,
        children=[
            dmc.SimpleGrid(
                cols=1,
                spacing=0,
                children=[
                    dmc.Group([
                        fac.AntdTag(content=category, color=category_color_dic[category]),
                        dmc.ActionIcon(DashIconify(icon="ph:star-fill", width=20),
                                       n_clicks=0,
                                       variant="subtle",
                                       color=star_color[heading],
                                       id={'type': 'card-star',
                                           'index': heading}
                                       ),
                    ],
                        position='apart',
                        style={'margin-bottom': '20px', 'width': '100%'}
                    ),

                    dcc.Link([
                        fac.AntdTitle(heading, level=4),
                        dmc.Divider(style={"width": "50px"}, size="sm", my=10),
                        fac.AntdText(description, type="secondary")],
                        href=href,
                        target="_blank")
                ],
                style={'width': '100%'}
            ),
        ],
        className='antd-tile',
        style={'height': '100%',
               'width': '350px',
               'align': 'center',
               'position': 'center',
               'flexDirection': 'column', }
    )


def create_tile_content_catalog(content: dict):
    card_content = [(v['category'], v['name'], v['description'], v['path']) for k, v in content.items() if
                    'description' in v]
    return card_content


def return_app_cards_list(app_dic, stored_color, stored_category):
    card_content = create_tile_content_catalog(app_dic)

    tiles = [
        AntDTileCatalog(category, heading, description, href, stored_category, star_color=stored_color)
        # Tile(icon, heading, description, href)

        for category, heading, description, href in card_content
    ]

    return tiles


def search_not_found(text):
    message = html.Div([  # DashIconify(icon="nonicons:not-found-16"),
        text],
        style={'padding-top': '20px', 'font-size': 'larger'}
    )
    return message
