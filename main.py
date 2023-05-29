from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
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
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu

# KV = '''
# #:import CustomOverFlowMenu __main__.CustomOverFlowMenu
#
#
# MDBoxLayout:
#     orientation: "vertical"
#
#     MDTopAppBar:
#         title: "MDTopAppBar"
#         use_overflow: True
#         overflow_cls: CustomOverFlowMenu()
#         right_action_items:
#             [
#             ["home", lambda x: x, "Home", "Home"],
#             ["message-star", lambda x: x, "Message star", "Message star"],
#             ["message-question", lambda x: x, "Message question", "Message question"],
#             ["message-reply", lambda x: x, "Message reply", "Message reply"],
#             ]
#
#     MDLabel:
#         text: "Content"
#         halign: "center"
# '''

KV_func = '''
MDScreen:


    MDTopAppBar:
        id: titleBox
        title: "Lucca's A Scrub"
        pos_hint: {"top": 1}
        use_overflow: 
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

    MDBoxLayout:
        id: box
        orientation: "vertical"
        spacing: "12dp"
        adaptive_height: True
        
    MDRectangleFlatButton:
        text: "Hello, World"
        pos_hint: {"center_x": .5, "center_y": .5}
'''

# class AssetTrackerApp(MDApp):
#     def build(self):
#         sm = ScreenManager()
#         main_screen = MainScreen(name='main_screen')
#         search_screen = SearchScreen(name='search_screen')
#         sm.add_widget(main_screen)
#         sm.add_widget(search_screen)
#         return sm


class ContentNavigationDrawer(BoxLayout):
    pass

# class MainScreen(MDScreen):
#     def __init__(self, **kwargs):
#         super(MainScreen, self).__init__(**kwargs)
#         self.layout = MDBoxLayout(orientation='vertical')
#
#         # # Add Floating Action Button first
#         # self.fab = MDFloatingActionButton(
#         #     icon="plus",
#         #     pos_hint={"center_x": 0.5, "center_y": 0.5},
#         #     on_release=self.on_fab_click
#         # )
#         # self.layout.add_widget(self.fab)
#
#         # Then add MDTopAppBar
#         self.top_app_bar = MDTopAppBar(
#             title="Lucca Move to Top",
#             md_bg_color="brown",
#             left_action_items=[["arrow-left", lambda x: x]],
#             right_action_items=[
#                 ["home", lambda x: print("home clicked")],
#                 ["message-star", lambda x: print("message-star clicked")],
#                 ["message-question", lambda x: print("message-question clicked")],
#                 ["message-reply", lambda x: print("message-reply clicked")]
#             ],
#             pos_hint={'top': 0},
#
#         )
#         self.layout.add_widget(self.top_app_bar)
#
#         self.add_widget(self.layout)  # Add layout to the screen
#
#     def on_fab_click(self, instance):
#         print("FAB clicked")


class NewMain(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        # Primary Palette Colors ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
        self.theme_cls.primary_palette = "Gray"
        #self.theme_cls.primary_hue = "400"  # "500"
        return Builder.load_string(KV_func)

    def on_start(self):
        for type_height in ["medium", "large", "small"]:
            self.root.ids.box.add_widget(
                MDTopAppBar(
                    type_height=type_height,
                    headline_text=f"Headline {type_height.lower()}",
                    left_action_items=[["arrow-left", lambda x: x]],
                    right_action_items=[
                        ["attachment", lambda x: x],
                        ["calendar", lambda x: x],
                        ["dots-vertical", lambda x: x],
                    ],
                    title="Title" if type_height == "small" else "",
                    anchor_title="left",
                )
            )


class CustomOverFlowMenu(MDDropdownMenu):
    # In this class you can set custom properties for the overflow menu.
    pass


# class AssetTrackerApp(MDApp):
#     def build(self):
#         sm = ScreenManager()
#         main_screen = MainScreen(name='main_screen')
#         search_screen = SearchScreen(name='search_screen')
#         sm.add_widget(main_screen)
#         sm.add_widget(search_screen)
#         return sm
#

# class Example(MDApp):
#     def build(self):
#         return Builder.load_string(KV)
#
#     def callback(self, instance_action_top_appbar_button):
#         print(instance_action_top_appbar_button)


#if __name__ == '__main__':
#MainScreenSec.run()
NewMain().run()
    #AssetTrackerApp().run()