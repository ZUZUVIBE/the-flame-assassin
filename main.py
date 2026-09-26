from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.core.audio import SoundLoader
import random
import json
import os

class FlameAssassinGame(FloatLayout):
    def __init__(self, **kwargs):
        super(FlameAssassinGame, self).__init__(**kwargs)
        
        # Load offline cache & saved data
        self.load_game_data()
        
        # Environmental & Advanced States
        self.weather_states = ["Sunny Day ☀️", "Heavy Rain 🌧️", "Midnight Ops 🌙"]
        self.current_weather = self.weather_states[0]
        self.radar_status = "Radar Active: Secure 🟢"
        self.stealth_mode = False
        self.online_friends = ["Shadow_X", "Viper_99", "BlazeQueen"]
        self.last_message = "System: Welcome to Online Network."
        self.current_achievement = "Badge: Rookie Assassin 🥉"
        self.unlocked_abilities = ["Basic Flame Strike"]
        
        # Modern-Vintage Background
        with self.canvas.before:
            Color(0.12, 0.12, 0.15, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        # Game Title
        self.title_label = Label(
            text='THE FLAME ASSASSIN [FINAL COMPLETE]',
            font_size='15sp',
            color=(1, 0.45, 0, 1),
            pos_hint={'center_x': 0.5, 'top': 0.97},
            size_hint=(1, 0.03)
        )
        self.add_widget(self.title_label)

        # Gamer ID & HUD Display
        self.id_label = Label(
            text=f'ID: {self.gamer_id} | Coins: {self.currency}🪙 | {self.current_weather}',
            font_size='11sp',
            color=(0.8, 0.8, 0.8, 1),
            pos_hint={'center_x': 0.5, 'top': 0.93},
            size_hint=(1, 0.03)
        )
        self.add_widget(self.id_label)

        # Radar, Chat & Achievements HUD
        self.radar_label = Label(
            text=f'{self.radar_status} | {self.current_achievement}',
            font_size='10sp',
            color=(0, 0.8, 1, 1),
            pos_hint={'center_x': 0.5, 'top': 0.89},
            size_hint=(1, 0.03)
        )
        self.add_widget(self.radar_label)

        # Email / Login Input
        self.email_input = TextInput(
            text=self.username,
            hint_text='Enter Email or Username',
            multiline=False,
            pos_hint={'center_x': 0.5, 'top': 0.83},
            size_hint=(0.8, 0.05)
        )
        self.add_widget(self.email_input)

        # Login Button
        self.login_btn = Button(
            text='Login ID',
            pos_hint={'center_x': 0.30, 'top': 0.76},
            size_hint=(0.35, 0.05),
            background_color=(1, 0.5, 0, 1)
        )
        self.login_btn.bind(on_press=self.handle_login)
        self.add_widget(self.login_btn)

        # Photo ID Verification Button
        self.photo_btn = Button(
            text='Verify Photo ID',
            pos_hint={'center_x': 0.70, 'top': 0.76},
            size_hint=(0.35, 0.05),
            background_color=(0, 0.4, 0.8, 1)
        )
        self.photo_btn.bind(on_press=self.handle_photo_verification)
        self.add_widget(self.photo_btn)

        # Weapon Upgrade Shop Button
        self.shop_btn = Button(
            text='Flame Shop (Upgrade: 50🪙)',
            pos_hint={'center_x': 0.5, 'top': 0.69},
            size_hint=(0.8, 0.05),
            background_color=(0.8, 0.2, 0.8, 1)
        )
        self.shop_btn.bind(on_press=self.open_upgrade_shop)
        self.add_widget(self.shop_btn)

        # Stealth Mode Button
        self.stealth_btn = Button(
            text='Toggle Stealth / Disguise Mode 👤',
            pos_hint={'center_x': 0.5, 'top': 0.62},
            size_hint=(0.8, 0.05),
            background_color=(0.2, 0.6, 0.4, 1)
        )
        self.stealth_btn.bind(on_press=self.toggle_stealth)
        self.add_widget(self.stealth_btn)

        # Online Multiplayer Drop Button
        self.multi_btn = Button(
            text='Sync Online Friends & Drop in Battlefield 🌐',
            pos_hint={'center_x': 0.5, 'top': 0.55},
            size_hint=(0.8, 0.05),
            background_color=(0.2, 0.4, 0.9, 1)
        )
        self.multi_btn.bind(on_press=self.trigger_multiplayer_drop)
        self.add_widget(self.multi_btn)

        # Love Story Choice Button
        self.story_btn = Button(
            text='Love Story Choice: [Make Choice ❤️]',
            pos_hint={'center_x': 0.5, 'top': 0.48},
            size_hint=(0.8, 0.05),
            background_color=(0.9, 0.2, 0.5, 1)
        )
        self.story_btn.bind(on_press=self.make_story_choice)
        self.add_widget(self.story_btn)

        # Main Status / Dashboard
        self.status_label = Label(
            text='Status: All Features Unlocked! Login to play.',
            font_size='11sp',
            color=(0, 1, 0.4, 1),
            pos_hint={'center_x': 0.5, 'top': 0.38},
            size_hint=(1, 0.08)
        )
        self.add_widget(self.status_label)

    def load_game_data(self):
        if os.path.exists("save_game.json"):
            try:
                with open("save_game.json", "r") as f:
                    data = json.load(f)
                    self.gamer_id = data.get("gamer_id", f"Assassin_{random.randint(1000, 9999)}")
                    self.score = data.get("score", 0)
                    self.level = data.get("level", 1)
                    self.currency = data.get("currency", 150)
                    self.username = data.get("username", "")
                    self.is_logged_in = data.get("is_logged_in", False)
                    self.has_photo_id = data.get("has_photo_id", False)
            except:
                self.init_default_data()
        else:
            self.init_default_data()

    def init_default_data(self):
        self.gamer_id = f"Assassin_{random.randint(1000, 9999)}"
        self.score = 0
        self.level = 1
        self.currency = 150
        self.username = ""
        self.is_logged_in = False
        self.has_photo_id = False

    def save_game_data(self):
        data = {
            "gamer_id": self.gamer_id,
            "score": self.score,
            "level": self.level,
            "currency": self.currency,
            "username": self.username,
            "is_logged_in": self.is_logged_in,
            "has_photo_id": self.has_photo_id
        }
        with open("save_game.json", "w") as f:
            json.dump(data, f)

    def play_sound_effect(self):
        sound = SoundLoader.load('fire_effect.wav')
        if sound:
            sound.play()

    def handle_login(self, instance):
        username = self.email_input.text.strip()
        if username:
            self.username = username
            self.is_logged_in = True
            self.save_game_data()
            self.status_label.text = f'Logged in as {username} [{self.gamer_id}]. Saved!'
        else:
            self.status_label.text = 'Error: Enter a valid username!'

    def handle_photo_verification(self, instance):
        if not self.is_logged_in:
            self.status_label.text = 'Error: Complete Login first!'
            return
        self.has_photo_id = True
        self.save_game_data()
        self.status_label.text = 'Photo ID Verified! All systems online.'

    def open_upgrade_shop(self, instance):
        if not self.is_logged_in or not self.has_photo_id:
            self.status_label.text = 'Error: Verify ID before opening shop!'
            return
        if self.currency >= 50:
            self.currency -= 50
            self.play_sound_effect()
            self.save_game_data()
            self.status_label.text = f'🔥 Weapon Upgraded! Coins: {self.currency}🪙'
            self.update_hud()
        else:
            self.status_label.text = 'Not enough coins!'

    def toggle_stealth(self, instance):
        if not self.is_logged_in or not self.has_photo_id:
            self.status_label.text = 'Error: Login required!'
            return
        self.stealth_mode = not self.stealth_mode
        state_str = "ACTIVE 🥷" if self.stealth_mode else "INACTIVE"
        self.status_label.text = f'Stealth Mode: {state_str}'

    def trigger_multiplayer_drop(self, instance):
        if not self.is_logged_in or not self.has_photo_id:
            self.status_label.text = 'Error: Login required!'
            return
        friend = random.choice(self.online_friends)
        self.last_message = f"Msg from {friend}: 'Squad joined!'"
        self.status_label.text = f'🌐 Multiplayer Drop: Joined with {friend}!'
        self.update_hud()

    def make_story_choice(self, instance):
        if not self.is_logged_in or not self.has_photo_id:
            self.status_label.text = 'Error: Login required for story mode!'
            return
        choices = [
            "Story Choice: Trusted Elena ❤️ [Romance Unlocked]",
            "Story Choice: Went Rogue 🗡️ [Assassin Path Unlocked]",
            "Story Choice: Shared Intel 🤝 [Alliance Ending Unlocked]"
        ]
        self.status_label.text = f'📖 {random.choice(choices)}'

    def update_achievements(self):
        if self.score >= 90:
            self.current_achievement = "Badge: Legend Flame 👑"
        elif self.score >= 50:
            self.current_achievement = "Badge: Master Assassin 🥈"
        else:
            self.current_achievement = "Badge: Rookie Assassin 🥉"

    def update_hud(self):
        self.id_label.text = f'ID: {self.gamer_id} | Coins: {self.currency}🪙 | {self.current_weather}'
        self.radar_label.text = f'{self.radar_status} | {self.current_achievement}'

    def check_boss_and_ability_reward(self):
        # Har 10th level par Dragon / Monster Boss aayega aur nayi ability milegi
        if self.level % 10 == 0:
            new_ability = f"Ultimate Flame Power Lv.{self.level}"
            self.unlocked_abilities.append(new_ability)
            self.status_label.text = f'🐉 BOSS FIGHT! Level {self.level} Dragon Defeated! New Ability Unlocked: {new_ability}'
        else:
            self.status_label.text = f'⚡ LEVEL UP! Level {self.level} Reached!'

    def on_touch_down(self, touch):
        if self.is_logged_in and self.has_photo_id:
            self.score += 1
            self.currency += 5
            self.play_sound_effect()
            
            self.update_achievements()

            if self.score % 15 == 0:
                self.current_weather = random.choice(self.weather_states)
                self.radar_status = "⚠️ CINEMATIC QTE: Action Event!"
            else:
                self.radar_status = "Radar Active: Secure 🟢"

            if self.score % 30 == 0:
                self.level += 1
                self.check_boss_and_ability_reward()
            else:
                self.status_label.text = f'Mission Active | Score: {self.score} | Level: {self.level}'
            
            self.save_game_data()
            self.update_hud()
            
        return super(FlameAssassinGame, self).on_touch_down(touch)

    def update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size

class TheFlameAssassinApp(App):
    def build(self):
        return FlameAssassinGame()

if __name__ == '__main__':
    TheFlameAssassinApp().run()
