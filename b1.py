import turtle
import winsound
import time
import random
from tkinter import *

score = 0
highest_score = 0
count = 0
execution_delay = 0.1
pause_duration = 0
pause_state = False

screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.bgpic("s9.gif")

def start_game():
    global game_screen
    screen.clear()
    game_screen = turtle.Screen()
    game_screen.title('Snake Game')
    game_screen.setup(width=600, height=600)
    game_screen.bgcolor('lightgreen')
    game_screen.bgpic('border.gif')
    game_screen.tracer(False)
    game_screen.addshape('upmouth.gif')
    game_screen.addshape('food.gif')
    game_screen.addshape('downmouth.gif')
    game_screen.addshape('leftmouth.gif')
    game_screen.addshape('rightmouth.gif')
    game_screen.addshape('body (3).gif')

    initialize_game()

button = Button(screen.getcanvas().master, text="   START   ", command=start_game, bg="green", fg="red",
                font=("Arial", 20, "bold"))
button.pack()
button.place(x=190, y=450)  
button.config(width=12)

def initialize_game():
    global head, food, text, segments, button

    button.pack_forget()
    button.destroy()

    global score, count, execution_delay, pause_state
    score = 0
    count = 0
    execution_delay = 0.1
    pause_state = False

    head = turtle.Turtle()
    head.shape('upmouth.gif')
    head.penup()
    head.goto(0, 0)
    head.direction = 'stop'

    food = turtle.Turtle()
    food.shape('food.gif')
    food.penup()
    food.goto(0, 100)

    text = turtle.Turtle()
    text.penup()
    text.goto(0, 268)
    text.hideturtle()
    text.color('white')
    text.write('Score:{}  High Score:{}'.format(score, highest_score), font=('courier', 25, 'bold'), align='center')

    segments = []

    game_screen.listen()
    game_screen.onkeypress(go_up, 'Up')
    game_screen.onkeypress(go_down, 'Down')
    game_screen.onkeypress(go_left, 'Left')
    game_screen.onkeypress(go_right, 'Right')

    game_loop()

def move_snake():
    if pause_state:
        return

    if head.direction == 'up':
        y = head.ycor()
        y += 20
        head.sety(y)

    if head.direction == 'down':
        y = head.ycor()
        y -= 20
        head.sety(y)

    if head.direction == 'right':
        x = head.xcor()
        x += 20
        head.setx(x)

    if head.direction == 'left':
        x = head.xcor()
        x -= 20
        head.setx(x)

def go_up():
    if head.direction != 'down':
        head.direction = 'up'
        head.shape('upmouth.gif')

def go_down():
    if head.direction != 'up':
        head.direction = 'down'
        head.shape('downmouth.gif')

def go_left():
    if head.direction != 'right':
        head.direction = 'left'
        head.shape('leftmouth.gif')

def go_right():
    if head.direction != 'left':
        head.direction = 'right'
        head.shape('rightmouth.gif')

def game_loop():
    global count, score, highest_score, execution_delay, pause_state

    while True:
        game_screen.update()

        inner_left_bound = -240
        inner_right_bound = 240
        inner_top_bound = 240
        inner_bottom_bound = -240

        if head.xcor() > inner_right_bound or head.xcor() < inner_left_bound or head.ycor() > inner_top_bound or head.ycor() < inner_bottom_bound:
            game_over()
            count = 0
            food.clear()
            food.shape("food.gif")

            head.goto(0, 0)
            head.direction = 'stop'
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()
            score = 0
            execution_delay = 0.1
            text.clear()
            text.write('Score:{}  High Score:{}'.format(score, highest_score), align='center',
                       font=('courier', 25, 'bold'))

        if head.distance(food) < 20:
            x = random.randint(-255, 255)
            y = random.randint(-255, 255)
            food.goto(x, y)
            winsound.PlaySound("eating-sound-effect-36186.wav", winsound.SND_ASYNC)

            execution_delay -= 0.003

            body = turtle.Turtle()
            body.penup()
            body.shape('body (3).gif')
            segments.append(body)

            count += 1
            if count == 5:
                score += 15  
                count = 0
                pause_state = True
                indicate_bonus()
                time.sleep(pause_duration)
                pause_state = False
            else:
                score += 5

            if score > highest_score:
                highest_score = score
            text.clear()
            text.write('Score:{}  High Score:{}'.format(score, highest_score), font=('courier', 25, 'bold'),
                       align='center')

            if count == 4:
                food.shape("square")
                food.color("black")
                x = random.randint(-200, 200)
                y = random.randint(-200, 200)
                food.goto(x, y)
            else:
                food.shape("food.gif")
                x = random.randint(-200, 200)
                y = random.randint(-200, 200)
                food.goto(x, y)

        for i in range(len(segments) - 1, 0, -1):
            x = segments[i - 1].xcor()
            y = segments[i - 1].ycor()
            segments[i].goto(x, y)

        if len(segments) > 0:
            x = head.xcor()
            y = head.ycor()
            segments[0].goto(x, y)

        move_snake()

        for body in segments:
            if body.distance(head) < 20:
                game_over()
                head.goto(0, 0)
                head.direction = 'stop'
                for segment in segments:
                    segment.goto(1000, 1000)
                segments.clear()
                score = 0
                execution_delay = 0.1
                text.clear()
                text.write('Score:{}  High Score:{}'.format(score, highest_score), align='center',
                           font=('courier', 25, 'bold'))

        time.sleep(execution_delay)

def game_over():
    global highest_score

    if score > highest_score:
        highest_score = score

    with open("highest_score.txt", "w") as file:
        file.write(str(highest_score))

    splash_text = turtle.Turtle()
    splash_text.hideturtle()
    splash_text.color(1, 1, 1)
    splash_text.write("GAME OVER", font=("Courier", 40, "bold"), align="center")

    splash_text.up()
    splash_text.goto(0, -100)
    splash_text.down()
    splash_text.hideturtle()

    splash_text.write("Press any key to start ", font=("Candara", 25, "bold"), align="center")
    splash_text.hideturtle()
    winsound.PlaySound("mixkit-arcade-space-shooter-dead-notification-272.wav", winsound.SND_FILENAME)
    game_screen.update()

    screen.onkeypress(start_game)
    turtle.listen()  
    turtle.mainloop()

def indicate_bonus():
    for _ in range(2):
        game_screen.bgcolor('red')
        time.sleep(0.1)
        game_screen.bgcolor('lightgreen')
        time.sleep(0.1)

screen.onkeypress(start_game, key="Return")
turtle.listen()  
turtle.mainloop()
