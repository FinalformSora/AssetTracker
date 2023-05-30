from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivymd.uix.screen import MDScreen

from asset import Asset
from asset_database import AssetDatabase  # import the instance directly


class CreateAssetPopup(MDScreen):
    def __init__(self, **kwargs):
        super(CreateAssetPopup, self).__init__(**kwargs)
        self.title = "Create a new Asset"
        self.size_hint = (0.8, 0.8)

        self.layout = BoxLayout(orientation='vertical')

        # Define text inputs
        self.name_input = TextInput(hint_text="Name")
        self.tags_input = TextInput(hint_text="Tags (separated by commas)")  # updated this line
        self.description_input = TextInput(hint_text="Description")
        self.link_input = TextInput(hint_text="Link")
        self.image_path_input = TextInput(hint_text="Image Path")
        self.location_input = TextInput(hint_text="Location")

        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.tags_input)
        self.layout.add_widget(self.description_input)
        self.layout.add_widget(self.link_input)
        self.layout.add_widget(self.image_path_input)
        self.layout.add_widget(self.location_input)

        self.submit_button = Button(text="Submit")
        self.submit_button.bind(on_release=self.submit_asset)
        self.layout.add_widget(self.submit_button)

        self.add_widget(self.layout)

    def submit_asset(self, *args):
        name = self.name_input.text
        tags = [tag.strip() for tag in self.tags_input.text.split(',')]
        description = self.description_input.text
        link = self.link_input.text
        image_path = self.image_path_input.text
        location = self.location_input.text

        new_asset = Asset(name, tags, description, link, image_path, location)
        db = AssetDatabase()  # Create an instance of AssetDatabase
        db.add_asset(new_asset)  # Call add_asset on the instance

        self.dismiss()  # Close the popup


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