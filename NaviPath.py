import json
from collections import deque
import tkinter.messagebox as mb
from tkinter import *
from PIL import ImageTk


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


tk = Tk()
# загрузка img
canvas = Canvas(tk, width=tk.winfo_screenwidth(), height=tk.winfo_screenheight(), bg='white')
canvas.pack(expand=YES, fill=BOTH)
image = ImageTk.PhotoImage(file="plan.gif")
point_img = round(tk.winfo_screenwidth() / 2 - image.width() / 2)
canvas.create_image(tk.winfo_screenwidth() / 2 - image.width() / 2, 0, image=image, anchor=NW)
canvas.create_line(0, image.height(), tk.winfo_screenwidth(), image.height())
# распаковка json
with open("graph.json", "r") as read_file:
    graph = json.load(read_file)
with open("edges.json", "r") as read_file:
    edges = json.load(read_file)
with open("vertex.json", "r") as read_file:
    vertex = json.load(read_file)
# лист для выпадающего списка
OptList_from = []
OptList_where = []
# создание кнопок
for room in vertex:
    Button(tk, text=room, font=("Times New Roman", 16)).place(x=vertex[room][0] - 15 + point_img,
                                                              y=vertex[room][1] - 15)
    OptList_from.append(room)
    OptList_where.append(room)
var_from = StringVar(tk)
var_from.set("Откуда")
opt_from = OptionMenu(tk, var_from, *OptList_from)
opt_from.config(width=15, font=('Times New Roman', 20))
opt_from.update()
opt_from.place(x=tk.winfo_screenwidth()/2-opt_from.winfo_reqwidth(), y=image.height() + 5)
var_where = StringVar(tk)
var_where.set("Куда")
opt_where = OptionMenu(tk, var_where, *OptList_where)
opt_where.config(width=15, font=('Times New Roman', 20))
opt_where.place(x=tk.winfo_screenwidth()/2, y=image.height() + 5)
"""path = shortest_path(graph, "102", "103")
way = []
for i in path:
    if edges.get(i) is None:
        way.append(vertex.get(i))
    else:
        way.append(edges.get(i))
for i in way:
    i[0] += point_img
canvas.create_oval(way[0][0] - 20, way[0][1] - 20, way[0][0] + 20, way[0][1] + 20, fill="green")
canvas.create_oval(way[len(way) - 1][0] - 20, way[len(way) - 1][1] - 20, way[len(way) - 1][0] + 20,
                   way[len(way) - 1][1] + 20, fill="red")
for i in range(len(way) - 1):
    canvas.create_line(way[i], way[i + 1], width=5, fill="blue")
"""
tk.mainloop()
