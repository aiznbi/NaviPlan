from collections import deque
from mailbox import mbox
from tkinter import *
import tkinter.messagebox as mb
import json
import self as self
from PIL import ImageTk, Image
import self as self
from PIL.ImageWin import Window


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


def in_out():
    mb.askquestion(title="Выбор")

# господи как пользоваться гитхабом

tk = Tk()
# загрузка img
canvas = Canvas(tk, width=tk.winfo_screenwidth(), height=tk.winfo_screenheight(), bg='white')
canvas.pack(expand=YES, fill=BOTH)
self.image = ImageTk.PhotoImage(file="plan.gif")
point_img = round(tk.winfo_screenwidth() / 2 - self.image.width() / 2)
canvas.create_image(tk.winfo_screenwidth() / 2 - self.image.width() / 2, 0, image=self.image, anchor=NW)
canvas.create_line(0, self.image.height(), tk.winfo_screenwidth(), self.image.height())
with open("graph.json", "r") as read_file:
    graph = json.load(read_file)
with open("edges.json", "r") as read_file:
    edges = json.load(read_file)
with open("vertex.json", "r") as read_file:
    vertex = json.load(read_file)
for room in vertex:
    Button(tk, text=room, command=in_out, font=("Times New Roman", 16)).place(x=vertex[room][0]-15 + point_img, y=vertex[room][1]-15)
path = shortest_path(graph, "102", "103")
way = []
for i in path:
    if edges.get(i) is None:
        way.append(vertex.get(i))
    else:
        way.append(edges.get(i))
for i in way:
    i[0] += point_img
canvas.create_oval(way[0][0]-20, way[0][1]-20, way[0][0]+20, way[0][1]+20, fill="green")
canvas.create_oval(way[len(way)-1][0]-20, way[len(way)-1][1]-20, way[len(way)-1][0]+20, way[len(way)-1][1]+20, fill="red")
for i in range(len(way)-1):
    canvas.create_line(way[i], way[i+1], width=5, fill="blue")

tk.mainloop()
