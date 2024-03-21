import tkinter as tk
from tkinter import PhotoImage, simpledialog
from PIL import Image, ImageTk
import random

root = tk.Tk()
root.title("Clicker")
canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()
images = []
images_list = ["clicker.png", "clicker2.png"]

counter = 1
autoclicks = 0
collecter = 0
first_price = 10
second_price = 10
third_price = 100
image_path = ''
click_count = 0

colors_list = ["red", "orange", "purple", "white", "yellow", "green", "pink"]
sizes_list = [4, 6, 8, 10]
particles_list = []

def create_particle(canvas, size, color, x, y):
    id = canvas.create_oval(x, y, x + size, y + size, fill=color)
    vx = random.uniform(-3, 3)
    vy = random.uniform(-8, -2)
    gravity = 0.2
    return id, vx, vy, gravity

def move_particle(canvas, particle):
    id, vx, vy, gravity = particle
    canvas.move(id, vx, vy)
    vy += gravity
    return id, vx, vy, gravity

def create_firework(event):
    x = event.x
    y = event.y
    color = random.choice(colors_list)
    size = random.choice(sizes_list)
    for _ in range(50):
        particle = create_particle(canvas, size, color, x, y)
        particles_list.append(particle)

def spawn_image(event):
    global click_count, image_path
    click_count += counter
    update_click_counter()
    x, y = event.x, event.y
    image_path = random.choice(images_list)

    original_image = Image.open(image_path)
    width, height = original_image.size
    coef = random.uniform(0.1, 2.0)
    new_width = int(width * coef)
    new_height = int(height * coef)
    resized_image = original_image.resize((new_width, new_height), Image.BICUBIC)

    falling_image = ImageTk.PhotoImage(resized_image)
    image_id = canvas.create_image(x, y, image=falling_image, anchor=tk.CENTER)
    speed = random.uniform(1, 5)
    images.append((falling_image, image_id, speed, x, y))
    update_mini_image()
    create_firework(event)

def upgrade1_action():
    global first_price, click_count, counter
    if click_count >= first_price:
        click_count -= first_price
        first_price *= 3
        counter += 1
        update_click_counter()

def upgrade2_action():
    global second_price, click_count, autoclicks
    if click_count >= second_price:
        click_count -= second_price
        second_price *= 3
        autoclicks += 0.01
        update_click_counter()

def show_upgrades():
    upgrades_dialog = tk.Toplevel(root)
    upgrades_dialog.title("Upgrades")
    upgrades_actions = [
        ("1. Increase tap +1", first_price, upgrade1_action),
        ("2. Autoclicks +1", second_price, upgrade2_action)
    ]
    for i, upgrade in enumerate(upgrades_actions):
        tk.Button(upgrades_dialog, text=upgrade[0] + ", Price: " + str(upgrade[1]), font=("Arial", 12), command=upgrade[2]).pack(pady=5)

canvas.bind("<Button-1>", spawn_image)
click_counter_var = tk.StringVar()
click_counter_label = tk.Label(root, textvariable=click_counter_var, font=("Helvetica", 14))
click_counter_label.pack()
mini_image_label = tk.Label(root)
mini_image_label.place(x=40, y=10)
tk.Button(root, text="Show upgrades", command=show_upgrades).pack(pady=10)

def auto_clicker():
    global autoclicks, click_count, collected
    click_count += int(autoclicks)
    if click_count > 1:
        click_count = 0
        y = random.randint(0, 600)  # Adjusted to canvas height
        x = random.randint(0, 800)  # Adjusted to canvas width
        my_event = type('Event', (object,), {'x': x, 'y': y})
        spawn_image(my_event)
    update_click_counter()

def update_click_counter():
    click_counter_var.set(str(click_count))

def update_mini_image():
    if images:
        global image_path
        mini_image, _, _, _, _ = images[-1]
        pil_image = Image.open(image_path)
        pil_image = pil_image.resize((50,50), Image.BICUBIC)
        mini_image = ImageTk.PhotoImage(pil_image)
        mini_image_label.config(image=mini_image)
        mini_image_label.image = mini_image


def update():
    global images, particles_list
    new_images = []
    new_particles= []
    for info in images:
        falling_image, image_id, speed, x, y = info
        canvas.move(image_id, 0, speed)
        if canvas.coords(image_id)[1] < 600:
            new_images.append((falling_image, image_id, speed, x, y))

    for particle in particles_list:
        new_particle = move_particle(canvas, particle)
        x, y, _, _ = canvas.coords(new_particle[0])
        if y < 600:
            new_particles.append(new_particle)
        else:
            canvas.delete(new_particle[0])
    images = new_images
    update_mini_image()
    auto_clicker()
    root.after(10, update)

update()
root.mainloop()
