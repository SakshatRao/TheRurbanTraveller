import tkinter
import time
import numpy as np
import pickle
import datetime
from PIL import ImageTk, Image
import multiprocessing
from pygame import mixer

Window_Width = 1500
Window_Height = 800

memories_dict = pickle.load(open('./Memories/Processed_Data/memories.pickle', 'rb'))

def create_animation_window():
    Window = tkinter.Tk()
    Window.title("Python Guides")

    Window.geometry(f'{Window_Width}x{Window_Height}')
    return Window
 
def create_animation_canvas(Window):
    canvas = tkinter.Canvas(Window)
    canvas.configure(bg = "white")
    canvas.pack(fill = "both", expand = True)
    return canvas

def scale_xaxis(x):
    return ((x - 72) / (75 - 72)) * Window_Width

def scale_yaxis(y):
    return Window_Height - ((y - 17) / (20 - 17)) * Window_Height
 
def animate_car(Window, canvas, memories_dict):
    iter_cnt = 0
    # bg_img_file = ImageTk.PhotoImage(Image.open("./Memories/Animation/Images/map.jpg").resize((1000, 800)))
    # bg_img = canvas.create_image(750, 400, anchor = tkinter.CENTER, image = bg_img_file)
    memory = memories_dict[f"Phase{iter_cnt}"]
    next_memory = memories_dict[f"Phase{iter_cnt + 1}"]
    car_file_se = tkinter.PhotoImage(file = "./Memories/Animation/Images/pickup-truck_SE.png")
    car_file_se = car_file_se.subsample(5)
    car_file_sw = tkinter.PhotoImage(file = "./Memories/Animation/Images/pickup-truck_SW.png")
    car_file_sw = car_file_sw.subsample(5)
    car_file_ne = tkinter.PhotoImage(file = "./Memories/Animation/Images/pickup-truck_NE.png")
    car_file_ne = car_file_ne.subsample(5)
    car_file_nw = tkinter.PhotoImage(file = "./Memories/Animation/Images/pickup-truck_NW.png")
    car_file_nw = car_file_nw.subsample(5)
    car = canvas.create_image(scale_xaxis(memory['gps'][1]), scale_yaxis(memory['gps'][0]), anchor = tkinter.CENTER, image = car_file_se)
    status_label = canvas.create_text(750, 20, text = "", fill = 'black')
    curr_time = datetime.datetime(2022, 1, 14, 0, 0, 0)
    time_label = canvas.create_text(750, 40, text = datetime.datetime.strftime(curr_time, "%b %d, %Y (%a) - %I:%M %p"), fill = 'black')
    imgs = []
    lines = []
    city_names = []
    Window.update()
    curr_img = None
    while True:
        time.sleep(0.25)
        delta_y = scale_yaxis(next_memory['gps'][0]) - scale_yaxis(memory['gps'][0])
        delta_x = scale_xaxis(next_memory['gps'][1]) - scale_xaxis(memory['gps'][1])
        if((delta_x > 0) and (delta_y > 0)):
            canvas.itemconfig(car, image = car_file_se)
        elif((delta_x < 0) and (delta_y > 0)):
            canvas.itemconfig(car, image = car_file_sw)
        elif((delta_x > 0) and (delta_y < 0)):
            canvas.itemconfig(car, image = car_file_ne)
        elif((delta_x < 0) and (delta_y < 0)):
            canvas.itemconfig(car, image = car_file_nw)
        canvas.move(car, delta_x, delta_y)

        update_text = ""
        if(memory['status'] == 'Travel'):
            start_loc = ""
            end_loc = ""
            for idx in np.arange(iter_cnt - 1, -1, -1):
                if(memories_dict[f"Phase{idx}"]['status'] == 'Stop'):
                    start_loc = memories_dict[f"Phase{idx}"]['city']
                    break
            for idx in np.arange(iter_cnt + 1, len(memories_dict), 1):
                if(memories_dict[f"Phase{idx}"]['status'] == 'Stop'):
                    end_loc = memories_dict[f"Phase{idx}"]['city']
                    break
            update_text = f"Travelling from {start_loc} to {end_loc}"
        else:
            update_text = f"Stop at {memory['city']}"
            city_name = canvas.create_text(scale_xaxis(memory['gps'][1]), scale_yaxis(memory['gps'][0]), text = memory['city'], anchor = tkinter.CENTER, fill = 'red', font = ("Arial", 25))
            city_names.append(city_name)
        curr_time = curr_time + datetime.timedelta(minutes = 30)
        canvas.itemconfig(time_label, text = datetime.datetime.strftime(curr_time, "%b %d, %Y (%a) - %I:%M %p"))
        canvas.itemconfig(status_label, text = update_text)
        # for img in imgs:
        #     canvas.delete(img)
        car_x, car_y = canvas.coords(car)
        for img_idx, img in enumerate(memory['images']):
            if(img_idx > 0):
                print("<<<<<<<<>>>>>>>")
            img_file = ImageTk.PhotoImage(Image.open(f"./Memories/Images/stock-image-{img + 1}.jpg"))
            imgs.append(img_file)
            curr_img = canvas.create_image(car_x + 100 * img_idx, car_y + 100, anchor = tkinter.N, image = img_file)
        line = canvas.create_line(scale_xaxis(memory['gps'][1]), scale_yaxis(memory['gps'][0]), scale_xaxis(next_memory['gps'][1]), scale_yaxis(next_memory['gps'][0]), width = 4, fill = 'black')
        lines.append(line)
        for line in lines:
            canvas.tag_raise(line)
        for city_name in city_names:
            canvas.tag_raise(city_name)
        canvas.tag_raise(car)
        Window.update()
        iter_cnt += 1
        if(iter_cnt == len(memories_dict) - 1):
            break
        memory = memories_dict[f"Phase{iter_cnt}"]
        next_memory = memories_dict[f"Phase{iter_cnt + 1}"]
    # mixer.music.stop()

Animation_Window = create_animation_window()
Animation_canvas = create_animation_canvas(Animation_Window)
# mixer.init()
# mixer.music.load('./Memories/Animation/Bailando.mp3')
# def play_music():
#     mixer.music.play()
#     mixer.music.set_volume(0.7)
# t = multiprocessing.Process(target = play_music)
# t.start()
animate_car(Animation_Window, Animation_canvas, memories_dict)