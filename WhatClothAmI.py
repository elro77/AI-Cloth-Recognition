import numpy as np
import matplotlib.pyplot as plt
import tkinter
import tkinter.messagebox
from tkinter import *

from tensorflow.python.keras.models import model_from_json



root= Tk()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")
loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])



head_label = Label(root,text="Please Draw A Clothing Type\n In The Grid Below:")


w, h = 28, 28
label_grid = [[Label(root,width="1",height="1",bg="white", borderwidth=1, relief="solid") for x in range(w)] for y in range(h)]


pixel_matrix = [[0.0 for x in range(w)] for y in range(h)]
matrix=np.zeros((28,28))

head_label.grid(row=0,column=0)

def label_clicked(event):
  row = event.widget.grid_info()['row']  # Row of the button
  column = event.widget.grid_info()['column']  # grid_info will return dictionary with all grid elements (row, column, ipadx, ipday, sticky, rowspan and columnspan)
  row = row - 1
  column = column - 1
  if (matrix[row][column] == 0):
      matrix[row][column] = 1
      pixel_matrix[row][column]=1.0
      event.widget.config(background="black")


def start_btn_clicked():

    print(type(np.array(pixel_matrix)))
    arr=np.array(pixel_matrix)
    print(arr.shape)
    img = arr.reshape((1,) + arr.shape)
    print(img.shape)

    result= loaded_model.predict(img)
    result_name=class_names[getMax(result[0])]
    tkinter.messagebox.showinfo(title="Result", message="This is a "+result_name)
    plt.imshow(pixel_matrix)
    plt.show()

def getMax(lst):
    best=0.0
    finaIndex=0
    for i in range(len(lst)):
        if(lst[i]>best):
            best=lst[i]
            finaIndex=i
    return finaIndex
def clear_btn_clicked():
    for i in range(28):
        for j in range(28):
            matrix[i][j]=0
            pixel_matrix[i][j] = 0.0
            label_grid[i][j].config(background="white")


start_btn=Button(root,text="Start",command=start_btn_clicked)
start_btn.grid(row=28,column=0)

start_btn=Button(root,text="Clear",command=clear_btn_clicked)
start_btn.grid(row=29,column=0)

row=1
col=1
for i in range(28):
    for j in range(28):
        if(row<28):
            if(col<28):
                label_grid[i][j].grid(row=row,column=col)
                label_grid[i][j].bind('<Button-1>',label_clicked)
                col = col+1
            else:
                row=row+1
                col=1


root.mainloop()
