import os,csv
import pandas as pd
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager,Screen
from KivyCalendar import DatePicker
from kivy.properties import ListProperty
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown

kv = '''
<ColoredLabel>:
    canvas.before:
        Color:
            rgba: root.background_color
        Rectangle:
            pos: self.pos
            size: self.size
            
<Calendar>:
    GridLayout:
        cols:1
        Button:
            text:'Calendar'
            on_press: root.show_calendar()
        TextInput:
            id: ti

<DatePicker>:
    pHint: 1, 1
    '''
k1 = '''
<NoteScreen>:
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'image_1.png'
    '''
k2 = '''
<NoteScreen>:
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'image_2.png'
    '''
k3 = '''
<NoteScreen>:
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'image_3.png'
    '''

Builder.load_string(kv)

class ColoredLabel(Label):
    background_color = ListProperty((0,0,0,1))

class CustomDatePicker(DatePicker):
    def __init__(self,Calendar):
        super().__init__()
        self.calen = Calendar 

    def update_value(self, inst):
        """ Update textinput value on popup close """

        string_list = []
        for x in self.cal.active_date:
            string_list.append(str(x).zfill(2))
        self.text = "%s.%s.%s" % tuple(string_list)
        self.focus = False
        self.calen.ids.ti.text = self.text

class Calendar(BoxLayout):

    def show_calendar(self):
        datePicker = CustomDatePicker(self)
        datePicker.show_popup(1, .3)

def update(username,password):
    Data = pd.read_csv('Database.csv')
    for u in Data.Username:
        if(username==u):return False
    with open('Database.csv','a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([username,password])
    directory = username
    parent_dir = './'
    path = os.path.join(parent_dir,directory)
    os.mkdir(path)
    return True

def check(username,password):
    Data = pd.read_csv('Database.csv')
    for [u,p] in Data[['Username','Password']].to_numpy():
        if (u==username and p==password):
            return True
    return False

class NoteScreenWidget(Screen):
    def __init__(self,username,file_name):
        super().__init__()
        self.add_widget(NoteScreen(username,file_name))

class AddnewScreenWidget(Screen):
    def __init__(self,username):
        super().__init__()
        self.add_widget(AddnewScreen(username))
            
class DiaryScreenWidget(Screen):
    def __init__(self,username):
        super().__init__()
        self.add_widget(DiaryScreen(username))
        
class HomeScreenWidget(Screen):
    def __init__(self,username):
        super().__init__()
        self.add_widget(HomeScreen(username))
        
class SigninScreenWidget(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.add_widget(SigninScreen())
        
class LoginScreenWidget(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.add_widget(LoginScreen())
        
class NoteScreen(GridLayout):
    def __init__(self,username,file_name):
        super().__init__()
        self.username = username
        self.file_name = file_name
        self.file_title = file_name[18:]
        self.text_size = file_name[13:15]
        self.text_color = file_name[16]
        self.back_image = int(file_name[11])
        self.file_date = file_name[:10]
        file = open('./'+username+'/'+file_name+'.txt','r')
        
        
        self.mood = file.readline()
        self.body = file.read()
        
        self.cols = 2
        self.color_dict = {'r':(0.5,0,0,1),'g':(0,0.5,0,1),'b':(0,0,0.5,1),'C':(0,0,0,1),'w':(1,1,1,1)}
        
        self.add_widget(Label(text='Title',color=self.color_dict[self.text_color],font_size=self.text_size))
        
        self.title = Label(text=self.file_title,color=self.color_dict[self.text_color],font_size=self.text_size)
        self.add_widget(self.title)
        
        self.add_widget(Label(text='Body',color=self.color_dict[self.text_color],font_size=self.text_size))
        
        self.text = Label(text=self.body,color=self.color_dict[self.text_color],font_size=self.text_size)
        self.add_widget(self.text)
        
        self.add_widget(Label(text='Mood',color=self.color_dict[self.text_color],font_size=self.text_size))
        self.mood_text = Label(text=self.mood[:-1],color=self.color_dict[self.text_color],font_size=self.text_size)
        self.add_widget(self.mood_text)
        
        self.add_widget(Label(text='Date',color=self.color_dict[self.text_color],font_size=self.text_size))
        self.add_widget(Label(text=self.file_date,color=self.color_dict[self.text_color],font_size=self.text_size))
        
        self.delete = Button(text='Delete')
        self.add_widget(self.delete)
        self.delete.bind(on_press=self.delete_pressed) 
        
        self.back = Button(text='Back')
        self.add_widget(self.back)
        self.back.bind(on_press=self.back_pressed) 
        
    def delete_pressed(self,instance):
        os.remove('./'+self.username+'/'+self.file_name+'.txt')
        Manager.switch_to(DiaryScreenWidget(self.username))
        
    def back_pressed(self,instance):
        Manager.switch_to(DiaryScreenWidget(self.username))
        
class AddnewScreen(GridLayout):
    def __init__(self,username):
        super().__init__()
        self.username = username
        self.cols = 2
        self.color_list = ['red','green','blue','white']
        self.color_tuple_list=[(1,0,0,1),(0,1,0,1),(0,0,1,1),(1,1,1,1)]
        
        self.add_widget(Label(text='Title'))
        
        self.title = TextInput(multiline=False)
        self.add_widget(self.title)
        
        self.add_widget(Label(text='Body'))
        
        self.body = TextInput()
        self.add_widget(self.body)
        
        self.add_widget(Label(text='Date'))
        
        self.calendar = Calendar()
        self.add_widget(self.calendar)
        
        self.add_widget(Label(text='Mood'))
        
        self.good_mood_list = ['Amused','Blissful','Calm','Cheerful','Content','Energetic','Excited','Good','Happy','Joyful','Loving','Peaceful','Silly']
        self.bad_mood_list = ['Angry','Annoyed','Bad','Depressed','Envious','Frustrated','Guilty','Irritated','Rejected','Restless','Weird','Sad','Stressed']
        self.mood_list = self.good_mood_list+self.bad_mood_list
        self.mood = Button(text='Select your mood')
        self.drop = DropDown()
        for i in range(len(self.mood_list)):
            btn = Button(text=self.mood_list[i],size_hint_y = None, height = 40)
            btn.bind(on_press = lambda btn: self.drop.select(btn.text))
            self.drop.add_widget(btn)
        self.mood.bind(on_release = self.drop.open)
        self.drop.bind(on_select = lambda instance, x: setattr(self.mood, 'text', x))
        self.add_widget(self.mood)
        
        self.c = GridLayout(cols=1)
        
        self.c.add_widget(Label(text='Text Size'))
        
        self.c.drop = DropDown()
        for i in range(0,70,10):
            btn = Button(text=str(i),size_hint_y = None, height = 40)
            btn.bind(on_press = lambda btn: self.c.drop.select(btn.text))
            self.c.drop.add_widget(btn)
        self.c.text_size = Button(text='20')
        self.c.text_size.bind(on_release = self.c.drop.open)
        self.c.drop.bind(on_select = lambda instance, x: setattr(self.c.text_size, 'text', x))
        self.c.add_widget(self.c.text_size)
        
        self.c.add_widget(Label(text='Color of Text'))
        
        self.c.drop_1 = DropDown()
        for i in range(4):
            btn = Button(text=self.color_list[i],color=self.color_tuple_list[i],size_hint_y = None, height = 40)
            btn.bind(on_press = lambda btn: self.c.drop_1.select(btn.text))
            self.c.drop_1.add_widget(btn)
        self.c.text_color = Button(text='white')
        self.c.text_color.bind(on_release = self.c.drop_1.open)
        self.c.drop_1.bind(on_select = lambda instance, x: setattr(self.c.text_color, 'text', x))
        self.c.add_widget(self.c.text_color)
        
        self.add_widget(self.c)
        
        self.drop_2 = DropDown()
        for i in range(1,4):
            btn = Button(background_normal = './image_'+str(i)+'.png',size_hint_y = None, height = 100)
            btn.bind(on_press = lambda btn: self.drop_2.select(btn.background_normal))
            self.drop_2.add_widget(btn)
        self.back_image = Button(text = 'Select Background Image')
        self.back_image.bind(on_release = self.drop_2.open)
        self.drop_2.bind(on_select = lambda instance, x:setattr(self.back_image, 'background_normal', x))
        self.add_widget(self.back_image)
        
        self.done = Button(text='Done')
        self.add_widget(self.done)
        self.done.bind(on_press=self.done_pressed)
        
        self.back = Button(text='Back')
        self.add_widget(self.back)
        self.back.bind(on_press=self.back_pressed)
        
    def done_pressed(self,instance):
        self.date = self.calendar.ids.ti.text
        save_path = './'+self.username+'/'
        name = os.path.join(save_path,self.date+'_'+self.back_image.background_normal[-5]+'_'+self.c.text_size.text+'_'+self.c.text_color.text[0]+'_'+self.title.text+'.txt')
        for n in os.listdir(save_path):
            if(self.date+'_'+self.back_image.background_normal[-1]+'_'+self.c.text_size.text+'_'+self.c.text_color.text[0]+'_'+self.title.text+'.txt'==n): 
                self.title.text=''
                return False
        file = open(name,'w')
        file.writelines([self.mood.text+'\n',self.body.text])
        file.close()
        Manager.switch_to(DiaryScreenWidget(self.username))
        
    def back_pressed(self,instance):
        Manager.switch_to(DiaryScreenWidget(self.username))
    
class DiaryScreen(GridLayout):
    def __init__(self,username):
        super().__init__()
        self.username = username
        self.cols = 1
        
        self.color_dict = {'r':(1,0,0,1),'g':(0,1,0,1),'b':(0,0,1,1),'C':(0,0,0,1),'w':(1,1,1,1)}
        
        for n in os.listdir('./'+self.username+'/'):
            if(n.endswith('.txt')):
                btn = Button(text=n[:-4],color=self.color_dict[n[16]],background_normal='./image_'+str(n[11])+'.png')
                btn.bind(on_press=lambda btn:self.note_pressed(btn.text))
                self.add_widget(btn)
        
        self.add = Button(text='Add a new note')
        self.add_widget(self.add)
        self.add.bind(on_press=self.add_pressed)
        
        self.back = Button(text='Back to Home')
        self.add_widget(self.back)
        self.back.bind(on_press=self.back_pressed)
        
    def back_pressed(self,instance):
        Manager.switch_to(HomeScreenWidget(self.username))
        
    def add_pressed(self,instance):
        Manager.switch_to(AddnewScreenWidget(self.username))
        
    def note_pressed(self,title):
        if(int(title[11])==1):Builder.load_string(k1)
        if(int(title[11])==2):Builder.load_string(k2)
        if(int(title[11])==3):Builder.load_string(k3)
        Manager.switch_to(NoteScreenWidget(self.username,title))
 
       
class HomeScreen(GridLayout):
    def __init__(self,username):
        super().__init__()
        self.username = username
        self.cols = 1
        self.add_widget(Label(text='Home Screen\nWelcome '+username))
        
        self.diary = Button(text='Open Notes')
        self.add_widget(self.diary)
        self.diary.bind(on_press=self.diary_pressed)
        
        self.logout = Button(text='Log Out')
        self.add_widget(self.logout)
        self.logout.bind(on_press=self.logout_pressed)
        
    def logout_pressed(self,instance):
        Manager.switch_to(LoginScreenWidget())
        
    def diary_pressed(self,instance):
        Manager.switch_to(DiaryScreenWidget(self.username))
        
class SigninScreen(GridLayout):
    def __init__(self):
        super().__init__()
        self.cols = 2
        
        self.add_widget(Label(text='Username'))
        
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        
        self.add_widget(Label(text='Password'))
        
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)
        
        self.signin = Button(text='Sign in')
        self.add_widget(self.signin)
        self.signin.bind(on_press=self.signin_pressed)
        
        self.back = Button(text='Back')
        self.add_widget(self.back)
        self.back.bind(on_press=self.back_pressed)
        
    def signin_pressed(self,instance):
        if(update(self.username.text,self.password.text)):
            Manager.switch_to(HomeScreenWidget(self.username.text))
        else:
            self.username.text=""
            self.password.text="" 
    
    def back_pressed(self,instance):
        Manager.switch_to(LoginScreenWidget())

class LoginScreen(GridLayout):
    def __init__(self):
        super().__init__()
        self.cols = 2
        
        self.label1 = Label(text="Username")
        self.add_widget(self.label1)
        
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        
        self.add_widget(Label(text='Password'))
        
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)
        
        self.signin = Button(text='Sign in')
        self.add_widget(self.signin)
        self.signin.bind(on_press=self.signin_pressed)
        
        self.login = Button(text='Login')
        self.add_widget(self.login)
        self.login.bind(on_press=self.login_pressed)
        
    def login_pressed(self,instance):
        if(check(self.username.text,self.password.text)):
            Manager.switch_to(HomeScreenWidget(self.username.text))
        else:
            self.username.text=""
            self.password.text=""
        
    def signin_pressed(self,instance):
        Manager.switch_to(SigninScreenWidget())

Manager = ScreenManager()
Manager.add_widget(LoginScreenWidget())       

class MyApp(App):
    def build(self):
        return Manager
    
if __name__ == '__main__':
    MyApp().run()