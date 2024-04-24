from tkinter import *
import sqlite3

root = Tk()
root.title("TO DO LIST")
root.geometry('400x400')

conn = sqlite3.connect('todo.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS todo (id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, description TEXT NOT NULL, completed BOOLEAN NOT NULL);')

conn.commit()

def complete(id):
    def _complete():
        todo = c.execute('select * from todo where id = ?', (id, )).fetchone()
        c.execute('UPDATE todo SET completed = ? WHERE id = ?', (not todo[3], id))
        conn.commit()
        render_todos()
    return _complete

def remove(id):
    def _remove():
        c.execute('DELETE FROM todo WHERE id = ?', (id, ))
        conn.commit()
        render_todos()
    
    return _remove

def render_todos():
    rows = c.execute('SELECT * FROM todo').fetchall()
    for widget in frame.winfo_children():
        widget.destroy()
    for i in range(0, len(rows)):
        id = rows[i][0]
        completed = rows[i][3]
        description = rows[i][2]
        color = '#555555' if completed else '#000000'
        cBtn = Checkbutton(frame, text=description, fg=color, width=42, anchor=W, command=complete(id))
        cBtn.grid(row=i, column=0, sticky='w')
        deleteBtn = Button(frame, text='Eliminar', command=remove(id))
        deleteBtn.grid(row=i, column=1)
        cBtn.select() if completed else cBtn.deselect()

def addTodo():
    todo = e.get()
    if todo:
        c.execute('INSERT INTO TODO (description, completed) VALUES (?, ?)', (todo, False))
        conn.commit()
        e.delete(0, END)
        render_todos()
    else:
        pass        

l = Label(root, text='Tarea')
l.grid(row=0, column=0)

e = Entry(root, width=40)
e.grid(row=0, column=1)
e.focus()

btn = Button(root, text='Agregar', command=addTodo)
btn.grid(row=0, column=2)

frame = LabelFrame(root, text='Mis tareas', padx=5, pady=5)
frame.grid(row=1, column=0, columnspan=3, sticky=NSEW, padx=5)

render_todos()
root.bind('<Return>', lambda x:addTodo())
root.mainloop()