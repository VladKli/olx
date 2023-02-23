import tkinter as tk
from result import main


def do_something():
    # get the input value and do something with it
    input_value = input_field.get()
    main(input_value)
    # clear the input field
    input_field.delete(0, tk.END)
    # do something with the input value
    label.config(text="Function executed with input: " + input_value)

root = tk.Tk()

# create an input field
input_field = tk.Entry(root)
input_field.pack()

# create a button
button = tk.Button(root, text="Вставь ссылку!", command=do_something)
button.pack()

label = tk.Label(root, text="check the sound")
label.pack()

root.mainloop()
