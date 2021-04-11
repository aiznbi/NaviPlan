import json
import tkinter.messagebox as mb
import tkinter.simpledialog as dg
from tkinter import *
from PIL import ImageTk

graph = {}
extender = []
buttons_dict = {}

# лист пары координат точки
cords = []
# лист ребер для json
edge = {}
global butt
global i, j
global hall_name, room_name
i = 0
j = 0


# бинд клика на коридор
def add_new_hall():
    ANH = mb.askokcancel(title="Коридор",
                         message="Выберите точки напротив выходов из аудиторий, по окончании нажмите кнопку "
                                 "'Завершить добавление коридора'")
    if ANH:
        canvas.bind("<Button-1>", on_click_hall)
        global i, j
        i = 0
        j += 1
    else:
        canvas.bind("<Button-1>", NONE)


# точки коридоров
def on_click_hall(event):
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    cords = [mouse_x - point_img, mouse_y]
    global i, j
    i += 1
    edge["h" + str(j) + "_e" + str(i)] = cords
    canvas.create_oval(mouse_x - 5, mouse_y - 5, mouse_x + 5, mouse_y + 5, fill="blue", width=2)


# разбинд клика
def exit_anh():
    exitANH = mb.askokcancel(title="Операция завершена",
                             message="Коридор добавлен")
    canvas.bind("<Button-1>", NONE)


def exit_anr():
    exitANR = mb.askokcancel(title="Операция завершена",
                             message="Аудитория добавлена")
    if exitANR:
        global butt
        butt['bg'] = 'pink'
        butt['fg'] = 'black'
        for but in buttons_dict:
            buttons_dict[but]['bg'] = "lightblue"
            buttons_dict[but]['fg'] = "black"


def widname(txt):
    global room_name
    graph[txt].append(room_name)
    graph[room_name].append(txt)
    buttons_dict[txt]['bg'] = "blue"
    buttons_dict[txt]['fg'] = "white"


# загрузка коридоров в json
def load_halls():
    with open("edges.json", "w") as write_file:
        json.dump(edge, write_file)
    exitHalls = mb.askokcancel(title="Операция завершена",
                               message="Коридоры загружены")
    if exitHalls:
        # кнопки коридоров
        for hall in edge:
            buttons_dict[hall] = Button(tk, text=hall, font=("Times New Roman", 14))
            buttons_dict[hall]['command'] = lambda txt=hall: widname(txt)
            buttons_dict[hall]['bg'] = "lightblue"
            buttons_dict[hall].place(x=edge[hall][0] + point_img - 15, y=edge[hall][1] - 15)
    edge.clear()


# бинд клика на аудиторию
def add_new_room():
    ANR = mb.askokcancel(title="Аудитория",
                         message="Выберите аудиторию, затем смежные коридоры")
    if ANR:
        canvas.bind("<Button-1>", on_click_room)
    else:
        canvas.bind("<Button-1>", NONE)


def roomname():
    global room_name
    room_name = dg.askstring(title='Название аудитории', prompt='Введите название аудитории')


# аудиторные вершины
def on_click_room(event):
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    cords = [mouse_x - point_img, mouse_y]
    canvas.bind("<Button-1>", NONE)
    canvas.create_oval(mouse_x - 10, mouse_y - 10, mouse_x + 10, mouse_y + 10, fill="red", width=2)
    roomname()
    global room_name, butt
    butt = Button(tk, text=room_name, font=("Times New Roman", 16), bg='red', fg='white')
    butt.place(x=mouse_x - 15, y=mouse_y - 15)
    graph[room_name] = []
    edge[room_name] = cords


# загрузка аудиторий в json
def load_rooms():
    with open("vertex.json", "w") as write_file:
        json.dump(edge, write_file)
    exitHalls = mb.askokcancel(title="Операция завершена",
                               message="Аудитории загружены")
    with open("graph.json", 'w') as write_file:
        json.dump(graph, write_file)


tk = Tk()
# загрузка img
canvas = Canvas(tk, width=tk.winfo_screenwidth(), height=tk.winfo_screenheight(), bg='white')
canvas.pack(expand=YES, fill=BOTH)
image = ImageTk.PhotoImage(file="plan.gif")
point_img = round(tk.winfo_screenwidth() / 2 - image.width() / 2)
canvas.create_image(tk.winfo_screenwidth() / 2 - image.width() / 2, 0, image=image, anchor=NW)
canvas.create_line(0, image.height(), tk.winfo_screenwidth(), image.height())
# кнопки для коридоров
addNewHall = Button(tk, text="Добавить коридор", command=add_new_hall, font=("Times New Roman", 16))
addNewHall.place(x=tk.winfo_screenwidth() / 4, y=image.height() + 2)
addNewHallExit = Button(tk, text="Завершить добавление коридора", command=exit_anh, font=("Times New Roman", 16))
addNewHallExit.place(x=tk.winfo_screenwidth() / 4, y=image.height() + 43)
ExitHalls = Button(tk, text="Загрузить коридоры", command=load_halls, font=("Times New Roman", 16))
ExitHalls.place(x=tk.winfo_screenwidth() / 4, y=image.height() + 84)
# выгрузка коридоров
with open("edges.json", "r") as read_file:
    edges = json.load(read_file)

# цикл смежности коридоров
i = 1
count = 0
for hall in edges:
    if int(hall[1:2]) == i:
        extender.append(hall)
        count += 1
    else:
        for x in range(count):  # по размеру списка
            list1 = extender.copy()  # копия списка
            list1.remove(extender[x])  # удалить одинаковый
            graph[extender[x]] = list1
            list1 = []  # очистка памяти и списка
        extender.clear()
        extender.append(hall)
        i += 1
        count = 1

# костыль!
for x in range(count):  # по размеру списка
    list1 = extender.copy()  # копия списка
    list1.remove(extender[x])  # удалить одинаковый
    graph[extender[x]] = list1
    list1 = []
extender = []


# конец костыля!


def save_file():
    with open("graph.json", "r") as read_file:
        graph = json.load(read_file)
    with open("edges.json", "r") as read_file:
        edges = json.load(read_file)
    with open("vertex.json", "r") as read_file:
        vertex = json.load(read_file)
    save_dict = {'graph': graph, 'edges': edges, 'vertex': vertex}
    file_name = dg.askstring(title='Сохранение файла', prompt='Введите название файла для сохранения')
    with open(file_name + '.json', "w") as write_file:
        json.dump(save_dict, write_file)


# кнопки для аудиторий
addNewRoom = Button(tk, text="Добавить аудиторию", command=add_new_room, font=("Times New Roman", 16))
addNewRoom.place(x=tk.winfo_screenwidth() / 2, y=image.height() + 2)
addNewHallExit = Button(tk, text="Завершить добавление аудитории", command=exit_anr, font=("Times New Roman", 16))
addNewHallExit.place(x=tk.winfo_screenwidth() / 2, y=image.height() + 43)
ExitRooms = Button(tk, text="Загрузить аудитории", command=load_rooms, font=("Times New Roman", 16))
ExitRooms.place(x=tk.winfo_screenwidth() / 2, y=image.height() + 84)
# кнопка сохранения
savefile = Button(tk, text="Сохранить внесенный план", command=save_file, font=("Times New Roman", 16))
savefile.place(x=tk.winfo_screenwidth() / 2, y=image.height() + 150)
tk.mainloop()
