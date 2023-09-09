from typing import Optional
import arcade
from arcade import Texture
import arcade.gui
import random


class Player(arcade.Sprite):
    def on_update(self, deltatime):
        self.center_x += self.change_x * deltatime
        self.center_y += self.change_y * deltatime

        if self.left < 0:
            self.left = 0
        elif self.right > 1000 - 1:
            self.right = 1000 - 1
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > 1000 - 1:
            self.top = 1000 - 1

    def move_up(self):
        self.change_y = 300
        self.angle = 0

    def move_down(self):
        self.change_y = -300
        self.angle = 180

    def move_right(self):
        self.change_x = 300
        self.angle = 270

    def move_left(self):
        self.change_x = -300
        self.angle = 90

    def attack(self):
        if not game.attack.sprite_lists:
            if self.angle == 0:
                game.attack.center_x = self.center_x
                game.attack.center_y = self.center_y + 60

            elif self.angle == 90:
                game.attack.center_x = self.center_x - 60
                game.attack.center_y = self.center_y

            elif self.angle == 180:
                game.attack.center_x = self.center_x
                game.attack.center_y = self.center_y - 60

            elif self.angle == 270:
                game.attack.center_x = self.center_x + 60
                game.attack.center_y = self.center_y

            game.scene.add_sprite("Attack", game.attack)

class Worm(arcade.AnimatedTimeBasedSprite):
    def __new__(cls):
        self = arcade.load_animated_gif("Worm.gif")
        self.__class__ = cls
        self.__init__()
        return self

    def __init__(self):
        self.center_x = random.randrange(1, 1000)
        self.center_y = random.randrange(1, 1000)

    def on_update(self, deltatime):
        # self.update_animation(delta_time=1 / 240)
        self.update_animation(deltatime)
        self.center_x += random.randint(-1, 1)
        self.center_y += random.randint(-1, 1)


class Menu:
    def __init__(self):
        self.uimanager = arcade.gui.UIManager()

        button_text_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.RED,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.GREEN,
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.WHITE,
            "font_color_pressed": arcade.color.BLACK,
        }

        start_button = arcade.gui.UIFlatButton(
            text="Game", width=200, height=100, style=button_text_style
        )
        start_button.on_click = self.hide

        quit_button = arcade.gui.UIFlatButton(
            text="Exit Game", width=200, height=100, style=button_text_style
        )
        quit_button.on_click = lambda event: exit()

        v_box = arcade.gui.UIBoxLayout()
        v_box.add(start_button.with_space_around(bottom=20))
        v_box.add(quit_button.with_space_around(bottom=20))

        self.uimanager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=v_box
            )
        )
        self.show()

    def draw(self):
        if self.uimanager._enabled:
            self.uimanager.draw()

    def show(self):
        self.uimanager.enable()
        self.shown = True

    def hide(self, event):
        self.uimanager.disable()
        self.shown = False


class MainGame(arcade.Window):
    def __init__(self):
        super().__init__(1000, 1000, title="My Super Game", resizable=True)
        arcade.set_background_color(arcade.color.YELLOW)
        self.scene = None
        self.menu = Menu()

    def setup(self):
        NUMBER_OF_WORMS = 100
        self.worms_killed = 0

        self.scene = arcade.Scene()

        self.player_sprite = Player("Mole.png", 0.25, center_x=500, center_y=100)
        self.scene.add_sprite("Player", self.player_sprite)

        self.attack = arcade.load_animated_gif("Attack.gif")

        self.worm_counter = arcade.Sprite("Worm.png", 0.25, center_x=50, center_y=950)
        self.scene.add_sprite("Counter", self.worm_counter)

        self.worms = arcade.SpriteList()
        for i in range(NUMBER_OF_WORMS):
            self.worms.append(Worm())

        self.scene.add_sprite_list(f"Worms", sprite_list=self.worms)

    def on_draw(self):
        self.clear()
        self.scene.draw()
        self.menu.draw()
        message = ":" + str(self.worms_killed)
        arcade.draw_text(message, 75, 935, arcade.color.BLACK, 30)

    def update(self, deltatime):
        if not self.menu.shown:
            self.scene.on_update(deltatime)

            if self.attack.sprite_lists:
                # sometimes fails with TypeError: '<=' not supported between instances of 'NoneType' and 'float'!
                worm_hit_list = arcade.check_for_collision_with_list(
                    self.attack, self.worms
                )
                for worm in worm_hit_list:
                    worm.kill()
                    self.worms_killed += 1

                self.attack.update_animation(deltatime)
                if self.attack.cur_frame_idx > 8:
                    self.attack.cur_frame_idx = 0
                    self.attack.kill()

    def on_key_press(self, key, modifiers):
        if self.menu.shown:
            return

        if key == arcade.key.ESCAPE:
            self.menu.show()

        if key == arcade.key.W:
            self.player_sprite.move_up()

        elif key == arcade.key.S:
            self.player_sprite.move_down()

        elif key == arcade.key.A:
            self.player_sprite.move_left()

        elif key == arcade.key.D:
            self.player_sprite.move_right()


        if key == arcade.key.SPACE:
            self.player_sprite.attack()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0

        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0


game = MainGame()
game.setup()
arcade.run()
