from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivymd.uix.screen import MDScreen

from asset import Asset
from asset_database import AssetDatabase  # import the instance directly
from kivy.lang import Builder
from kivymd.uix.textfield import MDTextField

KV_Create_Asset = '''
<CreateAssetScreen>:

    MDBoxLayout:
        orientation: "vertical"
        spacing: "20dp"
        adaptive_height: True
        size_hint_x: .8
        pos_hint: {"center_x": .5, "center_y": .5}

        MDTextField:
            id: name
            hint_text: "Enter the name of the asset"
            helper_text: "Enter a valid name"
            
        MDTextField:
            id: Description
            hint_text: "Enter the description of the asset"
            helper_text: "Enter a valid description"

        MDRectangleFlatButton:
            text: "Submit"
            on_release: root.submit_asset()
'''

Builder.load_string(KV_Create_Asset)


class CreateAssetScreen(MDScreen):
    #name = ObjectProperty(None)
    #description = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CreateAssetScreen, self).__init__(**kwargs)

    def submit_asset(self):
        name = self.ids.name.text
        description = self.ids.description.text
        print(name)

        new_asset = Asset(name, tags, description, link, image_path, location)
        db = AssetDatabase()  # Create an instance of AssetDatabase
        #db.add_asset(new_asset)  # Call add_asset on the instance

        self.manager.current = 'main'  # Go back to main screen


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical')

        self.create_asset_button = Button(text="Create Asset")
        self.create_asset_button.bind(on_release=self.open_create_asset_popup)
        self.layout.add_widget(self.create_asset_button)

        self.add_widget(self.layout)

    def open_create_asset_popup(self, *args):
        CreateAssetPopup().open()