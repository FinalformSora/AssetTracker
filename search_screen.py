from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView  # new import

from asset_database import AssetDatabase


class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical')

        self.search_input = TextInput(hint_text="Search")
        self.layout.add_widget(self.search_input)

        self.search_button = Button(text="Search")
        self.search_button.bind(on_release=self.search_assets)
        self.layout.add_widget(self.search_button)

        # create a label to display results inside a ScrollView
        self.result_label = Label(size_hint_y=None)  # set size_hint_y to None so it can scroll
        self.result_scroll = ScrollView()  # create the ScrollView
        self.result_scroll.add_widget(self.result_label)  # add the label to the ScrollView
        self.layout.add_widget(self.result_scroll)  # add the ScrollView to the layout

        self.add_widget(self.layout)

    def search_assets(self, *args):
        db = AssetDatabase()
        results = db.search_assets(self.search_input.text)
        db.close()

        # create a string from the results and update the result_label text
        result_text = '\n'.join([str(result) for result in results])
        self.result_label.text = result_text
        print(result_text)
        # update the height of the label to be able to scroll
        self.result_label.height = max(self.result_label.texture_size[1], self.result_scroll.height)
