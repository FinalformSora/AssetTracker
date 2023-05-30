from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import RoundedRectangle, Color
from kivy.properties import ListProperty, ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton, MDFloatingActionButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from create_asset import CreateAssetPopup
from search_screen import SearchScreen
from asset_database import AssetDatabase
from kivymd.uix.list import MDList, ThreeLineListItem, ThreeLineIconListItem
from kivy.lang import Builder
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.theming import ThemableBehavior
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from create_asset import CreateAssetPopup

KV_func = '''
<MainScreen>:
    MDTopAppBar:
        id: titleBox
        title: "Lucca's A Scrub"
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
    MDRectangleFlatButton:
        text: "Hello, World"
        pos_hint: {"center_x": .5, "center_y": .5}
    MDBoxLayout:
        id: addAsset
        spacing: "56dp"
        adaptive_size: True
        pos_hint: {"center_x": .92, "center_y": .1}
'''
Builder.load_string(KV_func)


class MainScreen(Screen):
    def on_kv_post(self, base_widget):
        self.ids.addAsset.add_widget(
            MDFloatingActionButton(
                icon="plus",
                on_release=lambda x: setattr(self.manager, 'current', 'create_asset')
            )
        )


class ContentNavigationDrawer(BoxLayout):
    pass


class NewMain(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"

        sm = ScreenManager()
        main_screen = MainScreen(name='main')
        create_asset_screen = CreateAssetPopup(name='create_asset')
        sm.add_widget(main_screen)
        sm.add_widget(create_asset_screen)
        return sm


class CustomOverFlowMenu(MDDropdownMenu):
    # In this class you can set custom properties for the overflow menu.
    pass


if __name__ == '__main__':
    NewMain().run()