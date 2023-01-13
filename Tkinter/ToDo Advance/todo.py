import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from datetime import datetime
import os
import json

PATH = os.path.dirname(os.path.realpath(__file__))
TODAY = datetime.today()


class TkImage(tk.Label):
    """Tkinter don't have a native way to place images."""
    def __init__(self, master: tk.Tk, image: str, **kwargs):
        self.pil_image = Image.open(image)
        image = ImageTk.PhotoImage(self.pil_image)
        super().__init__(master, image=image, bd=0, **kwargs)
        self.image = image


class ImageButton(tk.Button):
    """Tkinter button with an image."""
    def __init__(self, master: tk.Tk, image: str, **kwargs):
        photo = tk.PhotoImage(file=image)
        super().__init__(master, image=photo, bd=0, relief='flat',**kwargs)
        self.image = photo


class TypeButton(tk.Frame):
    """Custom buttom to choose different colors for tasks."""
    def __init__(
        self, window: tk.Tk, master: tk.Frame, color: str, text: str,
        selected: bool=False
    ):
        super().__init__(master, bg=master['bg'])

        # Config
        self.window = window
        self.selected = False
        self.original_color = master['bg']
        self.type_color = color

        # Widgets
        self.indicator = tk.Label(
            self, text=chr(9679), font='Arial 24 bold', fg=color, bg=master['bg']
        )
        self.indicator.pack(side='left', fill='y')
        self.text = tk.Label(self, text=text, font='Arial 12 bold', bg=master['bg'], fg='black')
        self.text.pack(side='left', expand=True, fill='both', padx=(0,8))

        # Mouse Binds
        self.bind('<Button-1>', self.click)
        self.indicator.bind('<Button-1>', self.click)
        self.text.bind('<Button-1>', self.click)
        if selected: self.select()
    
    def click(self, *_) -> None:
        """Manages the click event on the button"""
        if self.selected: return
        self.select()
        self.window.update_task_color(self)

    def get(self) -> str:
        """Returns the color given to the button"""
        return self.type_color
    
    def select(self) -> None:
        """Updates the button to be selected"""
        self['bg'] = self.type_color
        self.text['bg'] = self.indicator['bg'] = self['bg']
        self.text['fg'] = 'white'
        self.selected = True
    
    def deselect(self) -> None:
        """Updates the button to be deselected"""
        self['bg'] = self.original_color
        self.text['bg'] = self.indicator['bg'] = self['bg']
        self.text['fg'] = 'black'
        self.selected = False


class DateEntry(tk.Frame):
    """Custom date entry dd/mm/yyyy"""
    def __init__(self, master: tk.Frame):
        super().__init__(master, bg=master['bg'])

        # Widgets
        self.day = ttk.Combobox(self, values=list(range(1, 32)), width=2, font='Arial 12')
        self.day.current(TODAY.day-1)
        self.day.grid(row=0, column=0)
        tk.Label(self, text='/', fg='#dfdfdf', bg=master['bg']).grid(row=0, column=1)
        self.month = ttk.Combobox(self, values=[
            'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ], width=10, state='readonly', font='Arial 12', justify='center')
        self.month.current(TODAY.month-1)
        self.month.grid(row=0,column=2)
        tk.Label(self, text='/', fg='#dfdfdf', bg=master['bg']).grid(row=0, column=3)
        self.year = ttk.Combobox(self, values=list(range(2023, 2100)), width=4, font='Arial 12')
        self.year.current(TODAY.year-2023)
        self.year.grid(row=0, column=4)
    
    def get(self) -> str:
        """Returns the input date"""
        return f'{self.day.get()}/{self.month.get()}/{self.year.get()}'


class Task(tk.Frame):
    """Custom frame to display the tasks"""
    def __init__(
        self, window: tk.Tk, master: tk.Frame, text: str, date: str,
        color: str='yellow'
    ):
        super().__init__(master, width=400, height=65, bg='white')

        # Config
        self.window = window
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Widgets
        self.color = tk.Frame(self, bg=color, width=10)
        self.color.grid(row=0, column=0, sticky='nsw', rowspan=2)
        self.text = tk.Label(self, text=text, font='Arial 12 bold', fg='#67609b', bg='white')
        self.text.grid(row=0, column=1)
        self.delete = ImageButton(self, f'{PATH}/images/delete.png', command=self.delete)
        self.delete.grid(row=0, column=2, padx=10, rowspan=2)
        self.date = tk.Label(self, text=date, font='Arial 10 bold', fg='#aaaaaa', bg='white')
        self.date.grid(row=1, column=1)
    
    def delete(self) -> None:
        """Calls the window function to update the tasks"""
        self.window.delete(self)
    
    def get(self) -> tuple[str, str, str]:
        """Returns the task info (text, color, date)"""
        return self.text['text'], self.color['bg'], self.date['text']


class StartWindow(tk.Frame):
    """Start window contained in a frame"""
    def __init__(self, window: tk.Tk, master: tk.Frame, **kwargs):
        super().__init__(master, **kwargs)

        # Widgets
        self.image = TkImage(self, f'{PATH}/images/notebook.png')
        self.image.place(x=225, rely=0.4, anchor='center')
        self.click = ImageButton(
            self, f'{PATH}/images/green.png',
            text='Empecemos!', compound='center', fg='white', font='Arial 16 bold',
            command=window.set_main
        )
        self.click.place(x=225, y=650, anchor='center')
        self.start_text = tk.Label(
            self, fg='#534c8f', font='Arial 16 bold',
            bg=self['bg'], text='Recordar de manera sencilla'
        )
        self.start_text.place(x=225, rely=0.6, anchor='center')


class MainWindow(tk.Frame):
    def __init__(self, window: tk.Tk, master: tk.Frame, **kwargs):
        super().__init__(master, **kwargs)

        # Variables
        self.tasks = []

        # Widgets
        self.top_frame = tk.Frame(self, height=200)
        self.top_frame.pack(side='top', fill='x')
        self.top_image = TkImage(self.top_frame, f'{PATH}/images/top.png')
        self.top_image.place(relwidth=1, relheight=1)
        self.center_frame = tk.Frame(self, bg='#f1f5f8')
        self.center_frame.pack(side='top', expand=True, fill='both')
        self.task_frame = tk.Frame(self.center_frame, bg='#f1f5f8')
        self.task_frame.pack(expand=True, fill='both', padx=25, pady=10)
        self.task_frame.grid_propagate(False)
        self.task_frame.grid_columnconfigure(0, weight=1)
        self.bottom_bar = tk.Frame(self, bg='#ffffff', height=100)
        self.bottom_bar.pack(side='bottom', fill='x')
        self.add_button = ImageButton(
            self.bottom_bar, f'{PATH}/images/circle.png',
            text='+', font='Arial 36 bold', fg='white', compound='center',
            command=self.add_task, bg='#ffffff'
        )
        self.add_button.place(relx=0.5, rely=0.5, anchor='center')
    
    def add_task(self) -> None:
        """Changes to the add task window"""
        self.pack_forget()
        window.add_frame.pack(expand=True, fill='both')
    
    def update_task(self, text: str, color: str, date: str) -> None:
        """Creates the new task and updates the main window"""
        task = Task(self, self.task_frame, text, date, color)
        task.grid(row=len(self.tasks), column=0, sticky='nsew', pady=(0,5))
        self.tasks.append(task)
    
    def clear_tasks(self) -> None:
        """Removes the tasks from the window"""
        for task in self.tasks:
            task.grid_forget()
    
    def update_tasks(self):
        """Places the tasks in the window"""
        for i, task in enumerate(self.tasks):
            task.grid(row=i, column=0, sticky='nsew', pady=(0, 5))
            self.task_frame.grid_rowconfigure(i, minsize=70)

    def delete(self, task: Task) -> None:
        """Deletes the task and updates the others"""
        self.clear_tasks()
        self.tasks.remove(task)
        self.update_tasks()


class TaskFrame(tk.Frame):
    """Task configuration window"""
    def __init__(self, window: tk.Tk, master: tk.Frame, **kwargs):
        super().__init__(master, **kwargs)

        # Variables
        self.window = window

        # Widgets
        self.config_frame = tk.Frame(self, bg=self['bg'])
        self.config_frame.place(width=450, height=600, x=0, y=200)
        self.cancel_task = ImageButton(
            self, f'{PATH}/images/circle.png', text='X',
            font='Arial 36 bold', compound='center', fg='white', bg='#f9fdff',
            command=window.return_home
        )
        self.cancel_task.place(x=225, y=200, anchor='center')
        self.task_button = ImageButton(
            self, f'{PATH}/images/blue.png', text='Añadir recordatorio',
            font='Arial 12 bold', fg='white', compound='center', command=self.create_task
        )
        self.task_button.place(x=225, y=850, anchor='center')
        self.add_text = tk.Label(
            self.config_frame, bg='#f9fdff', fg='#000000', text='Añadir recordatorio',
            font='Arial 12 bold'
        )
        self.add_text.pack(fill='x', side='top', pady=(50,0))
        self.info_frame = tk.Frame(self.config_frame, bg=self.config_frame['bg'])
        self.info_frame.pack(side='top', expand=True, fill='both')
        self.info_frame.grid_columnconfigure(0, weight=1)
        self.task_entry = tk.Entry(
            self.info_frame, bg=self.info_frame['bg'], bd=0, relief='flat',
            font='Arial 16 bold', fg='black', justify='center', selectbackground='gray'
        )
        self.task_entry.insert(0, 'Que tengas un gran día!')
        self.task_entry.focus()
        self.task_entry.grid(row=0, column=0, sticky='ew', padx=10, pady=(10, 35))

        self.border = tk.Frame(self.info_frame, bg='#dfdfdf', height=75)
        self.border.grid(row=1, column=0, sticky='ew', padx=20)
        self.border.pack_propagate(False)
        self.type_frame = tk.Frame(self.border, bg=self.info_frame['bg'])
        self.type_frame.pack(expand=True, fill='both', pady=1)

        self.current_color = '#00ff00'
        self.work = TypeButton(self, self.type_frame, '#00ff00', 'Personal', True)
        self.work.pack(side='left', fill='x')
        self.meeting = TypeButton(self, self.type_frame, '#d20361', 'Trabajo')
        self.meeting.pack(side='left', fill='x')
        self.study = TypeButton(self, self.type_frame, '#0000ff', 'Estudio')
        self.study.pack(side='left', fill='x')
        self.shop = TypeButton(self, self.type_frame, '#ff7f00', 'Compras')
        self.shop.pack(side='left', fill='x')

        tk.Label(
            self.info_frame, text='Elige la fecha', font='Arial 12 bold',
            bg=self.info_frame['bg']
        ).grid(row=2, column=0, pady=(50,5), sticky='w', padx=20)

        self.date_entry = DateEntry(self.info_frame)
        self.date_entry.grid(row=3, column=0, sticky='w', padx=20)
    
    def update_task_color(self, color: str) -> None:
        """Updates the types to be singular"""
        self.work.deselect()
        self.meeting.deselect()
        self.study.deselect()
        self.shop.deselect()

        color.select()
        self.current_color = color.get()
    
    def create_task(self) -> None:
        """Creates a new task"""
        color = self.current_color
        text = self.task_entry.get()
        date = self.date_entry.get()
        self.window.main_frame.update_task(text, color, date)
        self.window.return_home()


class Window(tk.Tk):
    """App window"""
    def __init__(self):
        super().__init__()

        # Config
        self.title('ToDo Advanced')
        self.geometry('450x750')
        self.grid_columnconfigure(0, weight=1)
        self.wm_protocol('WM_DELETE_WINDOW', self.save_info)
        self.resizable(False, False)
        
        # Windows
        self.start_frame = StartWindow(self, self, bg='#f9fdff')
        self.start_frame.pack(expand=True, fill='both')
        self.main_frame = MainWindow(self, self, bg='#f9fdff')
        self.add_frame = TaskFrame(self, self, bg='#f9fdff')

        self.load_info()
    
    def set_main(self) -> None:
        """Sets the main window"""
        self.start_frame.pack_forget()
        self.main_frame.pack(expand=True, fill='both')
    
    def return_home(self) -> None:
        """Returns to main window"""
        self.add_frame.pack_forget()
        self.main_frame.pack(expand=True, fill='both')
    
    def load_info(self) -> None:
        """Loads the tasks from the data.json"""
        with open(f'{PATH}/data.json', 'r', encoding='UTF-8') as f:
            data = json.load(f)
            for text, color, date in data['tasks']:
                self.main_frame.update_task(text, color, date)
        if data['started']: self.set_main()
    
    def save_info(self):
        """Saves the tasks into data.json"""
        data = {
            'started': True,
            'tasks': [task.get() for task in self.main_frame.tasks]
        }
        with open(f'{PATH}/data.json', 'w', encoding='UTF-8') as f:
            json.dump(data, f, indent=4)
        self.destroy()


if __name__ == '__main__':
    window = Window()
    window.mainloop()