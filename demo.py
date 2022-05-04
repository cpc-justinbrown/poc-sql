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

# def buttonFetchCallback(fromscore, toscore, reverse : bool = False, top : int = None):
#     text_box.delete("1.0", END)
#     key = 'site:{site}:extruder:{extruder}'.format(site=entrySite.get(),extruder=entryExtruder.get())
#     if reverse is False and top is None:
#         text_box.insert(END, "ZRANGEBYSCORE {key} {min} {max} WITHSCORES\n".format(key = key, min = fromscore, max = toscore))
#         records = redisClient.zrangebyscore(key,fromscore,toscore,withscores=True)
#     elif reverse is False and top is not None:
#         text_box.insert(END, "ZRANGEBYSCORE {key} {min} {max} WITHSCORES LIMIT 0 {count}\n".format(key = key, min = fromscore, max = toscore, count = top))
#         records = redisClient.zrangebyscore(key,fromscore,toscore,withscores=True,start=0,num=top)
#     elif reverse is True and top is None:
#         text_box.insert(END, "ZREVRANGEBYSCORE {key} +inf -inf WITHSCORES\n".format(key = key))
#         records = redisClient.zrevrangebyscore(key,'+inf','-inf',withscores=True)
#     elif reverse is True and top is not None:
#         text_box.insert(END, "ZREVRANGEBYSCORE {key} +inf -inf WITHSCORES LIMIT 0 {count}\n".format(key = key, count = top))
#         records = redisClient.zrevrangebyscore(key,'+inf','-inf',withscores=True,start=0,num=top)

#     text_box.insert(END, "ZCARD {key}\n".format(key = key))
#     sheet_data = []
#     sheet_data.append([
#         "score",
#         "timestamp",
#         "site",
#         "extruder",
#         "predicted",
#         "lcl",
#         "target",
#         "ucl",
#         "model",
#         "resinName"])
#     for record in records:
#         memberJSON = json.loads(record[0])
#         sheet_data.append([
#             record[1],
#             memberJSON["timestamp"],
#             memberJSON["site"],
#             memberJSON["extruder"],
#             memberJSON["predicted"],
#             memberJSON["lcl"],
#             memberJSON["target"],
#             memberJSON["ucl"],
#             memberJSON["model"],
#             memberJSON["resinName"]])

#     sheet.set_sheet_data(sheet_data)
#     sheet.set_all_cell_sizes_to_text()

#     cardinality = redisClient.zcard('site:{site}:extruder:{extruder}'.format(site = entrySite.get(), extruder = entryExtruder.get()))
#     text_box.insert(END, "\nResults: {len_records} (of {cardinality})\n".format(len_records = len(records), cardinality = cardinality))
#     appendRedisStatistics()

# def buttonPublishEventCallback():
#     event = EventGridEvent(subject="PoC",event_type="PoC.Events.NewPrediction",data_version="1.0",data={
#         "timestamp": datetime.utcnow().isoformat(' '),
#         "site": entrySite.get(), 
#         "extruder": entryExtruder.get(), 
#         "predicted": 0.5, 
#         "lcl": 0.0, 
#         "target": 0.5, 
#         "ucl": 1.0, 
#         "model": entryModel.get(), 
#         "resinName": entryResinName.get()})
#     eventGridClient.send(event)

# def buttonFetchKeysCallback():
#     text_box.delete("1.0", END)
#     text_box.insert(END, 'SCAN 0 MATCH site:*:extruder:*\n')
#     sheet_data = []
#     sheet_data.append([
#         "key",
#         "memory",
#         "cardinality"])
#     for key in redisClient.scan_iter('site:*:extruder:*'):
#         text_box.insert(END, "MEMORY USAGE {key}\n".format(key = key))
#         text_box.insert(END, "ZCARD {key}\n".format(key = key))
#         memory = redisClient.memory_usage(key)
#         cardinality = redisClient.zcard(key)
#         sheet_data.append([
#             key,
#             memory,
#             cardinality])

#     sheet.set_sheet_data(sheet_data)
#     sheet.set_all_cell_sizes_to_text()
#     appendRedisStatistics()

# def getTicksForDatetime(input: datetime):
#     return (input - datetime(1,1,1)).total_seconds() * 10**7
# def getTicksForTimestamp(input: str):
#     return (datetime.strptime(input, '%Y-%m-%d %H:%M:%S.%f') - datetime(1,1,1)).total_seconds() * 10**7

# buttonFetchAll.configure(command=lambda: buttonFetchCallback('-inf', '+inf'))
# buttonFetchLatest.configure(command=lambda: buttonFetchCallback('-inf', '+inf', top = 1, reverse = True))
# buttonFetchLastTwoHours.configure(command=lambda: buttonFetchCallback(
#     getTicksForDatetime(datetime.utcnow() - timedelta(hours=2)),
#     '+inf'))
# buttonPublishEvent.configure(command=buttonPublishEventCallback)
# buttonFetchKeys.configure(command=buttonFetchKeysCallback)
# buttonFetchCustomDateTimeRange.configure(command=lambda: buttonFetchCallback(
#     getTicksForTimestamp(entryFromDateTime.get()),
#     getTicksForTimestamp(entryToDateTime.get())))

#     key = 'site:{site}:extruder:{extruder}'.format(site=entrySite.get(),extruder=entryExtruder.get())
#     if reverse is False and top is None:
#         text_box.insert(END, "ZRANGEBYSCORE {key} {min} {max} WITHSCORES\n".format(key = key, min = fromscore, max = toscore))
#         records = redisClient.zrangebyscore(key,fromscore,toscore,withscores=True)
#     elif reverse is False and top is not None:
#         text_box.insert(END, "ZRANGEBYSCORE {key} {min} {max} WITHSCORES LIMIT 0 {count}\n".format(key = key, min = fromscore, max = toscore, count = top))
#         records = redisClient.zrangebyscore(key,fromscore,toscore,withscores=True,start=0,num=top)
#     elif reverse is True and top is None:
#         text_box.insert(END, "ZREVRANGEBYSCORE {key} +inf -inf WITHSCORES\n".format(key = key))
#         records = redisClient.zrevrangebyscore(key,'+inf','-inf',withscores=True)
#     elif reverse is True and top is not None:
#         text_box.insert(END, "ZREVRANGEBYSCORE {key} +inf -inf WITHSCORES LIMIT 0 {count}\n".format(key = key, count = top))
#         records = redisClient.zrevrangebyscore(key,'+inf','-inf',withscores=True,start=0,num=top)

#     text_box.insert(END, "ZCARD {key}\n".format(key = key))
#     sheet_data = []
#     sheet_data.append([
#         "score",
#         "timestamp",
#         "site",
#         "extruder",
#         "predicted",
#         "lcl",
#         "target",
#         "ucl",
#         "model",
#         "resinName"])
#     for record in records:
#         memberJSON = json.loads(record[0])
#         sheet_data.append([
#             record[1],
#             memberJSON["timestamp"],
#             memberJSON["site"],
#             memberJSON["extruder"],
#             memberJSON["predicted"],
#             memberJSON["lcl"],
#             memberJSON["target"],
#             memberJSON["ucl"],
#             memberJSON["model"],
#             memberJSON["resinName"]])

#     sheet.set_sheet_data(sheet_data)
#     sheet.set_all_cell_sizes_to_text()

#     cardinality = redisClient.zcard('site:{site}:extruder:{extruder}'.format(site = entrySite.get(), extruder = entryExtruder.get()))
#     text_box.insert(END, "\nResults: {len_records} (of {cardinality})\n".format(len_records = len(records), cardinality = cardinality))
#     appendRedisStatistics()

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