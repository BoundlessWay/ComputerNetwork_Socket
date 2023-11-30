#!/usr/bin/env python3
# client_gui.py

import tkinter as tk 
from tkinter import messagebox
from tkinter import *
import json
import socket
import tkinter as tk
import os

cwd = os.path.abspath(os.getcwd())
assets_path = os.path.join(cwd, 'assets/') 

LARGE_FONT = ("Crystal", 13)

# s.connect(('127.0.0.1', 5566))
check = 0
t404 = os.path.join(assets_path, "t4042_2.png")
ip = os.path.join(assets_path, "input_ip_1.png")
co = os.path.join(assets_path, "connect_4.png")
info = os.path.join(assets_path, "info.png")
# -------------------------------
MAN_SHELL = """
Dac Cong's Currency Interactive Shell
Commands:
    help        print this manual`
    latest      request the most recent exchange rate data (base: EUR)
    historical  request historical rates for a specific day (base: EUR)
    convert     convert any amount from one currency to another using real-time exchange rates
    timeseries  request exchange rates for a specific period of time
    login       login an account
    logout      logout
    register    register an account
Run <command> -h for more information
"""

MAN_LATEST = """
latest - Request the most recent exchange rate data (base: EUR)
Usage:  
    latest -h                   help
    latest                      return all symbols
    latest [<list of symbols>]  return specified symbols
Return: 
    json-like string data
"""

MAN_HISTORICAL = """
historical - Request historical rates for a specific day (base: EUR)
Usage:
    historical -h                       help
    historical <date>                   return all symbols
    historical <date> <list of symbols> return specified symbols
    date format is YYYY-MM-DD
Return:
    json-like string data
"""

MAN_CONVERT = """
convert - Convert any amount from one currency to another
Usage:
    convert -h                          help
    convert                             return all symbols
    convert <date> <list of symbols>    return specified symbols
Return:
    json-like string data
"""

MAN_TIMESERIES = """
timeseries - request exchange rates for a specific period of time
Usage:
    timeseries -h       help
    timeseries <start date> <end date> <base>   
                        return all symbols
    timeseries <start date> <end date> <base> <list of symbols> 
                        return specified symbols
Return:
    json-like string data
"""

MAN_LOGIN = """
login - login
Usage:
    login <username> <password>
Return:
    if success: return string "Logged in successfully"
    if account incorrect: return string "Username or password incorrect!"
"""

MAN_REGISTER = """
register - register account
Usage:
    register <username> <password>
Return:
    if account exists: return string "Account already exists"
    if success: return string "Account successfully registered"
"""

MAN_QUIT = """f
quit
Usage: 
    quit
Return:
    string "Quitted"
"""

# -------------------------------
class Frame404(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.backgroundImg = PhotoImage(file=t404)
            self.background = Label( self, image = self.backgroundImg)
            self.background.place(x = 0,y = 0)
            button_back = tk.Button(self, text="Back Home",bg="SteelBlue4",fg='floral white', command=lambda: controller.showFrame(Frame_inputIP))
            button_back.place(x = 335, y = 330, width= 100)
            # self.resizable(width=False, height=False)
class Frame_inputIP(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.backgroundImg = PhotoImage(file=ip)
            self.background = Label( self, image = self.backgroundImg)
            self.background.place(x = 0,y = 0)
            Input_IP = Entry(self,bd=0, font=("Microsoft Sans Serif",12),justify="center")
            Input_IP.place(x = 284, y = 195, width = 185, height=40)
            self.connectBtnImg = PhotoImage(file=co)
            self.connectBtn = Button(self,image=self.connectBtnImg,bg="#202c3c", bd=0, command=lambda: controller.Connect_server(Input_IP, check))
            self.connectBtn.place(x = 330, y = 281)
            

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#e3d5b8")

        label_title = tk.Label(self, text="CURRENCY RATE", font=("Algerian", 13),fg="#253250",bg="#e3d5b8")
        label_user = tk.Label(self, text="username ",fg="#253250",bg="#e3d5b8",font='verdana 10 ')
        label_pswd = tk.Label(self, text="password ",fg="#253250",bg="#e3d5b8",font='verdana 10 ')

        label_notice = tk.Label(self,text="",bg="#e3d5b8", fg="#253250")
        entry_user = tk.Entry(self,width=20,bg='Ivory1')
        entry_pswd = tk.Entry(self,width=20,bg='Ivory1')

        button_log = tk.Button(self,text="LOG IN", bg="#253250", fg='#e3d5b8',command=lambda: controller.LogIn(entry_user, entry_pswd, label_notice )) 
        button_log.configure(width=10)
        button_sign = tk.Button(self,text="SIGN UP", bg="#253250",fg='#e3d5b8', command=lambda: controller.SignUp(entry_user, entry_pswd,label_notice)) 
        button_sign.configure(width=10)
        label_title.pack()
        label_user.pack()
        entry_user.pack()
        label_pswd.pack()
        entry_pswd.pack()
        label_notice.pack()

        button_log.pack()
        button_sign.pack(pady=5)



#-----------------------------------
class LatestFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#e3d5b8")
        self.grid_columnconfigure([0,1,2], weight=1)
        self.grid_rowconfigure(3, weight=1)

        label_title = tk.Label(self, text="CURRENCY RATE", font=LARGE_FONT, fg="#253250",bg="#e3d5b8", pady=2)
        label_title.grid(row=0, column=1)
        label_hist = tk.Label(self, text="{ Latest }", font=("Algerian", 13), fg='#253250',bg="#e3d5b8")
        label_hist.grid(row=1, column=1)
        label_title = tk.Label(self, text="Search", font=LARGE_FONT,fg='#253250',bg="#e3d5b8")
        label_title.grid(row=2, column=0, sticky='e')

        list_result = tk.Listbox(self,font = ("Century", 12),bg="Ivory1")
        scrbar = tk.Scrollbar(list_result, orient=VERTICAL)
        list_result.config(yscrollcommand=scrbar.set)
        scrbar.config(command=list_result.yview)

        
        list_result.grid(row=3, column=0, sticky='news', columnspan=3, pady=10, padx=50)
        scrbar.pack(side=RIGHT, fill=BOTH)
        entry_list = tk.Entry(self, bg='Ivory1')
        entry_list.grid(row=2, column=1, sticky='ew', padx=10)

        self.button_infoImg = PhotoImage(file=info)
        self.button_info = Button(self,image=self.button_infoImg,bg="#e3d5b8", bd=0, command=lambda: controller.msgb(MAN_LATEST))
        self.button_info.place(x = 0, y = 0)
        button_go = tk.Button(self,text="GO !",font=("Crystal", 10),bg="#253250",fg='#e3d5b8',command=lambda: controller.request_latest(entry_list, list_result)) 
        button_go.grid(row=2, column=2, sticky='w')
        button_quit = tk.Button(self,text="Quit",font=("Crystal", 10),bg="#660000",fg='#e3d5b8',command=lambda: controller.quit()) 
        button_quit.grid(row=0, column=2, sticky='e', pady= 2, padx=10)
        button_latest = tk.Button(self,text="Historical >",bg="#253250",fg='#e3d5b8',command=lambda: controller.showFrame(HistoricalFrame)) 
        button_latest.grid(row=4, column=0, pady= 5)
        button_convert = tk.Button(self,text="Convert >",bg="#253250",fg='#e3d5b8',command=lambda: controller.showFrame(ConvertFrame)) 
        button_convert.grid(row=4, column=2, pady= 5)
        button_latest = tk.Button(self,text="Time Series",bg="#253250", width=15,fg='#e3d5b8',command=lambda: controller.showFrame(TimeSeriesFrame)) 
        button_latest.grid(row=4, column=1)
        button_latest = tk.Button(self,text="Log Out",bg="#253250", width=15,fg='#e3d5b8',command=lambda: controller.logout()) 
        button_latest.grid(row=5, column=1, pady= 10)
# ------------------------------------
class HistoricalFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#e3d5b8")
        self.grid_columnconfigure([0,1,2], weight=1)
        self.grid_rowconfigure(4, weight=1)

        label_title = tk.Label(self, text="CURRENCY RATE", font=LARGE_FONT,fg="#253250",bg="#e3d5b8")
        label_title.grid(row=0, column=1)
        label_hist = tk.Label(self, text="{ Historical }", font=("Algerian", 13), fg="#253250",bg="#e3d5b8")
        label_hist.grid(row=1, column=1)
        label_hist = tk.Label(self, text="Date", font=LARGE_FONT, fg="#253250",bg="#e3d5b8")
        label_hist.grid(row=2, column=0, sticky='e')
        label_hist = tk.Label(self, text="Search", font=LARGE_FONT, fg="#253250",bg="#e3d5b8")
        label_hist.grid(row=3, column=0, sticky='e')

        entry_date = tk.Entry(self, bg='Ivory1')
        entry_date.grid(row=2, column=1, sticky='ew', padx=10)
        entry_list = tk.Entry(self, bg='Ivory1')
        entry_list.grid(row=3, column=1, sticky='ew', padx=10)


        self.button_infoImg = PhotoImage(file=info)
        self.button_info = Button(self,image=self.button_infoImg,bg="#e3d5b8", bd=0, command=lambda: controller.msgb(MAN_HISTORICAL))
        self.button_info.place(x = 0, y = 0)
        button_go = tk.Button(self,text="GO !",bg="#253250",fg='#e3d5b8',command=lambda: controller.request_historical( entry_date, entry_list, list_result)) 
        button_go.grid(row=3, column=2, sticky='w')
        button_quit = tk.Button(self,text="Quit",font=("Crystal", 10),bg="#660000",fg='#e3d5b8',command=lambda: controller.quit()) 
        button_quit.grid(row=0, column=2, sticky='e', pady= 5, padx=10)
        button_latest = tk.Button(self,text="Latest >",bg="#253250",fg='#e3d5b8',command=lambda: controller.showFrame(LatestFrame)) 
        button_latest.grid(row=5, column=0, pady= 5)
        button_convert = tk.Button(self,text="Convert >",bg="#253250",fg='#e3d5b8',command=lambda: controller.showFrame(ConvertFrame)) 
        button_convert.grid(row=5, column=2, pady=5)
        button_latest = tk.Button(self,text="Time Series",bg="#253250", width=15,fg='#e3d5b8',command=lambda: controller.showFrame(TimeSeriesFrame)) 
        button_latest.grid(row=5, column=1, pady= 5)
        button_Log = tk.Button(self,text="Log Out",bg="#253250", width=15,fg='#e3d5b8',command=lambda: controller.logout()) 
        button_Log.grid(row=7, column=1, pady= 10)


        list_result = tk.Listbox(self,font = ("Century", 12),bg='Ivory1')
        scrbar = tk.Scrollbar(list_result, orient=VERTICAL)
        list_result.config(yscrollcommand=scrbar.set)
        scrbar.config(command=list_result.yview)

        
        list_result.grid(row=4, column=0, sticky='news', columnspan=3, pady=20, padx=50)
        scrbar.pack(side=RIGHT, fill=BOTH)
class TimeSeriesFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#e3d5b8")
        self.grid_columnconfigure([0,1,2], weight=1)
        self.grid_rowconfigure(5, weight=1)

        label_title = tk.Label(self, text="CURRENCY RATE", font=LARGE_FONT,fg="#253250",bg="#e3d5b8")
        label_title.grid(row=0, column=1)
        label_TS = tk.Label(self, text="{ TimeSeries }", font=("Algerian", 13), fg="#253250",bg="#e3d5b8")
        label_TS.grid(row=1, column=1)
        label_TS = tk.Label(self, text="Start date", font=LARGE_FONT, fg="#253250",bg="#e3d5b8")
        label_TS.grid(row=2, column=0, sticky='e')
        label_TS = tk.Label(self, text="End date", font=LARGE_FONT, fg="#253250",bg="#e3d5b8")
        label_TS.grid(row=3, column=0, sticky='e')
        label_TS = tk.Label(self, text="Search", font=LARGE_FONT, fg="#253250",bg="#e3d5b8")
        label_TS.grid(row=4, column=0, sticky='e')

        entry_date_start = tk.Entry(self, bg='Ivory1')
        entry_date_start.grid(row=2, column=1, sticky='ew', padx=10)
        entry_date_end = tk.Entry(self, bg='Ivory1')
        entry_date_end.grid(row=3, column=1, sticky='ew', padx=10)
        entry_list = tk.Entry(self, bg='Ivory1')
        entry_list.grid(row=4, column=1, sticky='ew', padx=10)

        self.button_infoImg = PhotoImage(file=info)
        self.button_info = Button(self,image=self.button_infoImg,bg="#e3d5b8", bd=0, command=lambda: controller.msgb(MAN_TIMESERIES))
        self.button_info.place(x = 0, y = 0)
        button_go = tk.Button(self,text="GO !",bg="#253250",fg='#e3d5b8',command=lambda: controller.request_TimeSeries(entry_date_start, entry_date_end, entry_list, list_result)) 
        button_go.grid(row=3, column=2, sticky='w')
        button_quit = tk.Button(self,text="Quit",font=("Crystal", 10),bg="#660000",fg='#e3d5b8',command=lambda: controller.quit()) 
        button_quit.grid(row=0, column=2, sticky='e', pady= 2, padx=10)
        button_latest = tk.Button(self,text="Latest >",bg="#253250",fg='#e3d5b8',command=lambda: controller.showFrame(LatestFrame)) 
        button_latest.grid(row=6, column=0, pady= 2)
        button_convert = tk.Button(self,text="Convert >",bg="#253250",fg='#e3d5b8',command=lambda: controller.showFrame(ConvertFrame)) 
        button_convert.grid(row=6, column=2, pady=2)
        button_hist = tk.Button(self,text="Historical >",bg="#253250", width=15,fg='#e3d5b8',command=lambda: controller.showFrame(HistoricalFrame)) 
        button_hist.grid(row=6, column=1, pady= 2)
        button_latest = tk.Button(self,text="Log Out",bg="#253250", width=15,fg='#e3d5b8',command=lambda: controller.logout()) 
        button_latest.grid(row=7, column=1, pady= 10)
        list_result = tk.Listbox(self,font = ("Century", 12),bg='Ivory1')
        scrbar = tk.Scrollbar(list_result, orient=VERTICAL)
        list_result.config(yscrollcommand=scrbar.set)
        scrbar.config(command=list_result.yview)

        
        list_result.grid(row=5, column=0, sticky='news', columnspan=3, pady=20, padx=50)
        scrbar.pack(side=RIGHT, fill=BOTH)
class ConvertFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#e3d5b8")
        self.grid_columnconfigure([0,1,2], weight=1)
        self.grid_rowconfigure(6, weight=1)

        label_title = tk.Label(self, text="CURRENCY RATE", font=LARGE_FONT,fg="#253250",bg="#e3d5b8",pady=10)
        label_title.grid(row=0, column=1)
        label_convert = tk.Label(self, text="{ Convert }", font=("Algerian", 13), fg="#253250",bg="#e3d5b8")
        label_convert.grid(row=1, column=1)

        entry_from = tk.Entry(self,bg='Ivory1')
        entry_from.grid(row=2, column=1, sticky='ew', padx=5, pady=10)
        entry_to = tk.Entry(self,bg='Ivory1')
        entry_to.grid(row=3, column=1, sticky='ew', padx=5, pady=10)
        entry_amount = tk.Entry(self,bg='Ivory1')
        entry_amount.grid(row=4, column=1, sticky='ew', padx=5, pady=10)

        label_from = tk.Label(self, text="from", font=LARGE_FONT, fg="#253250",bg="#e3d5b8")
        label_from.grid(row=2, column=0, sticky='e')
        label_to = tk.Label(self, text="to", font=LARGE_FONT, fg="#253250",bg="#e3d5b8")
        label_to.grid(row=3, column=0, sticky='e')
        label_amount = tk.Label(self, text="amount", font=LARGE_FONT, fg="#253250",bg="#e3d5b8")
        label_amount.grid(row=4, sticky='e')
        
        self.button_infoImg = PhotoImage(file=info)
        self.button_info = Button(self,image=self.button_infoImg,bg="#e3d5b8", bd=0, command=lambda: controller.msgb(MAN_CONVERT))
        self.button_info.place(x = 0, y = 0)
        button_go = tk.Button(self,text="GO !",bg="#253250",fg='#e3d5b8',command=lambda: controller.request_convert(entry_from, entry_to, entry_amount, list_result)) 
        button_go.grid(row=4, column=2, sticky='w',padx=10)
        button_quit = tk.Button(self,text="Quit",font=("Crystal", 10),bg="#660000",fg='#e3d5b8',command=lambda: controller.quit()) 
        button_quit.grid(row=0, column=2, sticky='e', pady= 2, padx=10)
        button_latest = tk.Button(self,text="Latest >",bg="#253250",fg='#e3d5b8',command=lambda: controller.showFrame(LatestFrame)) 
        button_latest.grid(row=6, column=0,pady=5)
        button_his = tk.Button(self,text="Historical >",bg="#253250",fg='#e3d5b8',command=lambda: controller.showFrame(HistoricalFrame)) 
        button_his.grid(row=6, column=2,pady=5)
        button_latest = tk.Button(self,text="Time Series",bg="#253250", width=15,fg='#e3d5b8',command=lambda: controller.showFrame(TimeSeriesFrame)) 
        button_latest.grid(row=6, column=1, pady=5)
        button_latest = tk.Button(self,text="Log Out",bg="#253250", width=15,fg='#e3d5b8',command=lambda: controller.logout()) 
        button_latest.grid(row=7, column=1, pady= 5)

        list_result = tk.Listbox(self,font = ("Century", 12),bg='Ivory1')
        scrbar = tk.Scrollbar(list_result, orient=VERTICAL)
        list_result.config(yscrollcommand=scrbar.set)
        scrbar.config(command=list_result.yview)

        
        list_result.grid(row=5, column=0, sticky='news', columnspan=3, pady=10, padx=120)
        scrbar.pack(side=RIGHT, fill=BOTH)       


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("APP")
        self.geometry("500x450")
        self.resizable(width=True, height=True)

        self.protocol("WM_DELETE_WINDOW", self.onClosing)
        container = tk.Frame(self)
        container.pack(side="top", fill = "both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LatestFrame, HistoricalFrame, ConvertFrame, LoginFrame, Frame404,Frame_inputIP, TimeSeriesFrame):
            frame = F(container, self)
            self.frames[F] = frame 
            frame.grid(row=0, column=0, sticky="nsew")
        self.showFrame(Frame_inputIP) 
    def showFrame(self, Frame_name):
        frame = self.frames[Frame_name]
        if Frame_name== ConvertFrame:
            self.geometry("520x340")
        elif(Frame_name == LoginFrame):
            self.geometry("455x203")
        elif(Frame_name == Frame404):
            self.geometry("754x376")
        elif(Frame_name == Frame_inputIP):
            self.geometry("754x376")
        else:
            self.geometry("500x450")
        frame.tkraise()
    
    def onClosing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if(check != 0):
                s.close()
            self.destroy()
    def Connect_server(self, input_IP, check):
        Host = input_IP.get()
        if (check == 0):
            try:
                global s
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((Host, 5566))
                self.showFrame(LoginFrame)
                check = 1
            except:
                self.showFrame(Frame404)
        else:
            self.showFrame(LoginFrame)
    def LogIn(self, entry_user, entry_pswd, label_notice ):
        request = 'login '+ entry_user.get() + ' ' + entry_pswd.get()
        try:
            s.send(request.encode())
            data = s.recv(1024).decode()
            print(data)
            if (data == "Logged in successfully"):
                self.showFrame(LatestFrame)
            elif(entry_user.get() == "" or entry_pswd.get()==""):
                label_notice["text"] = "The above fields cannot be empty!"
            else:
                label_notice["text"] = "Username or password incorrect!"
        except:
            self.showFrame(Frame404)
    def Log_out(seft):
        # s.close()
        seft.showFrame(Frame_inputIP)
    def SignUp(self, entry_user, entry_pswd, label_notice ):
        request = 'register '+ entry_user.get() + ' ' + entry_pswd.get()
        try:
            s.send(request.encode())
            data = s.recv(1024).decode()
            print(data)
            if (data == "Account successfully registered"):
                label_notice["text"] = "Account successfully registered"
            elif(entry_user.get() == "" or entry_pswd.get()==""):
                label_notice["text"] = "The above fields cannot be empty!"
            else:
                label_notice["text"] = "Account already exists!"
        except:
            self.showFrame(Frame404)

    def request_latest(self, entry_list, list_result):
        request = 'latest ' + entry_list.get()
        try:
            s.send(request.encode())
            data = s.recv(4096).decode()
            print(data)
            if (data != "0"):
                data = json.loads(data)
                list_result.delete(0,END)
                list_result.insert(END, "                        ---RESULT (base: EUR)--- ")
                for item in data.items():
                    data = str(item) 
                    data = data.replace("(", "                                - ")
                    data = data.replace(")", "")
                    data = data.replace("'", "")
                    data = data.replace(",", ": ")
                    list_result.insert(END, data)
                    print(item)
            else:
                list_result.delete(0,END)
                data = "                                No results valid !"
                list_result.insert(END, data)
        except :
            self.showFrame(Frame404)
       
    def request_convert(self, entry_from, entry_to, entry_amount, list_result):
        request = 'convert ' + entry_from.get() + " " + entry_to.get() + " " + entry_amount.get()
        try:
            if (entry_to.get() == "" or entry_amount.get() == "" or entry_from.get() == ""):
                list_result.delete(0,END)
                data = " The above fields cannot be empty !"
                list_result.insert(END, data)
            else:
                s.send(request.encode())
                data = s.recv(1024).decode()
                print(data)
                if (data != "0"):
                    list_result.delete(0,END)
                    data = '        Result: ' + data
                    list_result.insert(END, data)
                else:
                    list_result.delete(0,END)
                    data = "                      No results valid !"
                    list_result.insert(END, data)
        except:
            self.showFrame(Frame404)
    def request_historical(self, entry_date, entry_list, list_result):
        request = 'historical ' + entry_date.get() + ' ' + entry_list.get()
        try:
            if (entry_date.get() == "" ):
                list_result.delete(0,END)
                data = "                  The date field cannot be empty !"
                list_result.insert(END, data)
            else:
                s.send(request.encode())
                data = s.recv(4096).decode()
                print(len(data))
                if (data != "0"):
                    data = json.loads(data)
                    list_result.delete(0,END)
                    list_result.insert(END, "                        ---RESULT (base: EUR)--- ")
                    for item in data.items():
                        data = str(item) 
                        data = data.replace("(","                           - ")
                        data = data.replace(")", "")
                        data = data.replace("'", "")
                        data = data.replace(",", ": ")
                        list_result.insert(END, data)
                        print(item)
                else:
                    list_result.delete(0,END)
                    data = "                                No results valid !"
                    list_result.insert(END, data)
        except:
            self.showFrame(Frame404)
    def request_TimeSeries(self, entry_date_start, entry_date_end, entry_list, list_result):
            request = 'timeseries ' + entry_date_start.get() + ' '+ entry_date_end.get() + ' ' + entry_list.get()
            try:
                if (entry_date_start.get() == "" or entry_date_end.get() == "" or entry_list.get() == ""):
                    list_result.delete(0,END)
                    data = "                 The above fields cannot be empty !"
                    list_result.insert(END, data)
                else:
                    s.send(request.encode())
                    data = s.recv(17000000).decode()
                    print(len(data))
                    if (data != "{}"):
                        print(data)
                        data = json.loads(data)
                        list_result.delete(0,END)
                        list_result.insert(END, "                        ---RESULT (base: EUR)--- ")
                        for item in data.items():
                            data = str(item) 
                            data = data.replace("(", "               - ")
                            data = data.replace(")", "")
                            data = data.replace("'", "")
                            data = data.replace("}", "")
                            data = data.replace("{", "")
                            list_result.insert(END, data)
                    else:
                        list_result.delete(0,END)
                        data = "                                No results valid !"
                        list_result.insert(END, data)
            except:
                self.showFrame(Frame404)    
    def logout(self):
        request = 'logout'
        s.send(request.encode())
        data = s.recv(4096).decode()
        if(data == "Logging out"):
            self.showFrame(LoginFrame)
        else:
            self.showFrame(Frame404) 
    def quit(self):
        msg = 'quit'
        s.send(msg.encode())
        msg = s.recv(4096).decode()
        self.destroy()
    def msgb(event, man):
        messagebox.showinfo('User manual', man)
# s.send('login a a'.encode())
# s.recv(1024)


app = App()
app.mainloop()