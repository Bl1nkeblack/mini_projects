from tkinter import *
from PIL import Image, ImageTk
import requests
import io
from tkinter import filedialog
from tkinter import ttk


window = Tk()
window.title("PICTURE PROGRAMM")

notebook = ttk.Notebook(window)
notebook.grid(row=0, column=0, sticky="nsew")


#Функции для первой вкладки(URL request)
def Open_Button():
    global window
    global frame_tab_1
    Entry_Adress_Data = Entry_Adress.get()
    image = place_image_on_button(Entry_Adress_Data, frame_tab_1, width=350, height=250)
    button_Picture = Button(master=frame_tab_1, width=350, height=250, image=image)
    button_Picture.grid(column=1, row=1)


def place_image_on_button(url, parent, width, height):
    global frame_tab_1
    response = requests.get(url)
    image_data = response.content
    image = Image.open(io.BytesIO(image_data))
    resized_image = image.resize((width, height))
    photo = ImageTk.PhotoImage(resized_image)

    button_Picture = Button(master=frame_tab_1, width=350, height=250, image=photo)
    button_Picture.config(image=photo)
    button_Picture.image = photo
    button_Picture.grid(column=1, row=1, columnspan=3)
    return image


def search_images():
    width = int(Entry_Width.get())
    height = int(Entry_Height.get())
    query = Entry_Search.get()
    responses = []
    for _ in range(width * height):
        response = requests.get(f"https://source.unsplash.com/random/?{query}")
        responses.append(response.content)
    images = []
    row = 0
    column = 0
    for response in responses:
        image = Image.open(io.BytesIO(response))
        resized_image = image.resize((200, 200))
        photo = ImageTk.PhotoImage(resized_image)
        images.append([photo, column, row])
        column += 1
        if column > width:
            column = 0
            row += 1
    for i, line in enumerate(images):
        button = Button(master=frame_tab_2, image=line[0])
        button.grid(row=line[2] +2, column=line[1], columnspan=1)
        button.image = line[0]
def save_image_to_disk(image, file_path):
    try:
        image.save(file_path)
        print("Image saved successfully at:", file_path)
    except Exception as e:
        print("An error occurred while saving the image:", e)


def button_download():
    image = place_image_on_button(Entry_Adress.get(), window, 410, 235)
    save_image_to_disk(image, file_path=Entry_Path.get())

def button_choose_path():
    Entry_Path.insert(END, filedialog.askdirectory())



# Добавляем вкладки
frame_tab_1 = ttk.Frame(notebook)
frame_tab_2 = ttk.Frame(notebook, width=10000, height=10000)

frame_tab_1.grid(row=0, column=0, sticky="nsew")
frame_tab_2.grid(row=0, column=0, sticky="nsew")

notebook.add(frame_tab_1, text="URL request")
notebook.add(frame_tab_2, text="Search")
#Кнопки для Первой Вкладки(URL requests)
Label_Open = Label(master=frame_tab_1, text="Picture Adress")
Label_Open.grid(column=0, row=0)
Label_Picrure = Label(master=frame_tab_1, text="There is your picture")
Label_Picrure.grid(column=0, row=1)
Label_Answer = Label(master=frame_tab_1, text="Your Path")
Label_Answer.grid(column=0, row=2)
button_Open = Button(text="Open", master=frame_tab_1, width=35, command=Open_Button)
button_Open.grid(column=2, row=0, columnspan=2)
button_Download = Button(text="Download", master=frame_tab_1, width=17, command=button_download)
button_Download.grid(column=2, row=2)
button_choose_path = Button(text="Choose path",master=frame_tab_1, width=17, command=button_choose_path)
button_choose_path.grid(column=3, row=2)
Entry_Adress = Entry(master=frame_tab_1, width=55)
Entry_Adress.grid(column=1, row=0)
Entry_Path = Entry(master=frame_tab_1, width=55)
Entry_Path.grid(column=1, row=2)
#Кнопки для Второй Вкладки(Search)
Entry_Search = Entry(master=frame_tab_2, width=75)
Entry_Search.grid(column=1, row=0, columnspan=4)
Entry_Width = Entry(master=frame_tab_2, width=20)
Entry_Width.grid(column=1, row=1)
Entry_Height = Entry(master=frame_tab_2, width=20)
Entry_Height.grid(column=2, row=1)
Label_Search = Label(master=frame_tab_2, text=" Your Request ")
Label_Search.grid(column=0, row=0)
Button_Search = Button(master=frame_tab_2, text="Search", width=40, command=search_images)
Button_Search.grid(column=3, row=0, columnspan=4)
Label_Settings = Label(master=frame_tab_2, text=" Your width and height ")
Label_Settings.grid(column=0, row=1)

window.mainloop()