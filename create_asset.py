from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from asset import Asset
from asset_database import AssetDatabase
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivymd.uix.button import MDRaisedButton


KV_Create_Asset = '''
<CreateAssetScreen>:

    MDBoxLayout:
        orientation: "vertical"
        spacing: "20dp"
        adaptive_height: True
        size_hint_x: .8
        pos_hint: {"center_x": .5, "center_y": .5}
        
        MDTopAppBar:
            id: titleBox
            title: "Create Asset"
            pos_hint: {"top": 1}
            left_action_items: 
                [['arrow-left', root.go_to_main_screen]]
                
        MDTextField:
            id: name
            hint_text: "Enter the name of the asset"
            helper_text: "Enter a valid name"

        MDTextField:
            id: tags
            hint_text: "Enter the tags of the asset"
            helper_text: "Enter a valid tags"

        MDTextField:
            id: description
            hint_text: "Enter the description of the asset"
            helper_text: "Enter a valid description"

        MDTextField:
            id: link
            hint_text: "Enter the link of the asset"
            helper_text: "Enter a valid link"

        MDRaisedButton:
            id: image_button
            text: "Upload Image"
            on_release: root.open_file_chooser()
            
        MDLabel:
            id: image_label
            text: ""

        MDTextField:
            id: location
            hint_text: "Name of the location where to Download"
            helper_text: "Name of the location where to Download"

        MDRectangleFlatButton:
            text: "Submit"
            on_release: root.submit_asset()
'''

Builder.load_string(KV_Create_Asset)


class CreateAssetScreen(MDScreen):
    name = ObjectProperty(None)
    tags = ObjectProperty(None)
    description = ObjectProperty(None)
    link = ObjectProperty(None)
    image_path = ObjectProperty(None)  # This is the correct property name for storing the image file path
    location = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CreateAssetScreen, self).__init__(**kwargs)

    def submit_asset(self):
        name = self.ids.name.text
        tags = [tag.strip() for tag in self.ids.tags.text.split(',')]
        description = self.ids.description.text
        link = self.ids.link.text
        image_path = self.image_path  # Correct this
        location = self.ids.location.text

        new_asset = Asset(name, tags, description, link, image_path, location)  # Assuming your Asset constructor accepts these parameters
        db = AssetDatabase()
        db.add_asset(new_asset)

        self.manager.current = 'main'  # Go back to main screen

    def open_file_chooser(self):
        filechooser = FileChooserIconView(multiselect=False, dirselect=False)
        popup = Popup(title='Choose Image File', content=filechooser)
        filechooser.bind(on_submit=lambda instance, selection, _: self.set_image_path(selection, popup))
        popup.open()

    def set_image_path(self, selection, popup):
        print("Selected", selection)
        if selection:
            self.image_path = selection[0]
            self.ids.image_button.text = "Image Selected"
            self.ids.image_label.text = f"Selected Image: {self.image_path}"
            popup.dismiss()  # dismiss the popup

    def go_to_main_screen(self, *args):
        self.manager.current = 'main'  # Go back to main screen


class MainScreen(Screen):
    pass  # No extra initialization is needed here


class AssetManagerApp(App):  # The main application class
    def build(self):
        sm = ScreenManager()
        self.root = sm
        sm.add_widget(MainScreen(name='main'))  # Set the name attribute to switch between screens
        sm.add_widget(CreateAssetScreen(name='create'))
        return sm


if __name__ == "__main__":
    AssetManagerApp().run()
