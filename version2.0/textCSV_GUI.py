

#import tkinter as tk
#from tkinter import filedialog
from functools import partial
import re, sys, os
from RandomNetworkFlow import *

# Version Check
if sys.version_info[0] == 3: # Python 3
    from tkinter import *
    #from tkinter import ttk
    from tkinter.ttk import Notebook
    from tkinter.ttk import Treeview
    from tkinter.ttk import Button
    import tkinter.filedialog as tkf
else:
    # Python 2
    from Tkinter import *
    from ttk import Notebook
    from ttk import Treeview
    from ttk import Entry
    import tkFileDialog as tkf

     

'''
class FindPopup(Toplevel):
    def __init__(self, master):
        super().__init__()
        self.master = master
    
        self.title("Find in file")
        self.center_window()
        self.transient(master)
        self.matches_are_highlighted = True
    
        self.main_frame = Frame(self, bg="lightgrey")
        self.button_frame = Frame(self.main_frame, bg="lightgrey")
        self.find_label = Label(self.main_frame, text="Find: ", bg="lightgrey", fg="black")
        self.find_entry = Entry(self.main_frame, bg="white", fg="black")
        self.find_button = Button(self.button_frame, text="Find All", bg="lightgrey", fg="black", command=self.find)
        self.next_button = Button(self.button_frame, text="Next", bg="lightgrey", fg="black", command=self.jump_to_next_match)
        self.cancel_button = Button(self.button_frame, text="Cancel", bg="lightgrey", fg="black", command=self.cancel)
    
        self.main_frame.pack(fill=BOTH, expand=1)
        self.find_button.pack(side=LEFT, pady=(0,10), padx=(20,20))
        self.next_button.pack(side=LEFT, pady=(0,10), padx=(15,20))
        self.cancel_button.pack(side=LEFT, pady=(0,10), padx=(15,0))
        self.button_frame.pack(side=BOTTOM, fill=BOTH)
        self.find_label.pack(side=LEFT, fill=X, padx=(20,0))
        self.find_entry.pack(side=LEFT, fill=X, expand=1, padx=(0,20))
    
        self.find_entry.focus_force()
        self.find_entry.bind("<Return>", self.jump_to_next_match)
        self.find_entry.bind("<KeyRelease>", self.matches_are_not_highlighted)
        self.bind("<Escape>", self.cancel)
        
        self.protocol("WM_DELETE_WINDOW", self.cancel)

    def find(self, event=None):
        text_to_find = self.find_entry.get()
        if text_to_find and not self.matches_are_highlighted:
            self.master.remove_all_find_tags()
        self.master.highlight_matches(text_to_find)
        self.matches_are_highlighted = True
    
    def jump_to_next_match(self, event=None):
        text_to_find = self.find_entry.get()
        if text_to_find:
            if not self.matches_are_highlighted:
                self.find()
            self.master.next_match()
    
    def cancel(self, event=None):
        self.master.remove_all_find_tags()
        self.destroy()
    
    def matches_are_not_highlighted(self, event):
    
        key_pressed = event.keysym
        if not key_pressed == "Return":
            self.matches_are_highlighted = False
    
    def center_window(self):
        master_pos_x = self.master.winfo_x()
        master_pos_y = self.master.winfo_y()
    
        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()
    
        my_width = 300
        my_height = 100
    
        pos_x = (master_pos_x + (master_width // 2)) - (my_width // 2)
        pos_y = (master_pos_y + (master_height // 2)) - (my_height // 2)
    
        geometry = "{}x{}+{}+{}".format(my_width, my_height, pos_x, pos_y)
        self.geometry(geometry)
'''

class Editor(object):
    def __init__(self):
        
        self.open_file = None
        if os.path.exists("log.txt"):
            for line in open("log.txt", "r"):
                #if re.match('FN_FDS', line):
                #    temp =  line.split('=')
                #    FN_FDS = temp[1].strip()
                if re.match('FN_EVAC', line):
                    temp =  line.split('=')
                    self.open_file = temp[1].strip()
                    
        print(self.open_file)
        self.fname_OutTXT = None
        self.fname_OutBIN = None
        self.fname_OutNPZ = None

        #self.currentSimu = None
        if self.open_file:
            self.currentdir = os.path.dirname(self.open_file)
        else:
            self.currentdir = None

        self.AUTOCOMPLETE_WORDS = ["stress", "fixed", "random", "auto", "True", "False"]
        self.FONT_SIZE = 10
        #self.AUTOCOMPLETE_WORDS = ["def", "import", "if", "else", "while", "for","try:", "except:", "print(", "True", "False"]
        self.WINDOW_TITLE = "CSV Text Editor"

        self.window = Tk()
        self.window.title(self.WINDOW_TITLE)
        self.window.geometry("800x600")

        self.menubar = Menu(self.window, bg="lightgrey", fg="black")
        self.window.config(menu=self.menubar)
    
        self.file_menu = Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
        self.file_menu.add_command(label="New", command=self.file_new, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.file_open, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.file_save, accelerator="Ctrl+S")
        
        self.edit_menu = Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
        self.edit_menu.add_command(label="Copy", command=self.edit_copy, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Cut", command=self.edit_cut, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Paste", command=self.edit_paste, accelerator="Ctrl+V")
        self.edit_menu.add_command(label="Undo", command=self.edit_undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=self.edit_redo, accelerator="Ctrl+Y")

        self.py_menu = Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
        #self.py_menu.add_command(label="python27", command=self.py2run, accelerator="F5")
        self.py_menu.add_command(label="RunSimulation", command=self.py3run, accelerator="F5")
        #self.py_menu.add_command(label="plotTpre", command=self.py3tpre, accelerator="Alt+Z")
        #self.py_menu.add_command(label="visualizeData", command=self.py3vis, accelerator="Alt+A")

        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)
        self.menubar.add_cascade(label="Run", menu=self.py_menu)
        
        
        #self.line_numbers = Text(self, bg="lightgrey", fg="black", width=6, font=("Times", self.FONT_SIZE))
        #self.line_numbers.insert(1.0, "1 \n")
        #self.line_numbers.configure(state="disabled")
        #self.line_numbers.pack(side=LEFT, fill=Y)
                
        self.main_text = Text(self.window, bg="lightgrey", fg="black", font=("Times", self.FONT_SIZE))
        self.main_text.pack(expand=1, fill=BOTH)
        #self.main_text = Text(self.window, width=45,height=6, bg="brown", fg="lightcyan", wrap=WORD,font=("Courier",10))
        #self.main_text.pack(side=LEFT,fill=BOTH,expand=YES)

        
        scrollInfo = Scrollbar(self.main_text)
        scrollInfo.pack(side=RIGHT, fill=Y)
        scrollInfo.config(command=self.main_text.yview)
        
        self.main_text.config(yscrollcommand=scrollInfo.set)
        self.main_text.insert(END, 'QuickStart: \nStep1: Please select csv file to read in initial state data and compartement networkflow data!\n')
        self.main_text.insert(END, 'Step2: Compute simulation and plot output data!\n')
        #self.main_text.insert(END, '\nWhen simulation starts, please try to press the following keys in your keybroad, and you will see the effects on the screen. \n')
        #self.main_text.insert(END, 'Press <pageup/pagedown> to zoom in or zoom out.\n')
        #self.main_text.insert(END, 'Press arrow keys to move the entities vertically or horizonally in screen.\n')
        #self.main_text.insert(END, 'Press 1/2/3 in number panel (Right side in the keyboard) to display the door or exit data on the screen.\n')
        self.main_text.insert(END, 'Press <space> to pause or resume the simulaton. \n')



        '''
        if self.open_file:
            self.main_text.delete(1.0, END)
            with open(self.open_file, "r") as file_contents:
                file_lines = file_contents.readlines()
                if len(file_lines) > 0:
                    for index, line in enumerate(file_lines):
                        index = float(index) + 1.0
                        line = re.sub(r',,', '', line)
                        line_t = re.sub(r',', ',\t', line)
                        self.main_text.insert(index, line_t)
                        #self.main_text.insert(index, line)
        self.window.title(" - ".join([self.WINDOW_TITLE, self.open_file]))
        '''
        
        #self.scrollbar = Scrollbar(self, orient="vertical") #, command=self.scroll_text_and_line_numbers)
        #self.main_text.configure(yscrollcommand=self.scrollbar.set)
        #self.scrollbar.config(command=self.main_text.yview)
        #self.scrollbar.pack(side=RIGHT, fill=Y)
    
        self.main_text.bind("<space>", self.destroy_autocomplete_menu)
        #self.main_text.bind("<KeyRelease>", self.display_autocomplete_menu)
        self.main_text.bind("<Tab>", self.insert_spaces)
    
        self.window.bind("<Control-s>", self.file_save)
        self.window.bind("<Control-o>", self.file_open)
        self.window.bind("<Control-n>", self.file_new)
        
        self.window.bind("<Control-a>", self.select_all)
        self.window.bind("<Control-f>", self.show_find_window)
        
        #self.window.bind("<F5>", self.py2run)
        self.window.bind("<F6>", self.py3run)

    '''
        self.main_text.bind("<MouseWheel>", self.scroll_text_and_line_numbers)
        self.main_text.bind("<Button-4>", self.scroll_text_and_line_numbers)
        self.main_text.bind("<Button-5>", self.scroll_text_and_line_numbers)
        self.line_numbers.bind("<MouseWheel>", self.skip_event)
        self.line_numbers.bind("<Button-4>", self.skip_event)
        self.line_numbers.bind("<Button-5>", self.skip_event)

    def skip_event(self, event=None):
        pass

    def scroll_text_and_line_numbers(self, *args):  
        try:
            # from scrollbar
            self.main_text.yview_moveto(args[1])
            self.line_numbers.yview_moveto(args[1])
        except IndexError:
            #from MouseWheel
            event = args[0]
            if event.delta:
                move = -1*(event.delta/120)
            else:
                if event.num == 5:
                    move = 1
                else:
                    move = -1
    
            self.main_text.yview_scroll(int(move), "units")
            self.line_numbers.yview_scroll(int(move), "units")
    '''

    def py3run(self, event=None):
        #os.system("python main.py "+self.open_file)

        T=16  # Simulation Timo Horizon [0, T]
        simulation(self.open_file, T)

    def py3tpre(self, event=None):
        self.fname_OutBIN = tkf.askopenfilename(filetypes=(("bin files", "*.bin"),("All files", "*.*")),\
        initialdir=self.currentdir)
        temp=re.split(r'/', self.fname_OutBIN)
        #temp=self.fname_OutTXT.split('/') 
        #self.lb_outbin.config(text = "The output bin file selected: "+str(temp[-1])+"\n")
        #self.textInformation.insert(END, 'fname_FDS:   '+self.fname_FDS)
        print('fname_outBinFile:', self.fname_OutBIN)
        visualizeTpre(self.fname_OutBIN)
        
    def py3vis(self, event=None):
        self.fname_OutBIN = tkf.askopenfilename(filetypes=(("bin files", "*.bin"),("npz files", "*.npz"),("All files", "*.*")),\
        initialdir=self.currentdir)
        
        if os.path.exists(self.open_file):
            for line in open(self.open_file, "r"):
                if re.match('ZOOM', line):
                    temp =  line.split('=')
                    ZOOM = float(temp[1].strip())                    
                if re.match('xSpace', line):
                    temp =  line.split('=')
                    xSpa = float(temp[1].strip())
                if re.match('ySpace', line):
                    temp =  line.split('=')
                    ySpa = float(temp[1].strip())
        else:
            ZOOM = 60.0
            xSpa = 30.0
            ySpa = 30.0
        #temp=self.fname_OutTXT.split('/') 
        #self.lb_outbin.config(text = "The output bin file selected: "+str(temp[-1])+"\n")
        #self.textInformation.insert(END, 'fname_FDS:   '+self.fname_FDS)
        print('Output data file selected:', self.fname_OutBIN)
        temp= self.fname_OutBIN.split('.')
        if temp[1]=='bin':
            visualizeEvac(self.fname_OutBIN, None, None, ZOOM, xSpa, ySpa)


    def file_new(self, event=None):
        file_name = tkf.asksaveasfilename()
        if file_name:
            self.open_file = file_name
            self.main_text.delete(1.0, END)
            self.title(" - ".join([self.WINDOW_TITLE, self.open_file]))

    def file_open(self, event=None):
        file_to_open = tkf.askopenfilename()

        if file_to_open:
            self.open_file = file_to_open
            self.main_text.delete(1.0, END)

            with open(file_to_open, "r") as file_contents:
                file_lines = file_contents.readlines()
                if len(file_lines) > 0:
                    for index, line in enumerate(file_lines):
                        index = float(index) + 1.0
                        line = re.sub(r',,', '', line)
                        line_t = re.sub(r',', ',\t', line)
                        self.main_text.insert(index, line_t)
                        #self.main_text.insert(index, line)
        self.window.title(" - ".join([self.WINDOW_TITLE, self.open_file]))
        print(self.open_file)
        #self.update_line_numbers()
        

    def file_save(self, event=None):
        if not self.open_file:
            new_file_name = tkf.asksaveasfilename()
            if new_file_name:
                self.open_file = new_file_name
        if self.open_file:
            #new_contents = self.main_text.get(1.0, END)
            #with open(self.open_file, "w") as open_file:
            #    open_file.write(new_contents)
            new_contents = self.main_text.get(1.0, END)
            new_contents2 = re.sub(',\t', ',', new_contents)
            with open(self.open_file, "w") as open_file:
                open_file.write(new_contents2)

    def select_all(self, event=None):
        self.main_text.tag_add("sel", 1.0, END)
        return None

    def edit_copy(self, event=None):
        self.main_text.event_generate("<<Copy>>")
        return None

    def edit_cut(self, event=None):
        self.main_text.event_generate("<<Cut>>")
        return None

    def edit_paste(self, event=None):
        self.main_text.event_generate("<<Paste>>")
        self.on_key_release()
        self.tag_all_lines()
        return None

    def edit_undo(self, event=None):
        self.main_text.event_generate("<<Undo>>")
        return None

    def edit_redo(self, event=None):
        self.main_text.event_generate("<<Redo>>")
        return None

    def insert_spaces(self, event=None):
        self.main_text.insert(INSERT, " ")
        return None

    def get_menu_coordinates(self):
        bbox = self.main_text.bbox(INSERT)
        menu_x = bbox[0] + self.winfo_x() + self.main_text.winfo_x()
        menu_y = bbox[1] + self.winfo_y() + self.main_text.winfo_y() + self.FONT_SIZE + 2
        
        return (menu_x, menu_y)

    def display_autocomplete_menu(self, event=None):
        current_index = self.main_text.index(INSERT)
        start = self.adjust_floating_index(current_index)

        try:
            currently_typed_word = self.main_text.get(start + " wordstart", INSERT)
        except TclError:
            currently_typed_word = ""
        
        currently_typed_word = str(currently_typed_word).strip()

        if currently_typed_word:
            self.destroy_autocomplete_menu()

            suggestions = []
            for word in self.AUTOCOMPLETE_WORDS:
                if word.startswith(currently_typed_word) and not currently_typed_word == word:
                    suggestions.append(word)

            if len(suggestions) > 0:
                x, y = self.get_menu_coordinates()
                self.complete_menu = Menu(self, tearoff=0, bg="lightgrey", fg="black")

                for word in suggestions:
                    insert_word_callback = partial(self.insert_word, word=word, part=
                        currently_typed_word, index=current_index)
                    self.complete_menu.add_command(label=word, command=
                        insert_word_callback)

                self.complete_menu.post(x, y)
                self.main_text.bind("<Down>", self.focus_menu_item)


    def destroy_autocomplete_menu(self, event=None):
        try:
            self.complete_menu.destroy()
            self.main_text.unbind("<Down>")
            self.main_text.focus_force()
        except AttributeError:
            pass

    def insert_word(self, word, part, index):
        amount_typed = len(part)
        remaining_word = word[amount_typed:]
        remaining_word_offset = " +" + str(len(remaining_word)) + "c"
        self.main_text.insert(index, remaining_word)
        self.main_text.mark_set(INSERT, index + remaining_word_offset)
        self.destroy_autocomplete_menu()
        self.main_text.focus_force()

    def adjust_floating_index(self, number):
        indices = number.split(".")
        x_index = indices[0]
        y_index = indices[1]
        y_as_number = int(y_index)
        y_previous = y_as_number - 1
        return ".".join([x_index, str(y_previous)])

    def focus_menu_item(self, event=None):
        try:
            self.complete_menu.focus_force()
            self.complete_menu.entryconfig(0, state="active")
        except TclError:
            pass
    
    '''
    def tag_all_lines(self):
        final_index = self.main_text.index(END)
        final_line_number = int(final_index.split(".")[0])

        for line_number in range(final_line_number):
            line_to_tag = ".".join([str(line_number), "0"])
            self.tag_keywords(None, line_to_tag)
        self.update_line_numbers()
    
    def update_line_numbers(self):
        self.line_numbers.configure(state="normal")
        self.line_numbers.delete(1.0, END)
        number_of_lines = self.main_text.index(END).split(".")[0]
        line_number_string = "\n".join(str(no+1) for no in range(int(number_of_lines)))
        self.line_numbers.insert(1.0, line_number_string)
        self.line_numbers.configure(state="disabled")
    '''
    
    def show_find_window(self, event=None):
        FindPopup(self)
    
    def highlight_matches(self, text_to_find):
        self.main_text.tag_remove("findmatch", 1.0, END)
        self.match_coordinates = []
        self.current_match = -1
    
        find_regex = re.compile(text_to_find)
        search_text_lines = self.main_text.get(1.0, END).split("\n")
    
        for line_number, line in enumerate(search_text_lines):
            line_number += 1
        for match in find_regex.finditer(line):
            start, end = match.span()
            start_index = ".".join([str(line_number), str(start)])
            end_index = ".".join([str(line_number), str(end)])
            self.main_text.tag_add("findmatch", start_index, end_index)
            self.match_coordinates.append((start_index, end_index))
    
    def next_match(self, event=None):
        try:
            current_target, current_target_end = self.match_coordinates[self.current_match]
            self.main_text.tag_remove("sel", current_target, current_target_end)
            self.main_text.tag_add("findmatch", current_target, current_target_end)
        except IndexError:
            pass
    
        try:
            self.current_match = self.current_match + 1
            next_target, target_end = self.match_coordinates[self.current_match]
        except IndexError:
            if len(self.match_coordinates) == 0:
                msg.showinfo("No Matches", "No Matches Found")
            else:
                if msg.askyesno("Wrap Search?", "Reached end of file. Continue from the top?"):
                    self.current_match = -1
                    self.next_match()
                else:
                    self.main_text.mark_set(INSERT, next_target)
                    self.main_text.tag_remove("findmatch", next_target, target_end)
                    self.main_text.tag_add("sel", next_target, target_end)
                    self.main_text.see(next_target)
    
    def remove_all_find_tags(self):
        self.main_text.tag_remove("findmatch", 1.0, END)
        self.main_text.tag_remove("self", 1.0, END)
    
    def start(self):
        self.window.mainloop()

if __name__ == "__main__":
    editor = Editor()
    editor.start()
