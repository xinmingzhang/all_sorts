import sys
import json
import random
import math
import pygame as pg


class MySprite(pg.sprite.Sprite):
    def __init__(self, image, x, y, name, **kwargs):
        super(MySprite, self).__init__()
        self.image = image
        w, h = self.image.get_size()
        self.rect = pg.Rect(x, y, w, h)
        self.name = name
        self.gdp = int(kwargs['gdp'])
        self.pop_growth = kwargs['pop growth']
        self.debt = int(kwargs['debt'])
        self.gdp_growth = kwargs['gdp growth']
        self.population = kwargs['population']
        self.pos = self.rect.center
        angle = random.uniform(0, 2 * math.pi)
        self.direction = [math.sin(angle), math.cos(angle)]
        self.speed = 0.2
        self.sorted = False
        self.destination = (0, 0)

    def update(self, dt):
        if not self.sorted:
            self.random_move(dt)
        elif self.sorted:
            self.move(dt)

    def random_move(self, dt):
        self.pos = (
        self.direction[0] * self.speed * dt + self.pos[0], self.direction[1] * self.speed * dt + self.pos[1])
        self.rect = self.image.get_rect(center=self.pos)
        self.rect.center = self.pos
        screenrect = pg.display.get_surface().get_rect()
        r = self.rect.clamp(screenrect)
        if r != self.rect:
            angle = random.uniform(0, 2 * math.pi)
            self.direction = [math.sin(angle), math.cos(angle)]
            self.rect = r
            self.pos = self.rect.center

    def move(self, dt):
        dx = self.destination[0] - self.pos[0]
        dy = self.destination[1] - self.pos[1]
        time = 60.0
        delta_x = dx / time
        delta_y = dy / time
        self.pos = (delta_x * dt + self.pos[0], delta_y * dt + self.pos[1])
        self.rect = self.image.get_rect(center=self.pos)
        self.rect.center = self.pos


class App(object):
    def __init__(self, screen_size):
        self.done = False
        self.screen = pg.display.set_mode(screen_size)
        self.state = 'All Sorts'
        self.caption = pg.display.set_caption(self.state)
        self.clock = pg.time.Clock()
        self.fps = 60
        self.bg_color = pg.Color("gray5")
        with open('nations_info.json', 'r') as f:
            self.data = json.load(f)
        self.countries = {}
        self.group = pg.sprite.Group()
        for c in self.data:
            img = pg.image.load('./flags/{}.png'.format(c.replace(' ', '-')))
            self.countries[c] = MySprite(img, random.randint(0, 1280), random.randint(0, 720), c, **self.data[c])
            self.group.add(self.countries[c])

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.done = True
                if event.key == pg.K_1:
                    self.state = 'debt descending order'
                    self.country_sort('debt', True)
                if event.key == pg.K_2:
                    self.state = 'debt ascending order'
                    self.country_sort('debt', False)
                if event.key == pg.K_3:
                    self.state = 'gdp descending order'
                    self.country_sort('gdp', True)
                if event.key == pg.K_4:
                    self.state = 'gdp ascending order'
                    self.country_sort('gdp', False)
                if event.key == pg.K_5:
                    self.state = 'gdp_growth descending order'
                    self.country_sort('gdp_growth', True)
                if event.key == pg.K_6:
                    self.state = 'gdp_growth ascending order'
                    self.country_sort('gdp_growth', False)
                if event.key == pg.K_7:
                    self.state = 'population descending order'
                    self.country_sort('population', True)
                if event.key == pg.K_8:
                    self.state = 'population ascending order'
                    self.country_sort('population', False)
                if event.key == pg.K_9:
                    self.state = 'pop_growth descending order'
                    self.country_sort('pop_growth', True)
                if event.key == pg.K_0:
                    self.state = 'pop_growth ascending order'
                    self.country_sort('pop_growth', False)
            if event.type == pg.KEYUP:
                self.state = 'All Sorts'
                self.country_shuffle()
            if event.type == pg.MOUSEMOTION:
                for c in self.countries:
                    if self.countries[c].rect.collidepoint(*event.pos):
                        self.caption = pg.display.set_caption('{}    {}'.format(self.state, self.countries[c].name))

    def update(self, dt):
        self.group.update(dt)

    def country_shuffle(self):
        for c in self.countries:
            self.countries[c].sorted = False

    def country_sort(self, arg, reverse):
        d = {value: key for key, value in self.countries.items()}
        l = list(d)
        order_list = sorted(l, key=lambda country: getattr(country, arg), reverse=reverse)
        for c in order_list:
            num = order_list.index(c)
            i = num % 16
            j = num // 16
            pos = (i * 80 + 40, j * 60 + 30)
            c.sorted = True
            c.destination = pos

    def draw(self):
        self.screen.fill(self.bg_color)
        self.group.draw(self.screen)

    def run(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()


if __name__ == "__main__":
    game = App((1280, 720))
    game.run()
    pg.quit()
    sys.exit()
