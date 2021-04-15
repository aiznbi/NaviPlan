import json
from collections import deque
import tkinter.filedialog as fd
from tkinter import *
import copy
from PIL import ImageTk

way = []
buttons_dict = {}


def bfs_paths(graph, start, goal):
    queue = deque([(start, [start])])
    while queue:
        (vertex, path) = queue.pop()
        for next in set(graph[vertex]) - set(path):
            if next == goal:
                yield path + [next]
            else:
                queue.appendleft((next, path + [next]))


def shortest_path(graph, start, goal):
    try:
        return next(bfs_paths(graph, start, goal))
    except StopIteration:
        return None


def root(mas):
    for i in range(len(way) - 1):
        canvas.create_line(way[i], way[i + 1], width=5, fill="white")
    vertex_cop = copy.deepcopy(vertex)
    edges_cop = copy.deepcopy(edges)
    path = shortest_path(graph, mas[0], mas[1])
    print(path)
    way.clear()
    for i in path:
        if edges_cop.get(i) is None:
            way.append(vertex_cop.get(i))
        else:
            way.append(edges_cop.get(i))
    for i in way:
        i[0] += point_img
    for i in range(len(way) - 1):
        canvas.create_line(way[i], way[i + 1], width=5, fill="blue")


def callback(*args):
    for but in buttons_dict:
        buttons_dict[but]['bg'] = 'lightblue'
    buttons_dict[var_from.get()]['bg'] = 'lightgreen'
    buttons_dict[var_where.get()]['bg'] = 'pink'
    if var_from.get() != 'Откуда' and var_where.get() != 'Куда':
        for_root = var_from.get(), var_where.get()
        root(for_root)


tk = Tk()
file_name = fd.askopenfile(filetypes=(('image', '*.gif'),))
file_name = file_name.name[file_name.name.rfind('/')+1:file_name.name.rfind('.')]
# загрузка img
canvas = Canvas(tk, width=tk.winfo_screenwidth(), height=tk.winfo_screenheight(), bg='white')
canvas.pack(expand=YES, fill=BOTH)
image = ImageTk.PhotoImage(file=file_name+'.gif')
point_img = round(tk.winfo_screenwidth() / 2 - image.width() / 2)
canvas.create_image(tk.winfo_screenwidth() / 2 - image.width() / 2, 0, image=image, anchor=NW)
canvas.create_line(0, image.height(), tk.winfo_screenwidth(), image.height())
# распаковка json
with open(file_name+'.json', 'r') as read_file:
    save_dict = json.load(read_file)
graph = save_dict['graph']
edges = save_dict['edges']
vertex = save_dict['vertex']
# лист для выпадающего списка
OptList_from = []
OptList_where = []
# создание кнопок
for room in vertex:
    buttons_dict[room] = Button(tk, text=room, font=("Times New Roman", 16))
    buttons_dict[room]['bg'] = 'lightblue'
    buttons_dict[room].place(x=vertex[room][0] - 15 + point_img, y=vertex[room][1] - 15)
    OptList_from.append(room)
    OptList_where.append(room)
var_from = StringVar(tk)
var_from.set("Откуда")
opt_from = OptionMenu(tk, var_from, *OptList_from)
opt_from.config(width=15, font=('Times New Roman', 20), bg='lightgreen')
opt_from.update()
opt_from.place(x=tk.winfo_screenwidth() / 2 - opt_from.winfo_reqwidth(), y=image.height() + 5)
var_from.trace("w", callback)
var_where = StringVar(tk)
var_where.set("Куда")
opt_where = OptionMenu(tk, var_where, *OptList_where)
opt_where.config(width=15, font=('Times New Roman', 20), bg='pink')
opt_where.place(x=tk.winfo_screenwidth() / 2, y=image.height() + 5)
var_where.trace("w", callback)
tk.mainloop()
