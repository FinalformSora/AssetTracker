from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.properties import ListProperty, ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import RoundedRectangle, Color

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton, MDFloatingActionButton
from kivymd.uix.fitimage import FitImage
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, ThreeLineListItem, ThreeLineIconListItem
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.fitimage import FitImage
from kivymd.theming import ThemableBehavior

# from asset_detail import AssetDetailScreen
from create_asset import CreateAssetScreen
from search_screen import SearchScreen
from asset_database import AssetDatabase

import os
from PIL import Image as PilImage
import io
import tempfile
import uuid

KV_func = '''
<MainScreen>:
    MDTopAppBar:
        id: titleBox
        title: "Jade's A Scrub"
        pos_hint: {"top": 1}
        left_action_items: 
            [['menu', lambda x: nav_drawer.set_state("open")]]
        right_action_items:
            [
            ["home", lambda x: x, "Home", "Home"],
            ["message-star", lambda x: x, "Message star", "Message star"],
            ["message-question", lambda x: x, "Message question", "Message question"],
            ["message-reply", lambda x: x, "Message reply", "Message reply"],
            ]
    MDNavigationDrawer:
        id: nav_drawer
        radius: (0, 16, 16, 0)
        ContentNavigationDrawer:  
    
    MDScrollView:
        pos_hint: {"top": .89}
        BoxLayout:  # or FloatLayout, etc...
            orientation: 'vertical'  # Important to make it vertical scroll
            size_hint_y: None
            height: self.minimum_height  # Very important for scrolling
            MDGridLayout:
                id: card_layout
                cols: 2  # Adjust this to the number of cards you want in each row.
                spacing: dp(5)  # Set spacing explicitly
                row_default_height: (self.width - 2 * dp(100)) / self.cols
                row_force_default: True
                size_hint_y: None
                height: self.minimum_height



    MDBoxLayout:
        id: addAsset
        spacing: "56dp"
        adaptive_size: True
        pos_hint: {"center_x": .92, "center_y": .1}
'''
Builder.load_string(KV_func)


# KV way MDcard with Image


class MainScreen(Screen):
    def on_kv_post(self, base_widget):
        # Plus Icon to add Assets
        self.ids.addAsset.add_widget(
            MDFloatingActionButton(
                icon="plus",
                on_release=lambda x: setattr(self.manager, 'current', 'create_asset')
            )
        )

    def on_enter(self, *args):
        # Get Recent Assets
        db = AssetDatabase()
        assets = db.get_assets()
        for asset in assets:
            asset_card = AssetCard(asset)
            self.ids.card_layout.add_widget(asset_card)


class ContentNavigationDrawer(BoxLayout):
    pass


class AssetCard(MDCard):
    def __init__(self, asset, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = None, None
        self.size = "280dp", "280dp"
        self.pos_hint = {"center_x": .5}

        # Check if the asset image file exists, if not, create a new one from BLOB data
        if os.path.isfile(asset.image_path):
            asset_image_file_path = asset.image_path
        else:
            asset_image_file_path = self.save_blob_to_file(asset.image)

        # Add asset image to the card
        asset_image = FitImage(source=asset_image_file_path, size_hint_y=.35)
        self.add_widget(asset_image)

        # Add asset information to card
        self.add_widget(MDLabel(
            text=asset.name,
            theme_text_color="Secondary",
        ))
        self.add_widget(MDLabel(
            text=asset.description,
            theme_text_color="Secondary",
        ))
        self.add_widget(MDLabel(
            text="Tags: " + ', '.join(asset.tags),
            theme_text_color="Secondary",
        ))
        self.add_widget(MDLabel(
            text="Location: " + asset.location,
            theme_text_color="Secondary",
        ))

    def save_blob_to_file(self, blob_data):
        """Save BLOB byte data as an image file in a temporary directory, return the file path."""

        # Convert bytes to PIL Image object
        pil_image = PilImage.open(io.BytesIO(blob_data))

        # Save the PIL Image object to a file in a temporary directory
        file_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4().hex}.png")
        pil_image.save(file_path)

        # Return the path to the newly created file
        return file_path


class NewMain(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"

        sm = ScreenManager()
        main_screen = MainScreen(name='main')
        create_asset_screen = CreateAssetScreen(name='create_asset')
        sm.add_widget(main_screen)
        sm.add_widget(create_asset_screen)
        #        sm.add_widget(AssetDetailScreen(name='asset_detail'))  # add this line

        return sm


class CustomOverFlowMenu(MDDropdownMenu):
    # In this class you can set custom properties for the overflow menu.
    pass


if __name__ == '__main__':
    NewMain().run()
