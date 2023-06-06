from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior

kv_asset_detail = """
<AssetDetailScreen>:
    name: 'asset_detail'
    BoxLayout:
        orientation: 'vertical'
        MDLabel:
            id: asset_name
            font_style: 'H5'
        MDLabel:
            id: asset_description
            font_style: 'Body1'
        FitImage:
            id: asset_image
"""

Builder.load_string(kv_asset_detail)


class AssetCard(ButtonBehavior, MDCard):
    asset = ObjectProperty(None)

    def __init__(self, asset, **kwargs):
        super().__init__(**kwargs)
        self.asset = asset
        # Add your other initialization code here

    def on_release(self):
        print("AssetCard clicked!")
        # Navigate to the asset detail screen when the card is clicked
        sm = App.get_running_app().root
        detail_screen = sm.get_screen('asset_detail')
        detail_screen.asset = self.asset
        sm.current = 'asset_detail'


class AssetDetailScreen(Screen):
    asset = ObjectProperty(None)

    def on_pre_enter(self, *args):
        # Update the UI with the asset data when the screen is about to be shown
        self.ids.asset_name.text = self.asset.name
        self.ids.asset_description.text = self.asset.description
        self.ids.asset_image.source = self.asset.image_path
        # Update other UI elements with asset data as needed
