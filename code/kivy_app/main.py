from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

import random

from kivy.uix.videoplayer import VideoPlayer

from sql.queries import sql_execute


class IslandApp(App):
    def build(self):
        self.is_video = False
        main_layout = BoxLayout(padding=10, orientation='vertical')
        self.img = Image(source='../data/app_layouts/photos/dark_hood.jpg', size_hint=(1, 1),
                     pos_hint={ 'top':1},)
        light_blue = [137 / 255, 250 / 255, 248 / 255, 1]

        black = (0, 0, 0, 1)
        # inner_layout1 = CategoryLayout()
        # inner_layout2 = CategoryLayout()
        inner_layout1 = BoxLayout( orientation='horizontal',size_hint=(1, 0.1))

        inner_layout2 = BoxLayout( orientation='horizontal', size_hint=(1, 0.1))
        with inner_layout1.canvas.before:
            Color(*light_blue)  # RGBA color values (blue)
            # print(inner_layout1.center_x)
            self.rect = Rectangle(size=(Window.size[0], Window.size[1]*0.3), pos=inner_layout1.pos)


        btn_arms = Button(text="Arms", background_color=black, pos_hint={'center_x': 0.5, 'center_y': 0.5,},
                          size_hint=(0.9, 0.9))
        btn_arms.bind(on_press=self.on_press_button)
        inner_layout1.add_widget(btn_arms)

        btn_legs = Button(text="Legs", background_color=black, pos_hint={'center_x': 0.5, 'center_y': 0.5},
                          size_hint=(0.9, 0.9))
        btn_legs.bind(on_press=self.on_press_button)
        inner_layout1.add_widget(btn_legs)

        btn_abs = Button(text="Core", background_color=black, pos_hint={'center_x': 0.5, 'center_y': 0.5},
                         size_hint=(0.9, 0.9))
        btn_abs.bind(on_press=self.on_press_button)
        inner_layout2.add_widget(btn_abs)

        btn_back = Button(text="Back", background_color=black, pos_hint={'center_x': 0.5, 'center_y': 0.5},
                          size_hint=(0.9, 0.9))
        btn_back.bind(on_press=self.on_press_button)
        inner_layout2.add_widget(btn_back)

        self.active_screen = FloatLayout(size_hint=(1, 0.7))
        self.active_screen.add_widget(self.img)

        main_layout.add_widget(self.active_screen)
        main_layout.add_widget(inner_layout1)
        main_layout.add_widget(inner_layout2)
        self.btn_start = Button(text="", background_color=black, size_hint=(1, 0.1))
        self.btn_start.bind(on_press=self.on_press_start_button)
        main_layout.add_widget(self.btn_start)

        return main_layout

    def on_press_button(self, instance):
        print('You pressed the button!')
        categories_dict = {'Arms': ['Wrist', 'Shoulders', 'Pushup', 'Push', 'Pull', 'Muscle Up', 'Triceps', 'Hspu', 'Handstand',
                               'Dips', 'Planche', 'Qdr'],
                        'Legs': ['Squat', 'Lunges', 'Calves', 'Hamstrings', 'Hipflexor', 'Hips', 'L-sit', 'Legs',
                                 ],
                        'Core': ['Abs', 'Plank', 'Chest', 'Core', 'Functional', 'Headstand', 'Locomotion', 'Strength', 'Upper Body' ],
                        'Back': ['Back', 'Inversion', 'Handstand Press', 'Lower Back', 'Mobility', 'Neck', 'Spine']}
        categories = categories_dict[instance.text]
        ex_ids = sql_execute("""SELECT ep.exercise_id FROM ex_cat_pairs ep join exercises e on ep.exercise_id = e.exercise_id
                              WHERE e.video_id is not NULL and ep.category_id IN (SELECT category_id FROM exercise_categories 
                              WHERE category_name IN :categories);""",
                    categories=categories)
        ex_ids = [ex[0] for ex in ex_ids]
        random_exercise = random.choice(ex_ids)
        print(len(ex_ids), random_exercise)

        video_name = sql_execute("""SELECT v.file_name FROM videos v join exercises e on v.video_id = e.video_id
                    WHERE e.exercise_id = :ex_id;""",
                    ex_id=random_exercise)
        if video_name:
            video_name = video_name[0][0]
        else:
            print('No video found for this category')
            return
        print(video_name)

        if self.is_video:
            print("Removing player")
            self.player.state = 'stop'
            self.active_screen.remove_widget(self.player)

            self.player = VideoPlayer(source='../data/app_videos/' + video_name, state='play',
                                      options={'eos': 'loop'}, size_hint=(1, 1), pos_hint={'top': 1}, )
            self.btn_start.text = 'End'
            self.active_screen.add_widget(self.player)
        else:
            print("Removing image")
            self.active_screen.remove_widget(self.img)
            self.player = VideoPlayer(source='../data/app_videos/' + video_name, state='play',
                                      options={'eos': 'loop'}, size_hint=(1, 1), pos_hint={'top': 1}, )
            self.btn_start.text = 'End'
            self.active_screen.add_widget(self.player)
        self.is_video = True


    def on_press_start_button(self, instance):
        if self.is_video:
            print('You pressed the start button!')
            self.btn_start.text = ''
            self.player.state = 'stop'
            self.active_screen.remove_widget(self.player)
            print('Removed player')
            self.active_screen.add_widget(self.img)
            self.is_video = False




class CategoryLayout(BoxLayout):
    pass


class BorderButton(Button):
    def __init__(self, **kwargs):
        super(BorderButton, self).__init__(**kwargs)
        with self.canvas.before:
            # Change the border color here (RGBA format)
            light_blue = [137 / 255, 250 / 255, 248 / 255, 1]
            Color(137 / 255, 250 / 255, 248 / 255, 1) # todo: pass better
            # Adjust the border size as needed
            self.border = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_border, size=self.update_border)

    def update_border(self, instance, value):
        self.border.pos = instance.pos
        self.border.size = instance.size


if __name__ == '__main__':
    app = IslandApp()
    app.run()
