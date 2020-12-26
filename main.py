"""
Name: Johnson Dinh
Spongebob RPG

-> inspiration and credits to: https://blackdevilx.newgrounds.com :)
"""

import sys
import pygame as p
import random


class Block(p.sprite.Sprite):
    def __init__(self, color, x, y, width, height, border_type=1):
        p.sprite.Sprite.__init__(self)

        self._image = p.Surface([width, height])
        self._image.fill(color)

        self._x = x
        self._y = y

        # border for the options
        if border_type == 1:
            self._rect = self._image.get_rect(center=(x+113, y+50))

        # border for the spells menu
        if border_type == 2:
            self._rect = self._image.get_rect(center=(x+123, y+75))

        # border for the description word box
        if border_type == 3:
            self._rect = self._image.get_rect(center=(x+115, y+15))

        # border for the actual description box
        if border_type == 4:
            self._rect = self._image.get_rect(center=(x+160, y+75))

    # virtual draw function
    def draw(self, surface):
        surface.blit(self._image, (self._x, self._y))
        p.draw.rect(surface, (128, 128, 128), self._rect, 5)

    @property
    def y(self):
        return self._y

    @property
    def x(self):
        return self._x

    @property
    def image(self):
        return self._image


class SpongebobSprite(p.sprite.Sprite):
    def __init__(self, x, y):
        super(SpongebobSprite, self).__init__()

        self._x = x
        self._y = y
        self._index = 0
        self._change_image_counter = 0
        self._current_time = 0

        self._spongebob_hp = 500
        self._spongebob_mp = 300

        self._display_background = p.image.load("displayBackground.PNG")

        self._spongebob_logo = p.image.load("spongebob_logo.png")
        self._spongebob_logo = p.transform.scale(self._spongebob_logo, (150, 150))

        self._font = p.font.Font("OpenSans-Bold.ttf", 40)
        self._spongebob_hp_word_text = self._font.render("HP=", True, (58, 205, 58))
        self._spongebob_mp_word_text = self._font.render("MP=", True, (168, 58, 205))

        self._spongebob_remaining_hp_text = self._font.render("500/500", True, (58, 205, 58))
        self._spongebob_remaining_mp_text = self._font.render("300/300", True, (168, 58, 205))

        self._spongebob_images_list = []

        self._health_potions = 2
        self._mana_potions = 2
        self._elixirs = 1

        for i in range(0, 9):
            temp = "spongebob" + str(i + 1) + ".png"
            self._spongebob_images_list.append(p.image.load(temp))
            self._spongebob_images_list[i] = p.transform.scale(self._spongebob_images_list[i], (200, 200))

        self._spongebob_sprite = self._spongebob_images_list[self._index]

        self._rect = self._spongebob_sprite.get_rect()

    # moves the sprite with arrow keys
    def move(self, velocity=1):
        key = p.key.get_pressed()

        self._x = min(max(1, self._x), 1265)  # prevent object from going out of bounds (x position)
        self._y = min(max(1, self._y), 665)  # prevent object from going out of bounds (y position)

        if key[p.K_DOWN]:
            self._y += velocity
        elif key[p.K_UP]:
            self._y -= velocity
        elif key[p.K_RIGHT]:
            self._x += velocity
        elif key[p.K_LEFT]:
            self._x -= velocity

    # check is spongebob still has enough mana
    def check_for_mana_cost(self, spell_type):
        if spell_type == 1:
            if self._spongebob_mp < 20:
                return False
        if spell_type == 2:
            if self._spongebob_mp < 40:
                return False
        if spell_type == 3:
            if self._spongebob_mp < 80:
                return False
        return True

    def use_item(self, item_type):
        if item_type == 1:
            self._spongebob_hp = 500
            self._spongebob_remaining_hp_text = self._font.render(f"{self._spongebob_hp}/500", True, (58, 205, 58))
            return True
        if item_type == 2:
            self._spongebob_mp = 300
            self._spongebob_remaining_mp_text = self._font.render(f"{self._spongebob_mp}/300", True, (168, 58, 205))
            return True
        if item_type == 3:
            self._spongebob_hp = 500
            self._spongebob_mp = 300
            self._spongebob_remaining_hp_text = self._font.render(f"{self._spongebob_hp}/500", True, (58, 205, 58))
            self._spongebob_remaining_mp_text = self._font.render(f"{self._spongebob_mp}/300", True, (168, 58, 205))
            return True
        return False

    # confirm action from jellyfish on spongebob
    def confirm_action_on_spongebob(self, spell_type=0):
        rand_num = random.randint(25, 40)

        self._spongebob_hp -= rand_num
        self._spongebob_remaining_hp_text = self._font.render(f"{self._spongebob_hp}/500", True, (58, 205, 58))

        if spell_type == 1:
            self._spongebob_mp -= 20
        elif spell_type == 2:
            self._spongebob_mp -= 40
        elif spell_type == 3:
            self._spongebob_mp -= 80

        self._spongebob_remaining_mp_text = self._font.render(f"{self._spongebob_mp}/300", True, (168, 58, 205))

    # animates the sprite with images (frame dependent)
    def update_image_frame_dependent(self):

        if self._change_image_counter == 100:
            self._index += 1

            if self._index >= len(self._spongebob_images_list):
                self._index = 0

            self._spongebob_sprite = self._spongebob_images_list[self._index]

            self._change_image_counter = 0

        self._change_image_counter += 1

    # animates the sprite with images (time dependent)
    def update_image_time_dependent(self, value):
        self._current_time += value

        if self._current_time >= 0.1:  # self._animation_time
            self._current_time = 0
            self._index = (self._index + 1) % len(self._spongebob_images_list)
            self._spongebob_sprite = self._spongebob_images_list[self._index]

    def draw(self, surface):
        if self._spongebob_hp <= 0:
            self._spongebob_remaining_hp_text = self._font.render("0/500", True, (50, 205, 50))
        surface.blit(self._display_background, (0, 0))
        surface.blit(self._spongebob_logo, (25, 25))
        surface.blit(self._spongebob_hp_word_text, (175, 40))
        surface.blit(self._spongebob_remaining_hp_text, (270, 40))
        surface.blit(self._spongebob_mp_word_text, (165, 110))
        surface.blit(self._spongebob_remaining_mp_text, (270, 110))
        surface.blit(self._spongebob_sprite, (self._x, self._y))


class JellyFish(p.sprite.Sprite):
    def __init__(self, x, y):
        super(JellyFish).__init__()

        self._jellyfish_hp = 7500

        self._x = x
        self._y = y
        self._index = 0
        self._change_image_counter = 0
        self._current_time = 0

        self._font = p.font.Font("OpenSans-Bold.ttf", 40)
        self._jellyfish_logo = p.image.load("jellyfish_logo.png")
        self._jellyfish_logo = p.transform.scale(self._jellyfish_logo, (150, 150))
        self._jellyfish_remaining_hp_text = self._font.render("7500/7500", True, (58, 205, 58))
        self._jellyfish_hp_word_font = self._font.render("HP=", True, (58, 205, 58))

        self._display_background = p.image.load("displayBackground.PNG")

        self._jellyfish_images_list = []

        for i in range(0, 8):
            temp = "jellyfish" + str(i + 1) + ".png"
            self._jellyfish_images_list.append(p.image.load(temp))
            self._jellyfish_images_list[i] = p.transform.scale(self._jellyfish_images_list[i], (300, 300))

        self._jellyfish_sprite = self._jellyfish_images_list[self._index]

        self._rect = self._jellyfish_sprite.get_rect()

    def update_image(self, value):
        self._current_time += value

        if self._current_time >= 0.1:  # self._animation_time
            self._current_time = 0
            self._index = (self._index + 1) % len(self._jellyfish_images_list)
            self._jellyfish_sprite = self._jellyfish_images_list[self._index]

    def confirm_action_on_jellyfish(self, value, spell_value):
        rand_num = 0

        if value == 1:
            rand_num = random.randint(45, 65) * 5

            self._jellyfish_hp -= rand_num
            self._jellyfish_remaining_hp_text = self._font.render(f"{self._jellyfish_hp}/7500", True, (58, 205, 58))
            return True

        if 1 <= spell_value <= 3:
            if spell_value == 1:
                rand_num = random.randint(100, 125)
            if spell_value == 2:
                rand_num = random.randint(150, 175)
            if spell_value == 3:
                rand_num = random.randint(250, 275)

            self._jellyfish_hp -= rand_num
            self._jellyfish_remaining_hp_text = self._font.render(f"{self._jellyfish_hp}/7500", True, (58, 205, 58))
            return True

        return False

    def draw(self, surface):
        if self._jellyfish_hp <= 0:
            self._jellyfish_remaining_hp_text = self._font.render(f"0/7500", True, (58, 205, 58))

        surface.blit(self._display_background, (902, 0))
        surface.blit(self._jellyfish_logo, (925, 25))
        surface.blit(self._jellyfish_hp_word_font, (1060, 70))
        surface.blit(self._jellyfish_remaining_hp_text, (1145, 70))
        surface.blit(self._jellyfish_sprite, (self._x, self._y))


# actions for spongebob
class Actions(SpongebobSprite):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self._actions_background_list = []

        for count in range(0, 4):
            self._actions_background_list.append(p.image.load("actions_background.PNG"))
            self._actions_background_list[count] = p.transform.scale(self._actions_background_list[count], (90, 40))

        self._font = p.font.Font("OpenSans-Bold.ttf", 23)
        self._attack_text = self._font.render("ATK", True, (0, 0, 0))
        self._spells_text = self._font.render("SPELL", True, (0, 0, 0))
        self._items_text = self._font.render("ITEM", True, (0, 0, 0))
        self._run_text = self._font.render("RUN", True, (0, 0, 0))

        self._commit_action = False

        self._show_spell_options = False
        self._show_item_options = False

        self._background_description_word_text = Block((170, 183, 184), 525, 165, 225, 35, 3)
        self._description_word_text = self._font.render("DESCRIPTION", True, (255, 255, 255))
        self._background_description = Block((170, 183, 184), 475, 200, 325, 150, 4)
        self._full_description_text = self._font.render("", True, (255, 255, 255))
        self._background = Block((170, 183, 184), 225, 200, 250, 150, 2)

        self._font = p.font.Font("OpenSans-Bold.ttf", 25)
        self._spell_one_text = self._font.render("Krabby Patty", True, (255, 255, 255))
        self._spell_two_text = self._font.render("Gary Bomb", True, (255, 255, 255))
        self._spell_three_text = self._font.render("Golden Spatula", True, (255, 255, 255))
        self._spell_four_text = self._font.render("- " * 14, True, (255, 255, 255))

        self._spell_cost_text = self._font.render("COST= N/A MP", True, (255, 255, 255))

        self._item_one_text = self._font.render("HEALTH POTION", True, (255, 255, 255))
        self._item_two_text = self._font.render("MANA POTION", True, (255, 255, 255))
        self._item_three_text = self._font.render("ELIXIR", True, (255, 255, 255))
        self._item_four_text = self._font.render("- " * 14, True, (255, 255, 255))

        self._item_amount_text = self._font.render("AMOUNT: N/A", True, (255, 255, 255))

    def detect_action_click(self):
        """
        event.button reference
        1 - left click
        2 - middle click
        3 - right click
        4 - scroll up
        5 - scroll down
        """

        if event.type == p.MOUSEBUTTONUP and event.button == 1:
            x, y = p.mouse.get_pos()

            if 17 <= x <= 103 and 212 <= y <= 245:
                print('attack')
                return 1

            elif 122 <= x <= 208 and 212 <= y <= 245:
                print('spell')
                return 2

            elif 17 <= x <= 103 and 252 <= y <= 285:
                print('item')
                return 3

            elif 122 <= x <= 208 and 252 <= y <= 285:
                print('run')
                return 4

    def do_specific_action(self, value):
        # attack
        if value == 1:
            pass

        # spells
        if value == 2:
            self._show_item_options = False
            self._show_spell_options = True

        # items
        if value == 3:
            self._show_spell_options = False
            self._show_item_options = True

        # run
        if value == 4:
            exit(0)

        return value

    def show_spell_cost_and_description(self):
        x, y = p.mouse.get_pos()

        # check if mouse hovers over spell 1
        if 237 <= x <= 420 and 202 <= y <= 240:
            self._spell_one_text = self._font.render("Krabby Patty", True, (0, 0, 255))
            self._spell_cost_text = self._font.render("COST=  20  MP", True, (255, 255, 255))

            self._full_description_text = self._font.render("KRABBY PATTY ATTACK", True, (255, 255, 255))
            return
        else:
            self._spell_one_text = self._font.render("Krabby Patty", True, (255, 255, 255))
            self._spell_cost_text = self._font.render("COST= N/A MP", True, (255, 255, 255))
            self._full_description_text = self._font.render("", True, (255, 255, 255))

        # check if mouse hovers over spell 2
        if 237 <= x <= 400 and 250 <= y <= 275:
            self._spell_two_text = self._font.render("Gary Bomb", True, (0, 0, 255))
            self._spell_cost_text = self._font.render("COST=  40  MP", True, (255, 255, 255))

            self._full_description_text = self._font.render("THROW A GARY BOMB", True, (255, 255, 255))
            return
        else:
            self._spell_two_text = self._font.render("Gary Bomb", True, (255, 255, 255))
            self._spell_cost_text = self._font.render("COST= N/A MP", True, (255, 255, 255))
            self._full_description_text = self._font.render("", True, (255, 255, 255))

        # check if mouse hovers over spell 3
        if 237 <= x <= 450 and 290 <= y <= 310:
            self._spell_three_text = self._font.render("Golden Spatula", True, (0, 0, 255))
            self._spell_cost_text = self._font.render("COST=  80  MP", True, (255, 255, 255))

            self._full_description_text = self._font.render("THE ULTIMATE ATTACK", True, (255, 255, 255))
            return
        else:
            self._spell_three_text = self._font.render("Golden Spatula", True, (255, 255, 255))
            self._spell_cost_text = self._font.render("COST= N/A MP", True, (255, 255, 255))
            self._full_description_text = self._font.render("", True, (255, 255, 255))

    def show_item_amount_and_description(self):
        x, y = p.mouse.get_pos()

        # check if mouse hovers over item 1
        if 237 <= x <= 475 and 202 <= y <= 240:
            self._item_one_text = self._font.render("HEALTH POTION", True, (0, 0, 255))
            self._item_amount_text = self._font.render(f"AMOUNT:   {self._health_potions}", True, (255, 255, 255))

            self._full_description_text = self._font.render("RESTORES ALL HP", True, (255, 255, 255))
            return
        else:
            self._item_one_text = self._font.render("HEALTH POTION", True, (255, 255, 255))
            self._item_amount_text = self._font.render("AMOUNT: N/A", True, (255, 255, 255))
            self._full_description_text = self._font.render("", True, (255, 255, 255))

        # check if mouse hovers over item 2
        if 237 <= x <= 450 and 250 <= y <= 275:
            self._item_two_text = self._font.render("MANA POTION", True, (0, 0, 255))
            self._item_amount_text = self._font.render(f"AMOUNT:   {self._mana_potions}", True, (255, 255, 255))

            self._full_description_text = self._font.render("RESTORES ALL MP", True, (255, 255, 255))
            return
        else:
            self._item_two_text = self._font.render("MANA POTION", True, (255, 255, 255))
            self._item_amount_text = self._font.render("AMOUNT: N/A", True, (255, 255, 255))
            self._full_description_text = self._font.render("", True, (255, 255, 255))

        # check if mouse hovers over item 3
        if 237 <= x <= 325 and 280 <= y <= 310:
            self._item_three_text = self._font.render("ELIXIR", True, (0, 0, 255))
            self._item_amount_text = self._font.render(f"AMOUNT:   {self._elixirs}", True, (255, 255, 255))

            self._full_description_text = self._font.render("RESTORES HP AND MP", True, (255, 255, 255))
            return
        else:
            self._item_three_text = self._font.render("ELIXIR", True, (255, 255, 255))
            self._item_amount_text = self._font.render("AMOUNT: N/A", True, (255, 255, 255))
            self._full_description_text = self._font.render("", True, (255, 255, 255))

    def click_on_spell(self):
        if self._show_spell_options is True:
            if event.type == p.MOUSEBUTTONUP and event.button == 1:
                x, y = p.mouse.get_pos()

                if 237 <= x <= 420 and 202 <= y <= 240:
                    return 1

                if 237 <= x <= 400 and 250 <= y <= 275:
                    return 2

                if 237 <= x <= 450 and 290 <= y <= 310:
                    return 3
        return 0

    def click_on_item(self):
        if self._show_item_options is True:
            if event.type == p.MOUSEBUTTONUP and event.button == 1:
                x, y = p.mouse.get_pos()

                # item 1
                if 237 <= x <= 475 and 202 <= y <= 240:
                    if self._health_potions == 0:
                        return
                    self._health_potions -= 1
                    return 1

                # item 2
                if 237 <= x <= 450 and 250 <= y <= 275:
                    if self._mana_potions == 0:
                        return
                    self._mana_potions -= 1
                    return 2

                # item 3
                if 237 <= x <= 325 and 280 <= y <= 310:
                    if self._elixirs == 0:
                        return
                    self._elixirs -= 1
                    return 3
        return 0

    def draw(self, surface):
        surface.blit(self._actions_background_list[0], (15, 210))
        surface.blit(self._actions_background_list[1], (120, 210))
        surface.blit(self._actions_background_list[2], (15, 250))
        surface.blit(self._actions_background_list[3], (120, 250))

        surface.blit(self._attack_text, (40, 210))
        surface.blit(self._spells_text, (135, 210))
        surface.blit(self._items_text, (35, 250))
        surface.blit(self._run_text, (140, 250))

        if self._show_spell_options is True or self._show_item_options is True:
            self._background.draw(surface)
            self._background_description_word_text.draw(surface)
            self._background_description.draw(surface)
            surface.blit(self._description_word_text, (547, 160))
            surface.blit(self._full_description_text, (500, 260))

            if self._show_spell_options is True:
                surface.blit(self._spell_cost_text, (540, 200))
                surface.blit(self._spell_one_text, (235, 205))
                surface.blit(self._spell_two_text, (235, 240))
                surface.blit(self._spell_three_text, (235, 275))
                surface.blit(self._spell_four_text, (235, 310))
                self.show_spell_cost_and_description()

            if self._show_item_options is True:
                surface.blit(self._item_amount_text, (540, 200))
                surface.blit(self._item_one_text, (235, 205))
                surface.blit(self._item_two_text, (235, 240))
                surface.blit(self._item_three_text, (235, 275))
                surface.blit(self._item_four_text, (235, 310))
                self.show_item_amount_and_description()


# do animations for fighting
class Animations(p.sprite.Sprite):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    p.init()

    clock = p.time.Clock()

    screen = p.display.set_mode(size=(1366, 768))
    p.display.set_caption("Spongebob RPG")

    b = Block((170, 183, 184), 0, 200, 225, 100)
    s = SpongebobSprite(150, 500)
    j = JellyFish(1000, 400)
    a = Actions()

    jellyfish_fields_background = p.image.load("jellyfish fields.jpg")
    jellyfish_fields_background = p.transform.scale(jellyfish_fields_background, (1366, 768))  # resize image

    while True:
        td = clock.tick(60) / 1000  # 60 represents FPS

        for event in p.event.get():
            if event.type == p.QUIT:
                sys.exit()

            spongebob_action_value = a.do_specific_action(a.detect_action_click())
            spongebob_spell_value = a.click_on_spell()
            spongebob_check_mana_bool = s.check_for_mana_cost(spongebob_spell_value)

            spongebob_item_value = a.click_on_item()
            spongebob_used_item_bool = s.use_item(spongebob_item_value)

            if spongebob_check_mana_bool is True:
                # once spongebob makes a move, the jellyfish will go right after
                if j.confirm_action_on_jellyfish(spongebob_action_value, spongebob_spell_value) is True:
                    s.confirm_action_on_spongebob(spongebob_spell_value)

            if spongebob_used_item_bool is True:
                s.confirm_action_on_spongebob()

        screen.fill([0, 0, 0])

        screen.blit(jellyfish_fields_background, jellyfish_fields_background.get_rect())

        # s.update_image()
        s.update_image_time_dependent(td)
        s.draw(screen)

        j.update_image(td)
        j.draw(screen)

        b.draw(screen)

        a.draw(screen)

        p.display.update()
