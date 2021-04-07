from tkinter import *
import tkinter.messagebox as mb
import json
import self as self
from PIL import ImageTk, Image

graph = {}
extender = []

# лист пары координат точки
cords = []
# лист ребер для json
edge = {}
global i, j
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


# загрузка коридоров в json
def load_halls():
    with open("edges.json", "w") as write_file:
        json.dump(edge, write_file)
    exitHalls = mb.askokcancel(title="Операция завершена",
                               message="Коридоры загружены")
    if exitHalls:
        # кнопки коридоров
        for hall in edges:
            Button(tk, text=hall, activebackground="blue", font=("Times New Roman", 14)).place(
                x=edges[hall][0] + point_img - 15, y=edges[hall][1] - 15)
        edge.clear()


# бинд клика на аудиторию
def add_new_room():
    ANR = mb.askokcancel(title="Аудитория",
                         message="Выберите аудиторию, затем смежные коридоры")
    if ANR:
        graph[room_name.get()] = []
        canvas.bind("<Button-1>", on_click_room)
    else:
        canvas.bind("<Button-1>", NONE)


# аудиторные вершины
def on_click_room(event):
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    cords = [mouse_x - point_img, mouse_y]
    edge[txt.get()] = cords
    canvas.create_oval(mouse_x - 10, mouse_y - 10, mouse_x + 10, mouse_y + 10, fill="red", width=2)


# разбинд клика
def exit_anr():
    exitANH = mb.askokcancel(title="Операция завершена",
                             message="Аудитория добавлена")
    canvas.bind("<Button-1>", NONE)
    room_name.set("")


# загрузка аудиторий в json
def load_rooms():
    with open("vertex.json", "w") as write_file:
        json.dump(edge, write_file)
    exitHalls = mb.askokcancel(title="Операция завершена",
                               message="Аудитории загружены")
    with open("graph.json", 'w') as write_file:
        json.dump(graph, write_file)
    tk.destroy()


# функция для коридора
def addHall():
    graph[hall_name.get()].append(room_name.get())
    graph[room_name.get()].append(hall_name.get())
    hall_name.set("")


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
del list1
extender = []
# конец костыля!

# кнопки для аудиторий
room_name = StringVar()
canvas.create_text(tk.winfo_screenwidth() / 2, image.height() + 10, text="Название аудитории",
                   font=("Times New Roman", 16))
txt = Entry(tk, width=15, font=("Times New Roman", 16), bd=3, bg="#bbbbbb", justify=CENTER, textvariable=room_name)
txt.place(x=tk.winfo_screenwidth() / 2 - 85, y=image.height() + 25)
addNewRoom = Button(tk, text="Добавить", command=add_new_room, font=("Times New Roman", 16))
addNewRoom.place(x=tk.winfo_screenwidth() / 2 - 110, y=image.height() + 55)
addNewRoomExit = Button(tk, text="Завершить", command=exit_anr, font=("Times New Roman", 16))
addNewRoomExit.place(x=tk.winfo_screenwidth() / 2, y=image.height() + 55)
ExitRooms = Button(tk, text="Загрузить аудитории", command=load_rooms, font=("Times New Roman", 16))
ExitRooms.place(x=tk.winfo_screenwidth() / 2 - 98, y=image.height() + 95)
# костыль для смежных коридоров
hall_name = StringVar()
canvas.create_text(tk.winfo_screenwidth() / 2 + 225, image.height() + 10, text="Смежный коридор",
                   font=("Times New Roman", 16))
text = Entry(tk, width=8, font=("Times New Roman", 16), bd=3, bg="#bbbbbb", justify=CENTER, textvariable=hall_name)
text.place(x=tk.winfo_screenwidth() / 2 + 180, y=image.height() + 25)
addHall = Button(tk, text="Добавить", command=addHall, font=("Times New Roman", 16))
addHall.place(x=tk.winfo_screenwidth() / 2 + 175, y=image.height() + 55)
tk.mainloop()
