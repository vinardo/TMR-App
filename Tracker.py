import pandas
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os
import csv

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, background='grey15')
        self.master = master
        self.master.title("TMR Tracker")
        self.pack(fill=BOTH, expand=True)
        self.path = os.path.abspath('tracker_files')
        self.working_file_name = ''
        self.working_file_content = pandas.DataFrame()
        self.file_dic = []
        self.updating = False
        # getting file path and checking for existing files
        self.folder = os.listdir(self.path)
        self.copied_line = pandas.Series
        # ADD HERE A "WORKING FILE ITEM" SO ITS EASIER TO WORK WITH

        self.create_widgets()
# LOADS ALL THE WIDGETS IN THE WINDOW
    def create_widgets(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1) 
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)
        self.grid_columnconfigure(6, weight=1)
        self.grid_columnconfigure(7, weight=1)

        # files list name label
        self.files_label = tk.Label(self, background='grey15')
        self.files_label['text'] = 'File Explorer'
        self.files_label.grid(row=0, column=0, columnspan=2, sticky="N", pady=5)

        # all the buttons getting loaded in
        self.add_button = tk.Button(self, width=10, height=5, background='LightSteelBlue4')
        self.add_button['text'] = "Add"
        self.add_button['command'] = self.add_tmr
        self.add_button.grid(row=0, column=2, sticky="NSEW")
             
        self.move_button = tk.Button(self, width=10, height=5, background='LightSteelBlue4')
        self.move_button['text'] = "Move"
        self.move_button['command'] = self.move_tmr
        self.move_button.grid(row=0, column=3, sticky="NSEW")
        
        self.export_button = tk.Button(self, width=10, height=5, background='LightSteelBlue4')
        self.export_button['text'] = "Export/\nPrint"
        self.export_button['command'] = self.export_tmr
        self.export_button.grid(row=0, column=6, sticky="NSEW")
        
        self.find_button = tk.Button(self, width=10, height=5, background='LightSteelBlue4')
        self.find_button['text'] = "Find"
        self.find_button['command'] = self.find_tmr
        self.find_button.grid(row=0, column=4, sticky="NSEW")
        
        self.filter_button = tk.Button(self, width=10, height=5, background='LightSteelBlue4')
        self.filter_button['text'] = "Filter"
        self.filter_button['command'] = self.filter_tmr
        self.filter_button.grid(row=0, column=5, sticky="NSEW")

        self.files_drop_menu = tk.Menu(self, tearoff = 0)
        self.files_drop_menu.add_command(label="Add File", command = self.add_new_file)
        self.files_drop_menu.add_command(label="Delete File", command = self.del_file)
        self.files_drop_menu.add_command(label="Open File", command = self.update_file_shown)
        self.files_drop_menu.add_separator()
        self.files_drop_menu.add_command(label="Rename File", command = self.rename_file)

        filter_list = tk.Menu(self, tearoff=1)
        filter_list.add_command(label='By Supporting Unit', command= lambda: self.filter_tmr('unit'))
        filter_list.add_command(label='By Start Date', command= lambda: self.filter_tmr('date'))

        self.file_d_list = tk.Menu(self)
        # RUNS A FOR LOOP TO CHECK HOW MUCH FILES ARE IN FOLDER AND CREATES A DROPDOWN FOR EACH
        self.move_options = []
        for i in self.folder:
            if i != '.DS_Store':
                file_name = i[:-4]
                if i != self.working_file_name:
                    self.move_options.append(file_name)
                    self.file_d_list.add_command(label=file_name, command=lambda n=file_name: self.move_tmr(n))
        # FIX MOVING TMR ITEM TO DIFFERENT FILE

        self.tmr_drop_down = tk.Menu(self, tearoff=0)
        self.tmr_drop_down.add_command(label="Add TMR", command = self.add_tmr)
        self.tmr_drop_down.add_command(label="Delete TMR", command = self.delete_tmr)
        self.tmr_drop_down.add_command(label="Edit TMR", command = self.edit_tmr)
        self.tmr_drop_down.add_separator()
        self.tmr_drop_down.add_cascade(label='Filter TMR', menu=filter_list)
        self.tmr_drop_down.add_separator()
        self.tmr_drop_down.add_cascade(label="Move TMR", menu=self.file_d_list)
        self.tmr_drop_down.add_separator()
        self.tmr_drop_down.add_command(label="Import/Compare", command = self.import_to_compare)

        # both lists right here 
        self.files_list = tk.Listbox(self, background='LightSteelBlue4', selectmode=tk.SINGLE)
        self.files_list.grid(row=0, rowspan=3, column=0, columnspan=2, sticky=(tk.N, tk.W, tk.S), padx=10, pady=30)
        
        self.tmrs_list = tk.Listbox(self, background='LightSteelBlue4', selectmode=tk.SINGLE)
        self.tmrs_list.grid(row=1, column=2, rowspan=2, columnspan=8, sticky=(tk.N, tk.W, tk.E, tk.S), padx=10, pady=10)
        self.tmrs_list.insert(0, 'Select a file to begin')
        
        # calling update function to update files list
        self.update_files_list()
# CONTROLS POP UP TO CREATE NEW FILE 
    def do_file_popup(self, event):
        try:
            self.files_drop_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.files_drop_menu.grab_release()    
# CONTROLS POP UP TO CREATE A NEW TMR ITEM
    def do_tmr_popup(self, event):
        try:
            self.tmr_drop_down.tk_popup(event.x_root, event.y_root)
        finally:
            self.tmr_drop_down.grab_release()
# REREADS THE FOLDER CONTAINING ALL THE .CSV FILES AND UPDATES IF ANY CHANGES    
    def update_files_list(self):
        self.files_list.delete(0, tk.END)

        # adding files from folder directory to the files listbox
        for i in self.folder:
            if i != '.DS_Store':
                file_name = i[:-4]
                self.files_list.insert(1, file_name)    
        
        if self.working_file_name == '':
            # print(f'starting file is {self.folder[1]}')
            self.working_file_name = self.folder[1]
            # print(type(self.working_file_content))

            if not self.working_file_content.empty:
                print('file is empty')
                if os.path.getsize(('tracker_files') + '/' + self.working_file_name) != 0:
                    self.working_file_content = pandas.read_csv(self.path + '/' + self.working_file_name)
                    if self.working_file_content.size > 0:
                        self.updating = True
                        self.update_file_shown()
                    else:
                        self.tmrs_list.insert(0, f'{self.working_file_name} is empty. Click add to add a new item to file.')

                    self.tmrs_list.bind('<Button-2>', self.do_tmr_popup)
                else:
                    self.tmrs_list.insert(0, f'{self.working_file_name} is the Wrong File format!')
        
        self.files_list.bind('<Double-1>', self.update_file_shown)
        self.files_list.bind('<Button-2>', self.do_file_popup)

    '''ALL THE LOGIC WILL BE BELOW THIS COMMENT'''
    def update_file_shown(self, *args):
        if self.updating:
            # delete old listbox data
            self.tmrs_list.delete(0, tk.END)
            self.file_dic.clear()
            self.working_file_content = pandas.read_csv(self.path + '/' + self.working_file_name + '.csv')
            for index, row in self.working_file_content.iterrows():
                mod_row = row.to_dict()
                self.file_dic.append(mod_row)
                line_item = (f"{mod_row['num']}   ||   {mod_row['name']}   ||   {mod_row['sd']} @ {mod_row['st']} - {mod_row['ed']} @ {mod_row['et']}   ||   {mod_row['req']}   ||   {mod_row['su']}")
                self.tmrs_list.insert(index, line_item)
            
            self.updating = False
        else:
            selected_idx = int(self.files_list.curselection()[0])
            self.working_file_name = self.files_list.get(selected_idx)
            # MAKE THE WORKING FILE HERE

            # delete old listbox data
            self.tmrs_list.delete(0, tk.END)
            self.file_dic.clear()
            # read selected file
            if os.path.getsize(('tracker_files') + '/' + self.working_file_name + '.csv') != 0:
                self.working_file_content = pandas.read_csv(self.path + '/' + self.working_file_name + '.csv')
                if self.working_file_content.size > 0:
                    # listbox of tmr items
                    for index, row in self.working_file_content.iterrows():
                        mod_row = row.to_dict()
                        self.file_dic.append(mod_row)
                        line_item = (f"{mod_row['num']}   ||   {mod_row['name']}   ||   {mod_row['sd']} @ {mod_row['st']} - {mod_row['ed']} @ {mod_row['et']}   ||   {mod_row['req']}   ||   {mod_row['su']}")
                        self.tmrs_list.insert(index, line_item)
                else:
                    self.tmrs_list.insert(0, f'{self.working_file_name} is empty. Click add to add a new item to file.')

            else:
                self.tmrs_list.insert(0, f'{self.working_file_name} is the Wrong File format!')

            self.tmrs_list.bind('<Button-2>', self.do_tmr_popup)
            # print(F'HELLO {self.working_file_name}')
            
# THIS IS EDITING TMR ITEMS
    def new_tmr(self):
        name = self.new_tmr_name.get()
        num = self.new_tmr_num.get()
        sd = self.new_tmr_sd.get()
        st = self.new_tmr_st.get()
        ed = self.new_tmr_ed.get()
        et = self.new_tmr_et.get()
        req = self.new_tmr_req.get()
        sup = self.new_tmr_sup.get()
        self.pop_up.destroy()

        file_path = os.path.join(self.path, f'{self.working_file_name}.csv')
        print(file_path)

        with open(file_path, mode='a') as csv_file:
            fieldnames = ['name', 'num', 'sd', 'st', 'ed', 'et', 'req', 'su']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writerow({'name': name, 'num': num, 'sd': sd, 'st': st, 'ed': ed, 'et': et, 'req': req, 'su': sup})

        csv_file.close()
        print('file save')

        self.updating = True
        self.update_file_shown()

        self.tmrs_list.bind('<Button-2>', self.do_tmr_popup)

    def add_tmr(self):
        if 'name' in self.working_file_content:
            win = tk.Toplevel(background='grey15')
            win.wm_title("Add new TMR")

            win.grid_rowconfigure(0, weight = 1)
            win.grid_columnconfigure(0, weight = 1)

            name_l = tk.Label(win, text="Enter TMR Name", background='grey15')
            name_l.grid(row=0, column=0, padx=5, pady=5)

            name = tk.Entry(win, background='grey15')
            name.focus_set()
            name.grid(row=1, column=0, padx=5, pady=5)

            num_l = tk.Label(win, text="Enter TMR Number", background='grey15')
            num_l.grid(row=2, column=0, padx=5, pady=5)

            num = tk.Entry(win, background='grey15')
            num.grid(row=3, column=0, padx=5, pady=5)

            start_date_l = tk.Label(win, text="Enter TMR Start Date", background='grey15')
            start_date_l.grid(row=4, column=0, padx=5, pady=5)

            start_date = tk.Entry(win, background='grey15')
            start_date.grid(row=5, column=0, padx=5, pady=5)

            start_time_l = tk.Label(win, text="Enter TMR Start Time", background='grey15')
            start_time_l.grid(row=6, column=0, padx=5, pady=5)

            start_time = tk.Entry(win, background='grey15')
            start_time.grid(row=7, column=0, padx=5, pady=5)

            end_date_l = tk.Label(win, text="Enter TMR End Date", background='grey15')
            end_date_l.grid(row=0, column=1, padx=5, pady=5)

            end_date = tk.Entry(win, background='grey15')
            end_date.grid(row=1, column=1, padx=5, pady=5)

            end_time_l = tk.Label(win, text="Enter TMR End Time", background='grey15')
            end_time_l.grid(row=2, column=1, padx=5, pady=5)

            end_time = tk.Entry(win, background='grey15')
            end_time.grid(row=3, column=1, padx=5, pady=5)

            req_l = tk.Label(win, text="Enter TMR Requirements", background='grey15')
            req_l.grid(row=4, column=1, padx=5, pady=5)

            req = tk.Entry(win, background='grey15')
            req.grid(row=5, column=1, padx=5, pady=5)

            sup_l = tk.Label(win, text="Enter TMR Supporting Unit", background='grey15')
            sup_l.grid(row=6, column=1, padx=5, pady=5)

            sup = tk.Entry(win, background='grey15')
            sup.grid(row=7, column=1, padx=5, pady=5)

            self.new_tmr_name = name
            self.new_tmr_num = num
            self.new_tmr_sd = start_date
            self.new_tmr_st = start_time
            self.new_tmr_ed = end_date
            self.new_tmr_et = end_time
            self.new_tmr_req = req
            self.new_tmr_sup = sup
            self.pop_up = win

            b = tk.Button(win, text="Enter", background='grey15', command = self.new_tmr)
            b.grid(row=8, column=0, columnspan=2, padx=5, pady=5)
        else:
            print("can't add a tmr to this file...")
            self.tmrs_list.delete(0, tk.END)
            self.tmrs_list.insert(0, f'{self.working_file_name} is the Wrong File format!')
            self.tmrs_list.insert(1, "Can not add to this file!")

    def delete_tmr(self):
        selected_idx = int(self.tmrs_list.curselection()[0])

        self.working_file_content.drop(self.working_file_content.index[selected_idx], inplace = True)

        same_path = os.path.join(self.path, f'{self.working_file_name}.csv')
        self.working_file_content.to_csv(same_path, index = False)

        # listbox of tmr items
        self.updating = True
        self.update_file_shown()

        self.tmrs_list.bind('<Button-2>', self.do_tmr_popup)

# CHANGE FROM SAYING ARCHIVE TO MOVE TMR, AND CHANGE TO MOVE TO ANY FILE
    def move_tmr(self, f_name):
        selected_idx = int(self.tmrs_list.curselection()[0])
        self.copied_line = self.tmrs_list.get(selected_idx)

        copied_path = os.path.join(self.path, f'{self.working_file_name}.csv')
        self.working_file_content.to_csv(copied_path, index = False)
        tmr_line = self.working_file_content.loc[selected_idx].to_dict()

        name = tmr_line['name']
        num = tmr_line['num']
        sd = tmr_line['sd']
        st = tmr_line['st']
        ed = tmr_line['ed']
        et = tmr_line['et']
        req = tmr_line['req']
        sup = tmr_line['su']

        # FIND A WAY TO GET A PATH TO A FOLDER BY CLICKING ON IT, PERFERABLY WITHOUT POP UPS
        to_paste = os.path.join(self.path, f'{f_name}.csv')

        with open(to_paste, mode='a') as csv_file:
            fieldnames = ['name', 'num', 'sd', 'st', 'ed', 'et', 'req', 'su']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writerow({'name': name, 'num': num, 'sd': sd, 'st': st, 'ed': ed, 'et': et, 'req': req, 'su': sup})

        csv_file.close()
        print('file save')

        self.working_file_content.drop(self.working_file_content.index[selected_idx], inplace = True)

        same_path = os.path.join(self.path, f'{self.working_file_name}.csv')
        self.working_file_content.to_csv(same_path, index = False)

        self.updating = True
        self.update_file_shown()
# STILL NEED TO FIX EDITING TMR ITEMS
    def save_edit(self):
        name = self.edt_tmr_name.get()
        num = self.edt_tmr_num.get()
        sd = self.edt_tmr_sd.get()
        st = self.edt_tmr_st.get()
        ed = self.edt_tmr_ed.get()
        et = self.edt_tmr_et.get()
        req = self.edt_tmr_req.get()
        sup = self.edt_tmr_sup.get()
        self.pop_up.destroy()

        for d in self.file_dic:
            if d['num'] == self.edit_tmr_num:
                ind = self.file_dic.index(d)
                d['name'] = name
                d['num'] = num
                d['sd'] = sd
                d['st'] = st
                d['ed'] = ed
                d['et'] = et
                d['req'] = req
                d['su'] = sup
                nl = d
        # print(ind)
        self.file_dic[ind] = nl

        file_path = os.path.join(self.path, f'{self.working_file_name}.csv')
        print(file_path)

        df = pandas.DataFrame(self.file_dic)
        print(f'type of object is: {type(df)}')
        self.working_file_content = df
        # SAVE THE LIST OF DICTONAIRS TO THE FILE
        self.working_file_content.to_csv(file_path, index = False)
        print(df)        
        
        print('file save')

        self.updating = True
        self.update_file_shown()

    def edit_tmr(self):
        selected_idx = int(self.tmrs_list.curselection()[0])
        self.copied_line = self.tmrs_list.get(selected_idx)

        tmr_line = self.working_file_content.loc[selected_idx].to_dict()
        self.edit_tmr_num = tmr_line['num']
        # print(tmr_line['num'])
        
        win = tk.Toplevel(background='grey15')
        win.wm_title("Editing TMR")

        win.grid_rowconfigure(0, weight = 1)
        win.grid_columnconfigure(0, weight = 1)

        name_l = tk.Label(win, text="Enter TMR Name", background='grey15')
        name_l.grid(row=0, column=0, padx=5, pady=5)

        name = tk.Entry(win, background='grey15')
        name.insert(0, tmr_line['name'])
        name.focus_set()
        name.grid(row=1, column=0, padx=5, pady=5)

        num_l = tk.Label(win, text="Enter TMR Number", background='grey15')
        num_l.grid(row=2, column=0, padx=5, pady=5)

        num = tk.Entry(win, background='grey15')
        num.insert(0, tmr_line['num'])
        num.grid(row=3, column=0, padx=5, pady=5)

        start_date_l = tk.Label(win, text="Enter TMR Start Date", background='grey15')
        start_date_l.grid(row=4, column=0, padx=5, pady=5)

        start_date = tk.Entry(win, background='grey15')
        start_date.insert(0, tmr_line['sd'])
        start_date.grid(row=5, column=0, padx=5, pady=5)

        start_time_l = tk.Label(win, text="Enter TMR Start Time", background='grey15')
        start_time_l.grid(row=6, column=0, padx=5, pady=5)

        start_time = tk.Entry(win, background='grey15')
        start_time.insert(0, tmr_line['st'])
        start_time.grid(row=7, column=0, padx=5, pady=5)

        end_date_l = tk.Label(win, text="Enter TMR End Date", background='grey15')
        end_date_l.grid(row=0, column=1, padx=5, pady=5)

        end_date = tk.Entry(win, background='grey15')
        end_date.insert(0, tmr_line['ed'])
        end_date.grid(row=1, column=1, padx=5, pady=5)

        end_time_l = tk.Label(win, text="Enter TMR End Time", background='grey15')
        end_time_l.grid(row=2, column=1, padx=5, pady=5)

        end_time = tk.Entry(win, background='grey15')
        end_time.insert(0, tmr_line['et'])
        end_time.grid(row=3, column=1, padx=5, pady=5)

        req_l = tk.Label(win, text="Enter TMR Requirements", background='grey15')
        req_l.grid(row=4, column=1, padx=5, pady=5)

        req = tk.Entry(win, background='grey15')
        req.insert(0, tmr_line['req'])
        req.grid(row=5, column=1, padx=5, pady=5)

        sup_l = tk.Label(win, text="Enter TMR Supporting Unit", background='grey15')
        sup_l.grid(row=6, column=1, padx=5, pady=5)

        sup = tk.Entry(win, background='grey15')
        sup.insert(0, tmr_line['su'])
        sup.grid(row=7, column=1, padx=5, pady=5)

        self.edt_tmr_name = name
        self.edt_tmr_num = num
        self.edt_tmr_sd = start_date
        self.edt_tmr_st = start_time
        self.edt_tmr_ed = end_date
        self.edt_tmr_et = end_time
        self.edt_tmr_req = req
        self.edt_tmr_sup = sup
        self.index = selected_idx
        self.pop_up = win

        # THIS REMOVES THE TMR LINE AND SAVES TO FILE
        # self.working_file_content.drop(self.working_file_content.index[selected_idx], inplace = True)
        # print(self.file_dic)
        # same_path = os.path.join(self.path, f'{self.working_file_name}.csv')
        # self.working_file_content.to_csv(same_path, index = False)

        b = tk.Button(win, text="Enter", background='grey15', command = self.save_edit)
        b.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

    def finish_import(self):
        tmrs = []

        file_path = os.path.join(self.path, f'{self.working_file_name}.csv')
        print(file_path)

        for i in self.missing_tmrs:
            n = i.get()
            tmrs.append(n)

        with open(file_path, mode='a') as csv_file:
            fieldnames = ['name', 'num', 'sd', 'st', 'ed', 'et', 'req', 'su']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            for i, v in zip(tmrs, self.not_included_tmrs):
                name = v['name']
                num = v['num']
                sd = v['st']
                st = v['sd']
                ed = v['ed']
                et = v['et']
                req = i
                sup = v['su']
                # print(f"'name': {name}, 'num': {num}, 'sd': {sd}, 'st': {st}, 'ed': {ed}, 'et': {et}, 'req': {req}, 'su': {sup}")
                writer.writerow({'name': name, 'num': num, 'sd': sd, 'st': st, 'ed': ed, 'et': et, 'req': req, 'su': sup})
                # FIX THE PROBLEM WITH ADDING A NEW LINE TO END OF LINE

        csv_file.close()
        self.w.destroy()
        print('file save')

        self.updating = True
        self.update_file_shown()

    def import_pop(self):
        win = tk.Toplevel(background='grey15')
        win.wm_title("Add new TMRs")
        # win.geometry('800x500')

        # BUILD A SCROLL VIEW TO FIT ALL THE ITEMS
        c = tk.Canvas(win, width=755, height=500, background='grey15')
        scroll_y = tk.Scrollbar(win, orient="vertical", command=c.yview)

        frame = tk.Frame(c, background='grey15')
        # group of widgets
        title = tk.Label(frame, background='grey15', text='Missing TMRs\nWould you like to add these missing TMRs to tracker?')
        title.grid(row=0, column=0, columnspan=2, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.missing_tmrs = []
        missing_names = []

        print(self.not_included_tmrs)
        for l in self.not_included_tmrs:
            pl = self.not_included_tmrs.index(l)
            n = tk.Label(frame, text=f"{l['name']}, #{l['num']} Requirements: ", background='grey15')
            n.grid(row=(pl+1), column=0, sticky=tk.E, padx=10, pady=10)
            en = tk.Entry(frame, background='LightSteelBlue4')
            en.grid(row=(pl+1), column=1, sticky=tk.W, padx=10, pady=10)
            self.missing_tmrs.append(en)
            missing_names.append(n)

        if len(self.missing_tmrs) == 0:
            n = tk.Label(frame, text=f"No TMR's need to be added...", background='grey15')
            n.grid(row=1, column=0, sticky=tk.E, padx=10, pady=10)

        self.w = win
        b = tk.Button(frame, background='LightSteelBlue4', text='Add TMRs',command=self.finish_import)
        b.grid(row=(len(self.not_included_tmrs)+2), column=0, columnspan=2, pady=10)

        # put the frame in the canvas
        c.create_window(0, 0, anchor='nw', window=frame)
        # make sure everything is displayed before configuring the scrollregion
        c.update_idletasks()

        c.configure(scrollregion=c.bbox('all'), yscrollcommand=scroll_y.set)

        c.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        scroll_y.grid(row=0, column=1, sticky=(tk.N, tk.E, tk.S))

        win.grid_rowconfigure(0, weight = 1)
        win.grid_columnconfigure(0, weight = 1)

    def import_to_compare(self):
        file_path = filedialog.askopenfilename()
        # print(type(file_path))

        # NEED TO CHAGNGE FROM DOWNLOAD TO OPENING FOLDER TO PICK FILE
        if file_path.endswith('.xls'):
            i_file = pandas.read_excel(file_path).to_csv(f'{self.path}/imported.csv')

            conv_csv = pandas.read_csv(f'{self.path}/imported.csv')

            lines = []
            for index, line in conv_csv.iterrows():
                if index > 0:
                    l = line.to_dict()
                    lines.append(l)
            
            # convert from unnameed as key to name, num, sd, etc...
            self.im_tmr_list = []
            for l in lines:
                if type(l['Unnamed: 1']) != float:
                    sd_t = l['Unnamed: 3']
                    ed_t = l['Unnamed: 5']
                    sd = f'{sd_t[6:10]}{sd_t[:2]}{sd_t[3:5]}'
                    # print(sd)
                    st = f'{sd_t[11:17]}'
                    ed = f'{ed_t[6:10]}{ed_t[:2]}{ed_t[3:5]}'
                    # print(ed)
                    et = f'{ed_t[11:17]}'
                    st = st.replace(':', '')
                    et = et.replace(':', '')
                    t_item = {'name': l['Unnamed: 9'], 'num': l['Unnamed: 1'], 
                            'sd': sd, 'st': st, 'ed': ed, 'et': et, 'req': 'tbd', 'su': l['Unnamed: 8']}
                    self.im_tmr_list.append(t_item)

            self.current_tmrs = []
            for tmr in self.file_dic:
                for k, v in tmr.items():
                    if k == 'num':
                        self.current_tmrs.append(v)

            self.not_included_tmrs = []
            for tmr in self.im_tmr_list:
                for k, v in tmr.items():
                    if k == 'num':
                        if v in self.current_tmrs:
                            print('included')
                        else:
                            print(f'{v} not in list')
                            # print(tmr)
                            # MAKE A LIST OF TMRS NOT IN LIST AND SHOW A POP UP ASKING USER IF THEY WANT TO ADD TO THE CURRENT FILE
                            self.not_included_tmrs.append(tmr)


            self.import_pop()
        else:
            print('wrong file selected...\nprobably have a pop up or something')

# THIS IS FILTERING AND EXPORTING TMR ITEMS
    def export_tmr(self):
        print("export tmr!!!")

    def find_tmr(self):
        print("find tmr!!!")

    def filter_tmr(self, fil_ty):
        # WORKING LIST
        wl = []
        # FILTERED LIST
        fl = []
        # NEW LIST
        nl = []

        for index, row in self.working_file_content.iterrows():
            mod_row = row.to_dict()
            wl.append(mod_row)
        
        if fil_ty == 'unit':
            # print(f'filter by {fil_ty}')
            for i in wl:
                for k, v in i.items():
                    if k == 'su':
                        fl.append(v)
                        
            # for i in sorted(fl):
            #     for l in wl:
            #         if i in l['name']:
            #             nl.append(l)
            s = sorted(fl)
            num_l = []
            for i in s:
                ind = s.index(i)
                for l in wl:
                    if l['name'] == i:
                        # print(f"index: {ind}, name: {i},num: {l['num']}")
                        # STILL DUPLICATING
                        num_l.append(l['num'])
            
            #print(num_l)
            nu_l = set(num_l)
            for n in nu_l:
                ind = num_l.index(n)
                print(f'{n}, index of {ind}')
                for l in wl:
                    if n in list(l['num']):
                        print(l['name'])

        elif fil_ty == 'date':
            print(f'filter by {fil_ty}')
        
        for i in fl:
            print(i)

# ALL THIS IS LOGIC TO CREATE/DELETE/RENAME FILES
    def create_file(self):
        name = self.new_file.get()
        self.pop_up.destroy()

        path = os.path.abspath('tracker_files')
        file_path = os.path.join(path, f'{name}.csv')

        with open(file_path, mode='w') as csv_file:
            fieldnames = ['name', 'num', 'sd', 'st', 'ed', 'et', 'req', 'su']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()

        csv_file.close()
        self.update_files_list()

    def add_new_file(self):
        win = tk.Toplevel(background='grey15')
        win.wm_title("Add new file")

        win.grid_rowconfigure(0, weight = 1)
        win.grid_columnconfigure(0, weight = 1)
        win.grid_columnconfigure(1, weight = 1)

        l = tk.Label(win, text="Enter file Name", background='grey15')
        l.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        i = tk.Entry(win, background='grey15')
        i.focus_set()
        i.grid(row=1, column=0, padx=5, pady=5)

        self.new_file = i
        self.pop_up = win

        b = tk.Button(win, text="Enter", background='grey15', command = self.create_file)
        b.grid(row=1, column=1, padx=5, pady=5)

    def del_file(self):
        selected_idx = int(self.files_list.curselection()[0])
        self.selected_file_to_delete = self.files_list.get(selected_idx)

        deleted_file = f'{self.selected_file_to_delete}.csv'

        path = os.path.abspath('tracker_files')
        file_path = os.path.join(path, f'{deleted_file}')

        os.remove(file_path)

        self.update_files_list()
    
    def rename(self):
        name = self.selected_file_new_name.get()
        self.pop_up.destroy()

        selected_idx = int(self.files_list.curselection()[0])
        self.selected_file_to_rename = self.files_list.get(selected_idx)

        rename_file = f'{self.selected_file_to_rename}.csv'
        new_name = f'{name}.csv'

        old_path = os.path.join(self.path, f'{rename_file}')
        new_path = os.path.join(self.path, new_name)

        os.rename(old_path, new_path)

        self.update_files_list()
    
    def rename_file(self):
        win = tk.Toplevel(background='grey15')
        win.wm_title("Rename file")

        win.grid_rowconfigure(0, weight = 1)
        win.grid_columnconfigure(0, weight = 1)
        win.grid_columnconfigure(1, weight = 1)

        l = tk.Label(win, text="Enter new file Name", background='grey15')
        l.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        i = tk.Entry(win, background='grey15')
        i.focus_set()
        i.grid(row=1, column=0, padx=5, pady=5)

        self.selected_file_new_name = i
        self.pop_up = win

        b = tk.Button(win, text="Enter", background='grey15', command = self.rename)
        b.grid(row=1, column=1, padx=5, pady=5)

'''
KEEPS LOOP RUNNING HERE
'''
root = tk.Tk()
root.geometry("1200x600")
app = Application(master=root)
app.mainloop()

# TO DO LIST
# FIX FILTERING
# FIX EXPORT AS A .TXT FILE AND PRINT
# FIX FIND TMR BUTTON