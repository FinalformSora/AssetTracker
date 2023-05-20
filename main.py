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
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from create_asset import CreateAssetPopup
from search_screen import SearchScreen
from asset_database import AssetDatabase
from kivymd.uix.list import MDList, ThreeLineListItem, ThreeLineIconListItem
from kivy.lang import Builder
from kivymd.uix.navigationdrawer import MDNavigationDrawer

Window.size = (300,500)

navigation_helper = """
Screen:
    NavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: 'vertical'
                    MDToolbar:
                        title: 'Demo Application'
                        left_action_items: [["menu", lambda x: nav_drawer.toggle_nav_drawer()]]
                        elevation:5

                    Widget:

        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                orientation: 'vertical'
                padding: "8dp"
                spacing: "8dp"

                Image:
                    id: avatar
                    size_hint: (1,1)
                    source: "CodingProphet.png"

                MDLabel:
                    text: "Attreya"
                    font_style: "Subtitle1"
                    size_hint_y: None
                    height: self.texture_size[1]

                MDLabel:
                    text: "attreya01@gmail.com"
                    size_hint_y: None
                    font_style: "Caption"
                    height: self.texture_size[1]

                ScrollView:

                    DrawerList:
                        id: md_list
                        
                        MDList:
                            OneLineIconListItem:
                                text: "Profile"
                            
                                IconLeftWidget:
                                    icon: "face-profile"
                                    
                           
                                    
                            OneLineIconListItem:
                                text: "Upload"
                            
                                IconLeftWidget:
                                    icon: "upload"
                                    
                           
                            OneLineIconListItem:
                                text: "Logout"
                            
                                IconLeftWidget:
                                    icon: "logout"
                                    
                           
                                
                            
                            

"""



class ColoredBoxLayout(BoxLayout):
    box_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=self.box_color)
            self.roundedrectangle = RoundedRectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.roundedrectangle.pos = instance.pos
        self.roundedrectangle.size = instance.size


class StartScreen(MDScreen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.title_label = MDLabel(text="Welcome to the Asset Tracker!", size_hint=(1, 0.6))
        self.layout.add_widget(self.title_label)
        self.start_button = MDRectangleFlatButton(text="Start", size_hint=(1, 0.4))
        self.start_button.bind(on_release=self.switch_to_main)
        self.layout.add_widget(self.start_button)
        self.add_widget(self.layout)

    def switch_to_main(self, *args):
        self.manager.current = 'main_screen'


class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.menu_pressed = False
        self.layout = BoxLayout(orientation='vertical')  # Changed from FloatLayout to BoxLayout

        self.menu_button = MDFlatButton(text="UwU", size_hint=(.1, .1))
        self.layout.add_widget(self.menu_button)
        self.menu_button.bind(on_release=self.toggle_menu)

        self.button_layout = BoxLayout(orientation='horizontal', size_hint=(1, .1)) # Container for buttons
        self.layout.add_widget(self.button_layout)

        self.create_asset_button = MDRectangleFlatButton(text="Create Asset", size_hint=(.5, 1))  # size_hint_y set to 1
        self.create_asset_button.bind(on_release=self.open_create_asset_popup)
        self.button_layout.add_widget(self.create_asset_button)

        self.search_button = MDRectangleFlatButton(text='Search', size_hint=(.5, 1))  # size_hint_y set to 1
        self.search_button.bind(on_release=self.switch_to_search)
        self.button_layout.add_widget(self.search_button)

        self.assets_layout = BoxLayout(orientation='vertical')  # size_hint_y set to .8
        self.layout.add_widget(self.assets_layout)

        self.add_widget(self.layout)
        self.load_latest_assets()


    def toggle_menu(self, instance):
        if not self.menu_pressed:  # If the UwU button has not been pressed yet
            print("UwU Unpressed")
            self.menu_pressed = True
            self.create_asset_button.md_bg_color = [0.5, 0.5, 0.5, 1]  # Darken the color
            self.search_button.md_bg_color = [0.5, 0.5, 0.5, 1]  # Darken the color
        else:  # If the UwU button has been pressed
            print("UwU Pressed")
            self.menu_pressed = False
            self.create_asset_button.md_bg_color = [1, 1, 1, 1]  # Reset the color
            self.search_button.md_bg_color = [1, 1, 1, 1]  # Reset the color

    def switch_to_search(self, *args):
        self.manager.current = 'search_screen'

    def open_create_asset_popup(self, *args):
        CreateAssetPopup().open()

    def load_latest_assets(self):
        db = AssetDatabase()
        latest_assets = db.get_latest_assets()
        asset_list = MDList()

        for asset in latest_assets:
            print(asset)
            item = ThreeLineListItem(text=asset['name'],
                                     secondary_text=', '.join(asset['tags']),  # Convert list of tags to string
                                     tertiary_text=asset['description'])
            asset_list.add_widget(item)

        padding_box = BoxLayout(padding=[0, 10, 0, 0])  # Create a box layout with padding
        padding_box.add_widget(asset_list)  # Add the asset list to the box layout

        # Create a ScrollView in case the list is larger than the screen
        assets_scroll_view = ScrollView()
        padding_box.size_hint_y = '.9'
        padding_box.height = '1'
        assets_scroll_view.add_widget(padding_box)  # Add the box layout to the scroll view
        self.layout.add_widget(assets_scroll_view)

    def toggle_nav_drawer(self):
        self.ids.nav_drawer.toggle_nav_drawer()

    def build(selfself):
        nav_drawer = MDNavigationDrawer()
        return nav_drawer


class AssetTrackerApp(MDApp):
    def build(self):
        sm = ScreenManager()

        start_screen = StartScreen(name='start_screen')
        main_screen = MainScreen(name='main_screen')
        search_screen = SearchScreen(name='search_screen')

        sm.add_widget(start_screen)
        sm.add_widget(main_screen)
        sm.add_widget(search_screen)

        return sm


class NewHeader(MDApp):
    def build(self):
        screen = Builder.load_string(navigation_helper)
        return screen


class MainApp(MDApp):
    def build(self):
        nav_drawer = MDNavigationDrawer()

        # Then add items to your navigation drawer here

        return nav_drawer

MainApp().run()

# if __name__ == '__main__':
#     AssetTrackerApp().run()
