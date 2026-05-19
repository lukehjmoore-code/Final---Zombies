from turtle import *
from random import randint, choice
import time

screen = Screen()
screen.bgcolor("light green")
screen.title("ZOMBIES")
screen.setup(width=600, height=600)
screen.tracer(0)

playing_area_size = 250
p1_bullets = []
p2_bullets = []
zombies = []
bombs = []
p1_score = 0
p2_score = 0
spawn_count = 2 

def playing_area():
    t = Turtle()
    t.hideturtle()
    t.speed(0)
    t.pu()
    t.color("light blue")
    t.goto(-250, 250)
    t.pd()
    t.pensize(3)
    for i in range(4):
        t.forward(500)
        t.right(90)
    t.pu()

class Player(Turtle):
    def __init__(self, x, y, color, left_key, right_key, fire_key, bomb_key, target_list):
        super().__init__()
        self.shape("turtle")
        self.color(color)
        self.pu()
        self.goto(x, y)
        self.setheading(randint(0, 360))
        self.left_key = left_key
        self.right_key = right_key
        self.fire_key = fire_key
        self.bomb_key = bomb_key
        self.bullets = []
        self.bombs_left = 3
        self.speed_val = 5
        self.is_alive = True

    def move(self):
        if not self.is_alive: return
        self.forward(self.speed_val)
        if self.xcor() > 240 or self.xcor() < -240:
            self.setheading(180 - self.heading())
        if self.ycor() > 240 or self.ycor() < -240:
            self.setheading(360 - self.heading())

    def turnLeft(self):
        if self.is_alive: self.left(10)

    def turnRight(self):
        if self.is_alive: self.right(10)

    def fire(self):
        if self.is_alive and len(self.bullets) < 5:
            b = Bullet(self.xcor(), self.ycor(), self.heading(), self)
            self.bullets.append(b)

    def drop_bomb(self):
        if self.is_alive and self.bombs_left > 0:
            bombs.append(Bomb(self.xcor(), self.ycor()))
            self.bombs_left -= 1
            print(f"{self.color()[0]} dropped bomb. {self.bombs_left} left.")

class Bullet(Turtle):
    def __init__(self, x, y, heading, owner):
        super().__init__()
        self.shape("circle")
        self.shapesize(0.3, 0.3)
        self.color("yellow")
        self.pu()
        self.goto(x, y)
        self.setheading(heading)
        self.owner = owner

    def move(self):
        self.forward(15)
        if not (-250 < self.xcor() < 250 and -250 < self.ycor() < 250):
            self.die()

    def die(self):
        self.hideturtle()
        if self in self.owner.bullets:
            self.owner.bullets.remove(self)
        if self in screen.turtles():
            self.clear()
            self.hideturtle()

class Zombie(Turtle):
    def __init__(self, target_player):
        super().__init__()
        self.color("green")
        self.pu()
        self.goto(randint(-200, 200), randint(-200, 200))
        self.target = target_player
        self.speed_val = 2

    def move(self):
        self.setheading(self.towards(self.target))
        self.forward(self.speed_val)

class Prize(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("gold")
        self.pu()
        self.relocate()

    def relocate(self):
        self.goto(randint(-200, 200), randint(-200, 200))

class Bomb(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.hideturtle()
        self.pu()
        self.goto(x, y)
        self.color("orange")
        self.timer = 50
        self.exploded = False

    def explode(self):
        self.goto(self.xcor(), self.ycor())
        self.shape("circle")
        self.shapesize(10, 10)
        self.color("orange")
        self.showturtle()
        
        for z in zombies[:]:
            if self.distance(z) < 100:
                z.hideturtle()
                zombies.remove(z)
                update_score(1)

        screen.update()
        time.sleep(0.2)
        self.hideturtle()
        self.clear()

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.hideturtle()
        self.pu()
        self.goto(0, 260)
        self.update_score()

    def update_score(self):
        self.clear()
        self.write(f"P1 (Blue) Score: {p1_score}  |  P2 (Red) Score: {p2_score}", 
                   align="center", font=("Arial", 16, "normal"))

def spawn_zombies():
    global spawn_count
    for _ in range(spawn_count // 2):
        zombies.append(Zombie(p1))
        zombies.append(Zombie(p2))
    spawn_count += 2

def update_score(amount):
    global p1_score, p2_score
    p1_score += amount
    score.update_score()

def game_over(winner):
    msg = Turtle()
    msg.color("white")
    msg.hideturtle()
    msg.write(f"GAME OVER! {winner} Wins!", align="center", font=("Arial", 30, "bold"))
    screen.update()
    time.sleep(3)
    screen.bye()

playing_area()
p1 = Player(-100, 0, "blue", "a", "d", "w", "s", None)
p2 = Player(100, 0, "red", "Left", "Right", "Up", "Down", None)
prize = Prize()
score = Scoreboard()

screen.listen()
screen.onkeypress(p1.turnLeft, p1.left_key)
screen.onkeypress(p1.turnRight, p1.right_key)
screen.onkeypress(p1.fire, p1.fire_key)
screen.onkeypress(p1.drop_bomb, p1.bomb_key)
screen.onkeypress(p2.turnLeft, p2.left_key)
screen.onkeypress(p2.turnRight, p2.right_key)
screen.onkeypress(p2.fire, p2.fire_key)
screen.onkeypress(p2.drop_bomb, p2.bomb_key)

game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(0.02) 

    p1.move()
    p2.move()

    for b in p1.bullets + p2.bullets:
        b.move()

    for z in zombies:
        z.move()
        if z.distance(p1) < 20:
            p1.hideturtle(); p1.is_alive = False
            game_over("Player 2 (Red)")
            game_is_on = False
        if z.distance(p2) < 20:
            p2.hideturtle(); p2.is_alive = False
            game_over("Player 1 (Blue)")
            game_is_on = False

    if p1.distance(prize) < 20 or p2.distance(prize) < 20:
        prize.relocate()
        spawn_zombies()

    for b in p1.bullets + p2.bullets:
        for z in zombies[:]:
            if b.distance(z) < 15:
                z.hideturtle()
                zombies.remove(z)
                b.die()
                update_score(1)

    for bomb in bombs[:]:
        bomb.timer -= 1
        if bomb.timer <= 0 and not bomb.exploded:
            bomb.explode()
            bomb.exploded = True
            bombs.remove(bomb)

    if not game_is_on: break

screen.exitonclick()
