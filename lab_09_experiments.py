import arcade
import arcade.gui
import random

class Player(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.left < 0:
            self.left = 0
        elif self.right > 1000 - 1:
            self.right = 1000 - 1
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > 1000 - 1:
            self.top = 1000 - 1

class Worm(arcade.AnimatedTimeBasedSprite):
    def update(self):
        self.update_animation(delta_time=1/240)

class MainGame(arcade.Window):
    def __init__(self):
        super().__init__(1000, 1000, title="Menu_example", resizable=True)
        arcade.set_background_color(arcade.color.YELLOW)

        self.v_box = arcade.gui.UIBoxLayout()

        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()

        self.menu = True

        default_style = {
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

        self.start_button = arcade.gui.UIFlatButton(text="Game", width=200, height=100, style=default_style)
        self.settings_button = arcade.gui.UIFlatButton(text="Settings", width=200, height=100, style=default_style)
        self.quit_button = arcade.gui.UIFlatButton(text="Exit Game", width=200, height=100, style=default_style)

        self.v_box.add(self.start_button.with_space_around(bottom=20))
        self.v_box.add(self.settings_button.with_space_around(bottom=20))
        self.v_box.add(self.quit_button.with_space_around(bottom=20))

        self.start_button.on_click = self.buttonclick
        self.quit_button.on_click = self.quit_game

        self.uimanager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def buttonclick(self, event):
        self.menu = False

    def quit_game(self, event):
        if self.menu:
            exit()

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player_sprite = Player('Mole.png', 0.25)
        self.player_list.append(self.player_sprite)
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 100

        self.attacking = False
        self.worm_list = arcade.SpriteList()
        self.attack_list = arcade.SpriteList()

        for i in range(10):
            worm = arcade.load_animated_gif("Worm.gif")
            self.worm_list.append(worm)
            worm.center_x = random.randrange(1, 1000)
            worm.center_y = random.randrange(1, 1000)

    def on_draw(self):
        arcade.start_render()
        if self.menu:
            self.uimanager.draw()

        # if not self.menu:
        self.player_list.draw()
        self.worm_list.draw()
        self.attack_list.draw()

    def worm_move(self, worms):
        for worm in worms:
            worm.update_animation(delta_time=1/200)
            # e = random.randint(0, 1)
            # print(e)
            move_right = random.randint(0, 1)
            move_up = random.randint(0, 1)

            if move_right == True:
                # print('+1')
                worm.center_x += 1

            elif move_right == False:
                # print('-1')
                worm.center_x -= 1

            if move_up == True:
                # print('+1')
                worm.center_y += 1

            elif move_up == False:
                # print('-1')
                worm.center_y -= 1

    def update(self, deltatime):
        if not self.menu:
            self.player_list.update()
            self.worm_move(self.worm_list)
            for attack in self.attack_list:
                self.attack_frame += 0.12
                attack.update_animation(delta_time=1/100)
                if self.attack_frame >= 10:
                    self.attacking = False
                    attack.kill()

            if self.attacking:
                worm_hit_list = arcade.check_for_collision_with_list(self.attack, self.worm_list)
                for worm in worm_hit_list:
                    worm.kill()





    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.menu = True

        if not self.menu:
            if key == arcade.key.W:
                self.player_sprite.change_y = 3
                self.player_sprite.angle = 0

            elif key == arcade.key.S:
                self.player_sprite.change_y = -3
                self.player_sprite.angle = 180

            elif key == arcade.key.A:
                self.player_sprite.change_x = -3
                self.player_sprite.angle = 90

            elif key == arcade.key.D:
                self.player_sprite.change_x = 3
                self.player_sprite.angle = 270

            if key == arcade.key.SPACE:
                if not self.attacking:
                    self.attacking = True
                    self.attack = arcade.load_animated_gif('Attack.gif')
                    self.attack_list.append(self.attack)
                    self.attack_frame = 1

                    if self.player_sprite.angle == 0:
                        self.attack.center_x = self.player_sprite.center_x
                        self.attack.center_y = self.player_sprite.center_y + 60

                    elif self.player_sprite.angle == 90:
                        self.attack.center_x = self.player_sprite.center_x - 60
                        self.attack.center_y = self.player_sprite.center_y

                    elif self.player_sprite.angle == 180:
                        self.attack.center_x = self.player_sprite.center_x
                        self.attack.center_y = self.player_sprite.center_y - 60

                    elif self.player_sprite.angle == 270:
                        self.attack.center_x = self.player_sprite.center_x + 60
                        self.attack.center_y = self.player_sprite.center_y

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0

        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0

game = MainGame()
game.setup()
arcade.run()