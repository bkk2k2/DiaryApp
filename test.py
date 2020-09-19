import emoji
from kivy.app import App
from kivy.uix.label import Label

class MyApp(App):
    def build(self):
        label = Label(text=emoji.emojize(':+1:',use_aliases=True),font_size = '100')
        return label
    
if __name__ == '__main__':
    MyApp().run()