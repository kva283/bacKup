import os
import sys
import shutil
import configparser
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk 

class CBacKup(tk.Tk):

    strLabelSize = "Size to backup :"
    lstFoldersToSave = []

    def __init__(self):
        super().__init__()
        self.title("bacKup - save your files (by Kv@)")
        self.geometry("540x580")
        self.resizable(False,False)

        # frame de selection du fichier de configuration
        self.config_frame = tk.LabelFrame(self, text="Configuration file")
        self.config_frame.grid(row=0, column=0, columnspan=8, padx=10, pady=10, sticky=tk.NSEW)

        self.lbl_inifile = tk.Label(self.config_frame, text="INI file :")
        self.lbl_inifile.grid(row=0, column=1, padx=10, pady=10)
        self.ent_inifile = tk.Entry(self.config_frame, width=50)
        self.ent_inifile.grid(row=0, column=2, columnspan=4, padx=10, pady=10)
        self.btn_inifile = tk.Button(self.config_frame, text="Browse", command=self.BrowseIniFile)
        self.btn_inifile.grid(row=0, column=6, padx=10, pady=10)
        self.btn_loadini = tk.Button(self.config_frame, text="Load", command=self.LoadIniFile)
        self.btn_loadini.grid(row=0, column=7, padx=10, pady=10)

        # frame d'affichage des parametres
        self.param_frame = tk.LabelFrame(self, text="Parameters")
        self.param_frame.grid(row=1, column=0, rowspan=6, columnspan=8, padx=10, pady=10, sticky=tk.NSEW)

        self.lbl_dest = tk.Label(self.param_frame, text="Destination :")
        self.lbl_dest.grid(row=1, column=1, padx=10, pady=1, sticky=tk.W)
        self.lbl_dest.config(state=tk.DISABLED)
        self.ent_dest = tk.Entry(self.param_frame, width=40)
        self.ent_dest.grid(row=1, column=2, columnspan=7, padx=10, pady=1, sticky=tk.W)
        self.ent_dest.config(state=tk.DISABLED)

        self.lbl_copy = tk.Label(self.param_frame, text="Backup type :")
        self.lbl_copy.grid(row=2, column=1, padx=10, pady=1, sticky=tk.W)
        self.lbl_copy.config(state=tk.DISABLED)
        strValue = tk.StringVar()
        self.cb_copy = ttk.Combobox(self.param_frame, width=37, textvariable=strValue)
        self.cb_copy['values']=('move','copy')
        self.cb_copy.grid(row=2, column=2, columnspan=7, padx=10, pady=1, sticky=tk.W)
        self.cb_copy.config(state=tk.DISABLED)

        self.lbl_zip = tk.Label(self.param_frame, text="Compression :")
        self.lbl_zip.grid(row=3, column=1, padx=10, pady=1, sticky=tk.W)
        self.lbl_zip.config(state=tk.DISABLED)

        self.chk_zip_yes = tk.Checkbutton(self.param_frame, text="Yes")
        self.chk_zip_yes.grid(row=3, column=2, padx=10, pady=1, sticky=tk.W)
        self.chk_zip_yes.config(state=tk.DISABLED)
        self.chk_zip_no = tk.Checkbutton(self.param_frame, text="No")
        self.chk_zip_no.grid(row=3, column=3, columnspan=5, padx=10, pady=1, sticky=tk.W)
        self.chk_zip_no.config(state=tk.DISABLED)

        self.lbl_time = tk.Label(self.param_frame, text="Timestamp :")
        self.lbl_time.grid(row=4, column=1, padx=10, pady=1, sticky=tk.W)
        self.lbl_time.config(state=tk.DISABLED)

        self.chk_time_yes = tk.Checkbutton(self.param_frame, text="Yes")
        self.chk_time_yes.grid(row=4, column=2, padx=10, pady=1, sticky=tk.W)
        self.chk_time_yes.config(state=tk.DISABLED)
        self.chk_time_no = tk.Checkbutton(self.param_frame, text="No")
        self.chk_time_no.grid(row=4, column=3, columnspan=5, padx=10, pady=1, sticky=tk.W)
        self.chk_time_no.config(state=tk.DISABLED)

        self.lbl_folders = tk.Label(self.param_frame, text="Folders to backup :")
        self.lbl_folders.grid(row=5, column=1, padx=10, pady=1, sticky=tk.W)
        self.lbl_folders.config(state=tk.DISABLED)

        self.txt_folders = tk.Text(self.param_frame, height=15, width=62)
        self.txt_folders.grid(row=6, column=1, columnspan=7, padx=10, pady=10, sticky=tk.W)
        self.txt_folders.config(state=tk.DISABLED)

        self.oTextSize = StringVar()
        self.oTextSize.set( self.strLabelSize )
        self.lbl_size = tk.Label(self.param_frame, textvariable=self.oTextSize)
        self.lbl_size.grid(row=7, column=1, padx=10, pady=1, sticky=tk.W)
        self.lbl_size.config(state=tk.DISABLED)

        self.btn_backup = tk.Button(self, text="Backup", width=10, command=self.Backup)
        self.btn_backup.grid(row=8, column=6, padx=10, pady=10, sticky=tk.E)
        self.btn_exit = tk.Button(self, text="Exit", width=10, command=self.Exit)
        self.btn_exit.grid(row=8, column=7, padx=10, pady=10, sticky=tk.E)

        #init buttons
        self.btn_loadini.config(state=tk.DISABLED)
        self.btn_backup.config(state=tk.DISABLED)

    def BrowseIniFile(self):
        self.btn_inifile.config(state=tk.DISABLED)

        self.ent_inifile.delete(0, tk.END)
        self.ent_inifile.insert(0, filedialog.askopenfilename())

        self.btn_loadini.config(state=tk.NORMAL)

    def LoadIniFile(self):
        self.btn_loadini.config(state=tk.DISABLED)

        strIniFile = self.ent_inifile.get()
        config = configparser.ConfigParser()
        config.read(strIniFile)

        self.lbl_dest.config(state=tk.NORMAL)
        self.ent_dest.config(state=tk.NORMAL)
        self.ent_dest.delete(0, tk.END)
        self.ent_dest.insert(0, config['general']['Destination'])

        self.lbl_copy.config(state=tk.NORMAL)
        self.cb_copy.config(state=tk.NORMAL)
        if config['general']['MoveOrCopy']=='move':
            self.cb_copy.set('move')
        else:
            self.cb_copy.set('copy')

        self.lbl_zip.config(state=tk.NORMAL)
        self.chk_zip_yes.config(state=tk.NORMAL)
        self.chk_zip_no.config(state=tk.NORMAL)
        if config['general']['Compression']=='no':
            self.chk_zip_no.invoke()
            self.chk_zip_yes.deselect()
        else:
            self.chk_zip_yes.invoke()
            self.chk_zip_no.deselect()
        
        self.lbl_time.config(state=tk.NORMAL)
        self.chk_time_yes.config(state=tk.NORMAL)
        self.chk_time_no.config(state=tk.NORMAL)
        if config['general']['Timestamp']=='no':
            self.chk_time_no.invoke()
            self.chk_time_yes.deselect()
        else:
            self.chk_time_yes.invoke()
            self.chk_time_no.deselect()
        
        self.lbl_folders.config(state=tk.NORMAL)
        self.txt_folders.config(state=tk.NORMAL)
        self.txt_folders.delete(1.0, tk.END)
        for key in config['backup_list']:  
            self.txt_folders.insert(tk.END, config['backup_list'][key] + '\n')
            self.lstFoldersToSave.append( config['backup_list'][key] )

        self.lbl_size.config(state=tk.NORMAL)
        self.oTextSize.set( self.strLabelSize + ' ' + self.GetFoldersSize() + ' bytes.' )

        self.btn_backup.config(state=tk.NORMAL)

    def Backup(self):
        #src = self.source_entry.get()
        #dst = self.destination_entry.get()
        tk.messagebox.showinfo("bacKup", "/!\ TODO /!\ ... Backup completed successfully!")

    def Exit(self):
        sys.exit()
    
    def GetFoldersSize(self):
        nTotalSize = 0

        for folder in self.lstFoldersToSave:
            for path, dirs, files in os.walk(folder):
                for f in files:
                    fp = os.path.join(path, f)
                    nTotalSize += os.path.getsize(fp)

        return str(nTotalSize)

if __name__ == "__main__":
    app = CBacKup()
    app.mainloop()