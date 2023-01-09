import tkinter as tk
import json
import os

BACKGROUND = '#222222'
BUTTON_CONFIG = {
    'bg': '#03926a',
    'fg': '#ffffff',
    'relief': 'flat',
    'bd': 0
}

TEXT_CONFIG = {
    'bg': BACKGROUND,
    'fg': '#ffffff',
    'font': 'Arial 12',
    'wraplength': 280
}


class Action(tk.Frame):
    "Action class"
    def __init__(self, master: tk.Tk, text: str, completed: bool=False):
        super().__init__(master, bg=master['bg'])

        # Variables
        self.selected = tk.IntVar()

        # Widgets
        self.check = tk.Checkbutton(self, bg=self['bg'], variable=self.selected)
        self.check.grid(row=0, column=0)
        if completed: self.check.select()
        self.text = tk.Label(self, text=text, **TEXT_CONFIG)
        self.text.grid(row=0, column=1, sticky='ew')
        self.edit = tk.Button(self, text='Edit', **BUTTON_CONFIG, command=self.edit)
        self.edit.grid(row=0, column=2, padx=1)
        self.delete = tk.Button(self, text='Delete', **BUTTON_CONFIG, command=self.delete)
        self.delete.grid(row=0, column=3)

        # Config
        self.grid_columnconfigure(1, weight=1)
    
    def edit(self) -> None:
        """Calls the master edit function"""
        self.master.master.edit_action(self)
    
    def delete(self) -> None:
        """Calls the master delete function"""
        self.master.master.delete_action(self)


class Window(tk.Tk):
    "Class Window"
    def __init__(self):
        super().__init__()
        # Init
        self.geometry('400x600')
        self.title('ToDo App')
        self['bg'] = BACKGROUND

        # Widgets
        self.main_frame = tk.Frame(self, bg=self['bg'])
        self.main_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        self.action_text = tk.Entry(self)
        self.action_text.grid(row=1, column=0, sticky='ew', padx=10)
        self.add_action = tk.Button(self, text='Add', **BUTTON_CONFIG,command=self.add_action)
        self.add_action.grid(row=2, column=0, sticky='ew', padx=10, pady=(0,10))

        # Config
        self.protocol("WM_DELETE_WINDOW", self.save)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.actions = []
    
    def load(self) -> None:
        """Loads the tasks from a JSON file"""
        path = os.path.dirname(os.path.realpath(__file__))
        with open(f'{path}/data.json', 'r', encoding='UTF-8') as f:
            data = json.load(f)
            for text, completed in data.items():
                action = Action(self.main_frame, text, completed)
                self.actions.append(action)
            self.update_actions()
        
    def save(self) -> None:
        """Saves the tasks into a JSON file"""
        path = os.path.dirname(os.path.realpath(__file__))
        data = {
            action.text['text']: action.selected.get()
            for action in self.actions
        }
        with open(f'{path}/data.json', 'w', encoding='UTF-8') as f:
            json.dump(data, f, indent=4)
        
        self.destroy()
    
    def delete_action(self, action: Action) -> None:
        """Deletes the action and updates the rest"""
        self.clear_actions()
        self.actions.remove(action)
        self.update_actions()
    
    def edit_action(self, action: Action) -> None:
        """Edits the action"""
        if not (text := self.action_text.get()): return
        action.text['text'] = text
        self.action_text.delete(0, 'end')

    def add_action(self) -> None:
        """Adds the action and updates the rest"""
        if not self.action_text.get(): return
        new_action = Action(self.main_frame, self.action_text.get())
        self.action_text.delete(0, 'end')
        self.clear_actions()
        self.actions.append(new_action)
        self.update_actions()
    
    def clear_actions(self) -> None:
        """Clears the actions from screen"""
        for action in self.actions:
            action.grid_forget()
    
    def update_actions(self) -> None:
        """Updates the actions in the screen"""
        for i, action in enumerate(self.actions):
            action.grid(row=i,column=0, sticky='ew')


if __name__ == '__main__':
    window = Window()
    window.load()
    window.mainloop()