from asyncio.windows_events import NULL
import json
from textwrap import fill
from tkinter import *
import tksheet
import pymssql

window = Tk()
window.title("SQL Demo Rig")

entryFrame = Frame(window)
entryFrame.grid(row=0, column=0, sticky="nswe")
buttonFrame = Frame(window)
buttonFrame.grid(row=0, column=1, sticky="nswe")
textFrame = Frame(window)
textFrame.grid(row=1, column=0, columnspan=3, sticky="nswe")
sheetFrame = Frame(window)
sheetFrame.grid(row=2, column=0, columnspan=3, sticky="nswe")

# Id
labelId = Label(entryFrame, text="Id:")
labelId.grid(row=0, column=0, sticky='e')
entryId = Entry(entryFrame)
entryId.insert(0, "")
entryId.grid(row=0, column=1)
# Value
labelValue = Label(entryFrame, text="Value:")
labelValue.grid(row=1, column=0, sticky='e')
entryValue = Entry(entryFrame)
entryValue.insert(0, "")
entryValue.grid(row=1, column=1)

buttonSelect = Button(buttonFrame, text="SELECT")
buttonSelect.pack(fill='x')
buttonInsert = Button(buttonFrame, text="INSERT")
buttonInsert.pack(fill='x')
buttonUpdate = Button(buttonFrame, text="UPDATE")
buttonUpdate.pack(fill='x')
buttonDelete = Button(buttonFrame, text="DELETE")
buttonDelete.pack(fill='x')
buttonTruncate = Button(buttonFrame, text="TRUNCATE")
buttonTruncate.pack(fill='x')

text_box = Text(textFrame, height=10)
text_box.pack(fill='x')

sheet = tksheet.Sheet(sheetFrame, width=200, height=200)
sheet.pack()
sheet.enable_bindings((
    "single_select",
    "row_select",
    "column_width_resize",
    "arrowkeys",
    "right_click_popup_menu",
    "rc_select",
    "rc_insert_row",
    "rc_delete_row",
    "copy",
    "cut",
    "paste",
    "delete",
    "undo",
    "edit_cell"))

def getConnection():
    return pymssql.connect(server = 'sqlcpcscus-brownjl.database.windows.net', database = 'sqldbCPCscus-BROWNJL', user = 'Tester', password = 'P@ssw0rd')

def refreshSheet():
    sheet_data = []
    sheet_data.append([
        "id",
        "value"])
    with getConnection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM [Entity];')
        row = cursor.fetchone()
        while row:
            sheet_data.append([
                row[0],
                row[1]])
            row = cursor.fetchone()
    sheet.set_sheet_data(sheet_data)
    sheet.set_all_cell_sizes_to_text()

refreshSheet()

def buttonSelectCallback(id : int):
    text_box.delete("1.0", END)
    text_box.insert(END, "Selecting id = {id}\n".format(id = id))
    try:
        with getConnection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM [Entity] WHERE [Id] = %d;',(id))
            row = cursor.fetchone()
            entryValue.delete(0,END)
            entryValue.insert(0, row[1])
    except:
        text_box.insert(END, "ERROR\n")
    refreshSheet()

def buttonInsertCallback(value : str):
    text_box.delete("1.0", END)
    text_box.insert(END, "Inserting value = {value}\n".format(value = value))
    try:
        with getConnection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO [Entity] ([Value]) VALUES (''%s'');',(value))
            conn.commit()
    except:
        text_box.insert(END, "ERROR\n")
    refreshSheet()

def buttonUpdateCallback(id : int, value : str):
    text_box.delete("1.0", END)
    text_box.insert(END, "Updating id = {id}, value = {value}\n".format(id = id, value = value))
    try:
        with getConnection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE [Entity] SET [Value] = %s WHERE [Id] = %d;',(value, id))
            conn.commit()
    except:
        text_box.insert(END, "ERROR\n")
    refreshSheet()

def buttonDeleteCallback(id : int):
    text_box.delete("1.0", END)
    text_box.insert(END, "Deleting id = {id}\n".format(id = id))
    try:
        with getConnection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM [Entity] WHERE [Id] = %d;',(id))
            conn.commit()
    except:
        text_box.insert(END, "ERROR\n")
    refreshSheet()

def buttonTruncateCallback():
    text_box.delete("1.0", END)
    text_box.insert(END, "Truncating\n")
    try:
        with getConnection() as conn:
            cursor = conn.cursor()
            cursor.execute('TRUNCATE TABLE [Entity];')
            conn.commit()
    except:
        text_box.insert(END, "ERROR\n")
    refreshSheet()

buttonSelect.configure(command=lambda: buttonSelectCallback(entryId.get()))
buttonInsert.configure(command=lambda: buttonInsertCallback(entryValue.get()))
buttonUpdate.configure(command=lambda: buttonUpdateCallback(entryId.get(), entryValue.get()))
buttonDelete.configure(command=lambda: buttonDeleteCallback(entryId.get()))
buttonTruncate.configure(command=lambda: buttonTruncateCallback())

window.mainloop()