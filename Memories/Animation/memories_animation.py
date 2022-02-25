import tkinter
import time
import numpy as np
import pickle
import datetime
from PIL import ImageTk, Image
import multiprocessing
from pydub import AudioSegment 
from pydub.playback import play

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
    canvas.configure(bg = "black")
    canvas.pack(fill = "both", expand = True)
    return canvas
 
def animate_car(Window, canvas, memories_dict, win):
    iter_cnt = 0
    MAX_LAT = -1
    MAX_LON = -1
    MIN_LAT = 10000
    MIN_LON = 10000

    for memory in memories_dict:
        curr_gsp = memories_dict[memory]['gps']
        if(curr_gsp[0] > MAX_LAT):
            MAX_LAT = curr_gsp[0]
        if(curr_gsp[0] < MIN_LAT):
            MIN_LAT = curr_gsp[0]
        if(curr_gsp[1] > MAX_LON):
            MAX_LON = curr_gsp[1]
        if(curr_gsp[1] < MIN_LON):
            MIN_LON = curr_gsp[1]
    
    MAX_LAT += 0.5
    MAX_LON += 0.5
    MIN_LON -= 0.5
    MIN_LAT -= 0.5
    
    def scale_xaxis(x):
        return ((x - MIN_LON) / (MAX_LON - MIN_LON)) * Window_Width

    def scale_yaxis(y):
        return Window_Height - ((y - MIN_LAT) / (MAX_LAT - MIN_LAT)) * Window_Height

    memory = memories_dict[f"Phase{iter_cnt}"]
    next_memory = memories_dict[f"Phase{iter_cnt + 1}"]
    car_img_file = Image.open("./Memories/Animation/Images/pickup-truck_SE.png").resize((100, 100))
    car_file = ImageTk.PhotoImage(car_img_file.rotate(30))
    car = canvas.create_image(scale_xaxis(memory['gps'][1]), scale_yaxis(memory['gps'][0]), anchor = tkinter.CENTER, image = car_file)
    func_images = []
    def create_rectangle(x,y,a,b,**options):
        if 'alpha' in options:
            # Calculate the alpha transparency for every color(RGB)
            alpha = int(options.pop('alpha') * 255)
            # Use the fill variable to fill the shape with transparent color
            fill = options.pop('fill')
            fill = win.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (a-x, b-y), fill)
            func_images.append(ImageTk.PhotoImage(image))
            canvas.create_image(x, y, image=func_images[-1], anchor='nw')
            canvas.create_rectangle(x, y,a,b, **options)
    create_rectangle(0, 0, Window_Width, Window_Height, fill = 'black', alpha = 0.5)
    create_rectangle(600, 10, 900, 50, fill = 'black', alpha = 0.75)
    status_label = canvas.create_text(750, 20, text = "", fill = 'white', font = ("Arial", 15))
    curr_time = datetime.datetime(2022, 1, 14, 0, 0, 0)
    time_label = canvas.create_text(750, 40, text = datetime.datetime.strftime(curr_time, "%b %d, %Y (%a) - %I:%M %p"), fill = 'white', font = ("Arial", 15))
    imgs = []
    lines = []
    city_names = []

    NUM_ROWS = -1
    NUM_COLS = -1
    
    all_prods = []
    for i in range(1, 11):
        for j in range(1, 11):
            all_prods.append(i * j)
    
    num_imgs = 0
    for memory_inst in memories_dict:
        num_imgs += len(memories_dict[memory_inst]['images'])
    print(num_imgs)
    while(1):
        if(num_imgs in all_prods):
            NUM_ROWS = all_prods.index(num_imgs) // 10 + 1
            NUM_COLS = all_prods.index(num_imgs) % 10 + 1
            break
        else:
            num_imgs -= 1
    print(NUM_ROWS, NUM_COLS)
    
    img_pos = np.arange(num_imgs)
    np.random.shuffle(img_pos)
    img_pos_idx = 0

    loc_names = set()

    Window.update()
    curr_img = None
    while True:
        time.sleep(0.25)
        delta_y = scale_yaxis(next_memory['gps'][0]) - scale_yaxis(memory['gps'][0])
        delta_x = scale_xaxis(next_memory['gps'][1]) - scale_xaxis(memory['gps'][1])
        ANGLE_OFFSET = 25
        if((delta_x == 0) and (delta_y == 0)):
            angle = np.pi / 180 * ANGLE_OFFSET
        else:
            if((delta_x > 0) and (delta_y > 0)):
                angle = np.pi / 180 * ANGLE_OFFSET - np.arctan(delta_y / delta_x)
                car_file = ImageTk.PhotoImage(car_img_file.rotate(angle * 180 / np.pi))
            elif((delta_x > 0) and (delta_y < 0)):
                angle = np.pi / 180 * ANGLE_OFFSET + np.arctan(-delta_y / delta_x)
                car_file = ImageTk.PhotoImage(car_img_file.rotate(angle * 180 / np.pi))
            elif((delta_x < 0) and (delta_y > 0)):
                angle = -np.pi / 180 * ANGLE_OFFSET + np.arctan(delta_y / -delta_x)
                car_file = ImageTk.PhotoImage(car_img_file.transpose(Image.FLIP_LEFT_RIGHT).rotate(angle * 180 / np.pi))
            elif((delta_x < 0) and (delta_y < 0)):
                angle = -np.pi / 180 * ANGLE_OFFSET - np.arctan(delta_y / delta_x)
                car_file = ImageTk.PhotoImage(car_img_file.transpose(Image.FLIP_LEFT_RIGHT).rotate(angle * 180 / np.pi))
        canvas.itemconfig(car, image = car_file)
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
            if(memory['city'] not in loc_names):
                city_name = canvas.create_text(scale_xaxis(memory['gps'][1]), scale_yaxis(memory['gps'][0]), text = memory['city'], anchor = tkinter.CENTER, fill = 'red', font = ("Arial", 25))
                city_names.append(city_name)
                loc_names.add(memory['city'])
        curr_time = curr_time + datetime.timedelta(minutes = 30)
        canvas.itemconfig(time_label, text = datetime.datetime.strftime(curr_time, "%b %d, %Y (%a) - %I:%M %p"))
        canvas.itemconfig(status_label, text = update_text)
        # for img in imgs:
        #     canvas.delete(img)
        car_x, car_y = canvas.coords(car)
        for img_idx, img in enumerate(memory['images']):
            img_file = ImageTk.PhotoImage(Image.open(f"./Memories/Images/stock-image-{img + 1}.jpg").resize((Window_Width // NUM_COLS, Window_Height // NUM_ROWS)))
            imgs.append(img_file)
            # canvas.create_image(car_x + 100 * img_idx, car_y + 100, anchor = tkinter.CENTER, image = img_file2)
            if(img_pos_idx == NUM_ROWS * NUM_COLS - 1):
                continue
            curr_img = canvas.create_image((img_pos[img_pos_idx] % NUM_COLS) * Window_Width / NUM_COLS, (img_pos[img_pos_idx] // NUM_COLS) * Window_Height / NUM_ROWS, anchor = tkinter.NW, image = img_file)
            canvas.tag_lower(curr_img)
            img_pos_idx += 1
        line = canvas.create_line(scale_xaxis(memory['gps'][1]), scale_yaxis(memory['gps'][0]), scale_xaxis(next_memory['gps'][1]), scale_yaxis(next_memory['gps'][0]), width = 4, fill = 'white')
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
    time.sleep(5)
    t.terminate()

wav_file = AudioSegment.from_file(file = "./Memories/Animation/bg_music.mp3", format = "mp3")
t = multiprocessing.Process(target = play, args = (wav_file, ))
t.start()
win = Animation_Window = create_animation_window()
Animation_canvas = create_animation_canvas(Animation_Window)
animate_car(Animation_Window, Animation_canvas, memories_dict, win)