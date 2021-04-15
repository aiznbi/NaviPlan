import json
import tkinter.messagebox as mb
import tkinter.simpledialog as dg
import tkinter.filedialog as fd
from tkinter import *
from PIL import ImageTk

cords = []
graph = {}
buttons_dict = {}
edge = {}
global file_name, butt, i, j, room_name, hall, flag_hall_room, count, hall1, hall2
count = 0
flag_hall_room = False
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
        global butt, flag_hall_room
        flag_hall_room = False
        butt['bg'] = 'pink'
        butt['fg'] = 'black'
        for but in buttons_dict:
            buttons_dict[but]['bg'] = "lightblue"
            buttons_dict[but]['fg'] = "black"


# лямбда на коридорные кнопки
def widname(txt):
    global flag_hall_room, count
    if flag_hall_room:
        global room_name
        graph[txt].append(room_name)
        graph[room_name].append(txt)
        buttons_dict[txt]['bg'] = "blue"
        buttons_dict[txt]['fg'] = "white"
    else:
        global hall1, hall2
        if count == 0:
            hall1 = txt
            buttons_dict[hall1]['bg'] = "blue"
            buttons_dict[hall1]['fg'] = "white"
            count += 1
        elif count == 1:
            hall2 = txt
            buttons_dict[hall2]['bg'] = "blue"
            buttons_dict[hall2]['fg'] = "white"
            count += 1
            ask = mb.askyesno(title="Стык коридоров", message="Все верно?")
            if ask:
                graph[hall1].append(hall2)
                graph[hall2].append(hall1)
                buttons_dict[hall1]['bg'] = "lightblue"
                buttons_dict[hall1]['fg'] = "black"
                buttons_dict[hall2]['bg'] = "lightblue"
                buttons_dict[hall2]['fg'] = "black"
                count = 0
                mb.showinfo(title="Стык коридоров", message="Успешно")
            else:
                buttons_dict[hall1]['bg'] = "lightblue"
                buttons_dict[hall1]['fg'] = "black"
                buttons_dict[hall2]['bg'] = "lightblue"
                buttons_dict[hall2]['fg'] = "black"
                mb.showwarning(title="Стык коридоров", message="Заново")

# загрузка коридоров в json
def show_halls():
    extender = []
    for hall in edge:
        buttons_dict[hall] = Button(tk, text="*", font=("Times New Roman", 14))
        buttons_dict[hall]['command'] = lambda txt=hall: widname(txt)
        buttons_dict[hall]['bg'] = "lightblue"
        buttons_dict[hall].place(x=edge[hall][0] + point_img - 15, y=edge[hall][1] - 15)
    # цикл смежности коридоров
    i = 1
    cnt = 0
    for hall in edge:
        if int(hall[1:2]) == i:
            extender.append(hall)
            cnt += 1
        else:
            for x in range(cnt):  # по размеру списка
                list1 = extender.copy()  # копия списка
                list1.remove(extender[x])  # удалить одинаковый
                graph[extender[x]] = list1
                list1 = []  # очистка памяти и списка
            extender.clear()
            extender.append(hall)
            i += 1
            cnt = 1
    # костыль!
    for x in range(cnt):  # по размеру списка
        list1 = extender.copy()  # копия списка
        list1.remove(extender[x])  # удалить одинаковый
        graph[extender[x]] = list1
        list1 = []
    extender = []
    with open("edges.json", "w") as write_file:
        json.dump(edge, write_file)
    mb.showinfo(title="Операция завершена", message="Коридоры загружены")
    # конец костыля!
    edge.clear()


def hall_inter():
    hallInter = mb.askokcancel(title="Стык коридоров",
                               message="Выберите две пересекающиеся вершины коридоров")
    if hallInter:
        global count
        count = 0


# бинд клика на аудиторию
def add_new_room():
    ANR = mb.askokcancel(title="Аудитория",
                         message="Выберите аудиторию, затем смежные коридоры")
    global flag_hall_room
    if ANR:
        flag_hall_room = True
        canvas.bind("<Button-1>", on_click_room)
    else:
        flag_hall_room = False
        canvas.bind("<Button-1>", NONE)


# название аудиториии
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
    exitHalls = mb.showinfo(title="Операция завершена",
                            message="Аудитории загружены")
    with open("graph.json", 'w') as write_file:
        json.dump(graph, write_file)


tk = Tk()
global file_name
file_name = fd.askopenfile(filetypes=(('image', '*.gif'),))
file_name = file_name.name[file_name.name.rfind('/') + 1:file_name.name.rfind('.')]
# загрузка img
canvas = Canvas(tk, width=tk.winfo_screenwidth(), height=tk.winfo_screenheight(), bg='white')
canvas.pack(expand=YES, fill=BOTH)
image = ImageTk.PhotoImage(file=file_name + '.gif')
point_img = round(tk.winfo_screenwidth() / 2 - image.width() / 2)
canvas.create_image(tk.winfo_screenwidth() / 2 - image.width() / 2, 0, image=image, anchor=NW)
canvas.create_line(0, image.height(), tk.winfo_screenwidth(), image.height())
# кнопки для коридоров
addNewHall = Button(tk, text="Добавить коридор", command=add_new_hall, font=("Times New Roman", 16))
addNewHall.place(x=tk.winfo_screenwidth() / 4, y=image.height() + 2)
addNewHallExit = Button(tk, text="Завершить добавление коридора", command=exit_anh, font=("Times New Roman", 16))
addNewHallExit.place(x=tk.winfo_screenwidth() / 4, y=image.height() + 43)
ExitHalls = Button(tk, text="Показать коридоры", command=show_halls, font=("Times New Roman", 16))
ExitHalls.place(x=tk.winfo_screenwidth() / 4, y=image.height() + 84)
HallIntersection = Button(tk, text="Добавить смежные коридоры", command=hall_inter, font=("Times New Roman", 16))
HallIntersection.place(x=tk.winfo_screenwidth() / 4, y=image.height() + 125)


def save_file():
    emp = {}
    with open("graph.json", "r") as read_file:
        graph = json.load(read_file)
    with open("edges.json", "r") as read_file:
        edges = json.load(read_file)
    with open("vertex.json", "r") as read_file:
        vertex = json.load(read_file)
    save_dict = {'graph': graph, 'edges': edges, 'vertex': vertex}
    with open(file_name + '.json', "w") as write_file:
        json.dump(save_dict, write_file)
    with open("graph.json", "w") as write_file:
        json.dump(emp, write_file)
    with open("edges.json", "w") as write_file:
        json.dump(emp, write_file)
    with open("vertex.json", "w") as write_file:
        json.dump(emp, write_file)
    mb.showinfo(title="Операция завершена", message="План успешно добавлен!")


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
