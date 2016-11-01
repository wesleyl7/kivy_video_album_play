'''
Video Album UI with Video Playback 
=====================================

This example demonstrates showing video in album view and playing video on clicking
video image. You should see a transparent video playback icon on top of first video 
frame. After stopping video, it should go back to the album view.

Demo usage of:
- Screen manager and screen transition between album and full screen playback
- Video player for video playback
- Grid layout to display multiple images
'''

#--- Kivy Modules ---#
import kivy
kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.logger import Logger
        
class OverlayImage(Image):
    def __init__(self, **kwargs):
        super(OverlayImage, self).__init__(**kwargs)
        
        self.source = kwargs['image']
        self.size_hint = (1.0, 1.0)


class ImageButtonLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(ImageButtonLayout, self).__init__(**kwargs)

        self.image_path = kwargs['path']
        self.callback = kwargs['callback']
        self.index = kwargs['index']

        self.button = Button(size_hint=(1.0, 1.0), on_press=self.button_selected)
        self.button.background_normal = self.image_path
        self.add_widget(self.button)

        self.image = OverlayImage(image='./playback_icon.png')
        self.add_widget(self.image)

    def button_selected(self, instance):
        self.callback(self.index)

class ImageButtonGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(ImageButtonGridLayout, self).__init__(**kwargs)
        self.rows = 2
        self.cols = 2
        self.image_buttons = []
        self.image_files = ['./Apple.jpg', './Banana.jpg', './Cantaloupe.jpg', './Grapefruit.jpg']
        self.video_files = ['./softboy.mpg', 'softboy.mpg', 'softboy.mpg', 'softboy.mpg']
        self.image_count = len(self.image_files)

        for i in range(self.image_count):
            buttonView = ImageButtonLayout(size_hint = (0.4, 0.4), path=self.image_files[i], index=i, callback=self.media_callback)
            self.image_buttons.append(buttonView)
            self.add_widget(self.image_buttons[i])

    def media_callback(self, index):
        self.stream_name = self.video_files[index]
        self.parent.set_stream_name(self.stream_name)
        self.parent.switch_to_playback_screen()

# Declare screens
class AlbumViewScreen(Screen):
    def __init__(self, **kwargs):
        super(AlbumViewScreen, self).__init__(**kwargs)

        album_view = ImageButtonGridLayout(size=Window.size)
        self.add_widget(album_view)
        self.stream_name = './softboy.mpg'

        album_layout = ImageButtonGridLayout(size_hint=(1.0, 1.0))
        self.add_widget(album_layout)

    def set_stream_name(self, stream_name):
        self.parent.parent.screenManager.get_screen('playback_screen').setup_video_player(self.stream_name)

    def switch_to_playback_screen(self):
        self.parent.parent.screenManager.transition.direction = 'left'
        self.parent.parent.screenManager.current = 'playback_screen'
        self.parent.parent.current_screen_id = 1

class PlaybackScreen(Screen):
    def __init__(self, **kwargs):
        super(PlaybackScreen, self).__init__(**kwargs)

        self.playback_view = BoxLayout(size=Window.size, orientation='vertical')
        self.add_widget(self.playback_view)

        self.button = Button(size_hint=(1.0, 0.1), pos_hint={'x':0, 'y': 0.9}, on_press=self.stop_video_playback)
        self.button.text = 'Back'
        self.playback_view.add_widget(self.button)

    def setup_video_player(self, stream_file):
        self.player = VideoPlayer(size_hint=(1.0, 0.9), pos_hint={'x':0, 'y': 0}, source=stream_file, state='play', options={'allow_stretch': True, 'fullscreen': True})
        self.playback_view.add_widget(self.player)

    def stop_video_playback(self, instance):
        self.player.state = 'stop'
        self.playback_view.remove_widget(self.player)

        # Switch back to album view
        self.switch_to_album_screen()

    def switch_to_album_screen(self):
        Logger.info('--> Switching back to album screen')
        self.parent.parent.screenManager.transition.direction = 'left'
        self.parent.parent.screenManager.current = 'album_screen'
        self.parent.parent.current_screen_id = 0

class HomeScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        # Setup screen manager
        self.screenManager = self.ids.screenManager
        self.current_screen_id = 0 
        self.screenManager.current = 'album_screen'


class kvVideoAlbumPlayApp(App):
    def build(self):
        Window.size = (1280, 720)
        homeScreen = HomeScreen(size_hint=(1.0,1.0))
        return homeScreen

if __name__ == '__main__':
    kvVideoAlbumPlayApp().run()
