import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from PIL import Image,ImageTk
import subprocess
import platform
import sys
import threading
import StarryScanner

scanner=tk.Tk()
scanner.title('StarryScanner')
scanner.geometry('600x700')

pic=Image.open('/home/alphakennybody/Downloads/space.png')
picresize=pic.resize((600,700),Image.Resampling.LANCZOS)
realpic=ImageTk.PhotoImage(picresize)
scanner.realpic=realpic
bg_lbl=tk.Label(scanner,image=scanner.realpic)
bg_lbl.place(x=0,y=0,relwidth=1,relheight=1)

class TerminalThings:
    def __init__(self,text_widget):
        self.text_widget=text_widget
    def write(self,input_str):
        self.text_widget.insert(tk.END,input_str)
        self.text_widget.see(tk.END)
    def flush(self):
        pass

ip_lbl=tk.Label(scanner,text='target IPv4 address:',fg='#9A9FC1',bg='black')
ip_lbl.pack(pady=10)
ip_entry=tk.Entry(scanner)
ip_entry.pack(pady='20')

def start_scan():
    target_server=ip_entry.get()
    threading.Thread(target=StarryScanner.everything,args=(target_server,),daemon=True).start()

start_button=tk.Button(scanner,text='start scan',command=start_scan,fg='green',bg='black')
start_button.pack(pady='10')

def shutdown():
    global os_version
    os_version=platform.system().lower()
    if os_version=='windows':
        subprocess.run(['shutdown','s','t','1'])
    if os_version in ['linux','darwin']:
        messagebox.showwarning('Lucky...',f'I only shut-down Windows users.')
        return

shutdown_button=tk.Button(scanner,text='shut-down',command=lambda:shutdown())
shutdown_button.pack(pady='5')

terminal=scrolledtext.ScrolledText(scanner,bg='black',fg='green')
terminal.pack(pady=20,padx=40,fill=tk.BOTH,expand=True)

sys.stdout=TerminalThings(terminal)

scanner.mainloop()