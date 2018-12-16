from tkinter.filedialog import *
from tkinter.messagebox import *
import json
import helper

app = Tk()
ActorWithActors = {}
ActorWithFilms = {}
FilmsWithYears = {}


def load_data():
    opened_file = askopenfile(defaultextension=".json", filetypes=[("All types", ".json")])

    if not opened_file:
        return

    actor_name = "Kevin Bacon"
    read_json = json.loads(opened_file.read())

    list_box.delete(0, END)

    for item in read_json:
        if actor_name != item['name']:
            continue
        parse_loaded_data(item, read_json)

    for item in read_json:
        if actor_name == item['name']:
            continue
        parse_loaded_data(item, read_json)


def parse_loaded_data(item, read_json):
    list_box.insert(END, item['name'])
    films = ''
    for film in item['films']:
        films = "{},,{}".format(films, film['title'])

        if film['title'] not in FilmsWithYears.keys():
            FilmsWithYears[film['title']] = film['year']

    ActorWithActors[item['name']] = helper.get_actors(read_json, item['films'], item['name'])
    ActorWithFilms[item['name']] = films.split(',,')[1:]


def find_bacon_number():
    selected = list_box.curselection()

    if list_box.size() and len(selected):
        result = helper.build_result(ActorWithFilms, ActorWithActors, FilmsWithYears, selected[0])
        showinfo("Число Бейкона", result)
    return


f = Frame()
f.pack(side=LEFT, padx=25)
Button(f, text="Загрузить данные", command=load_data).pack(fill=X)
Button(f, text="Найти число Бейкона", command=find_bacon_number).pack(fill=X)

list_box = Listbox(width=35, height=20)
list_box.pack(side=RIGHT)
scroll = Scrollbar(command=list_box.yview())
scroll.pack(side=RIGHT, fill=Y)
list_box.config(yscrollcommand=scroll.set)

app.mainloop()
