
import socket
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import *
import json
import threading
from tkinter import font
import time
from datetime import date
from datetime import datetime
import struct


HOST = '192.168.56.1'
# HOST = '127.0.0.1'
PORT = 5566


class CLIENT:
	def __init__(self):
		self.server_Host = HOST
		self.server_Port = PORT
		self.message_Format = "utf8"
		self.client_Socket = ""
		self.client_App = {}
		self.today = date.today()
		self.outdated_Date = ""
		self.received_Data = {}


	def auto_Input_IP_And_Port(self):
		if self.client_App['chb_Connect_Value'].get() == 1:
			self.client_App['ent_IP_Address'].delete(0, tk.END)
			self.client_App['ent_Port'].delete(0, tk.END)
			self.client_App['ent_IP_Address'].insert(0, self.server_Host)
			self.client_App['ent_Port'].insert(0, str(self.server_Port))
		else:
			self.client_App['ent_IP_Address'].delete(0, tk.END)
			self.client_App['ent_Port'].delete(0, tk.END)
			

	def show_Password(self):
		if self.client_App['chb_Show_Value'].get() == 1:
			self.client_App['ent_Password']['show'] = ""
		else:
			self.client_App['ent_Password']['show'] = "*"


	def connect_Server(self):
		if (self.client_App["ent_IP_Address"].get() == self.server_Host and self.client_App["ent_Port"].get() == str(self.server_Port)):
			self.run_Client()

		else:
			self.show_Frame("frm_404")
			
 
	def show_Frame(self, frame_Name):

		if frame_Name == "frm_Connect": self.client_App['window'].geometry("568x150")
		elif frame_Name == "frm_404": self.client_App['window'].geometry("754x376")
		elif frame_Name == "frm_Login_And_Register": self.client_App['window'].geometry("380x435")
		else: self.client_App['window'].geometry("1200x640")
		frame = self.client_App[frame_Name]
		frame.tkraise()


	def create_Frame_Connect_Server(self):
		name_Frame = "frm_Connect"
		self.client_App[name_Frame] = tk.Frame(master=self.client_App["frm_Container"])
		self.client_App[name_Frame].grid(row=0, column=0, sticky="nsew")
		self.client_App[name_Frame].configure(bg="#3b4b4d")

		self.client_App["lbl_IP_Address"] = tk.Label(master=self.client_App[name_Frame], text="IP Address",fg='#7b9de0', bg="#3b4b4d")
		self.client_App["ent_IP_Address"] = tk.Entry(master=self.client_App[name_Frame], width=20, bg="#7b9de0")
		self.client_App['chb_Connect_Value'] = tk.IntVar()
		self.client_App['chb_Automatic'] = tk.Checkbutton(master=self.client_App[name_Frame], text="Automatic", fg='#7b9de0', bg="#3b4b4d", command=self.auto_Input_IP_And_Port, variable=self.client_App['chb_Connect_Value'], activebackground='#3b4b4d', activeforeground='#7b9de0', selectcolor='#3b4b4d')
		self.client_App["lbl_IP_Address"].grid(row=0, column=0, sticky="w", padx=30, pady=(30, 0))
		self.client_App["ent_IP_Address"].grid(row=1, column=0, padx=30, pady=(0, 0))
		self.client_App['chb_Automatic'].grid(row=2, column=0, sticky="w", padx=25, pady=(10, 30))
  
		self.client_App["lbl_Port"] = tk.Label(master=self.client_App[name_Frame], text="Port", fg='#7b9de0', bg="#3b4b4d")
		self.client_App["ent_Port"] = tk.Entry(master=self.client_App[name_Frame], width=20, bg="#7b9de0")
		self.client_App["lbl_Port"].grid(row=0, column=1, sticky="w", padx=30, pady=(30,0))
		self.client_App["ent_Port"].grid(row=1, column=1, padx=30, pady=(0, 0))

		self.client_App["btn_Connect"] = tk.Button(master=self.client_App[name_Frame], width=10, text="Connect", bg="#7b9de0", command=self.connect_Server)
		self.client_App["btn_Connect"].grid(row=1, column=2, padx=(45, 60), pady=(0, 0), sticky="nsew")
  

	def create_Frame_404(self):
		name_Frame = "frm_404"
		self.client_App[name_Frame] = tk.Frame(master=self.client_App["frm_Container"])
		self.client_App[name_Frame].grid(row=0, column=0, sticky="nsew")

		self.client_App["img_Background_404"] = tk.PhotoImage(file="p404.png")
		self.client_App['lbl_Background'] = tk.Label(self.client_App[name_Frame], image = self.client_App["img_Background_404"])
		self.client_App['lbl_Background'].place(x = 0,y = 0)
		self.client_App['btn_Back_Connect_Frame'] = tk.Button(self.client_App[name_Frame], text="Back Home",bg="SteelBlue4",fg='floral white', command=lambda: self.show_Frame("frm_Connect"))
		self.client_App['btn_Back_Connect_Frame'].place(x = 335, y = 330, width= 100)
  

	def create_Frame_Login_And_Register(self):
		name_Frame = "frm_Login_And_Register"
		self.client_App[name_Frame] = tk.Frame(master=self.client_App["frm_Container"])
		self.client_App[name_Frame].grid(row=0, column=0, sticky="nsew")
		self.client_App[name_Frame].configure(bg="#000000")
  
		self.client_App['btn_Disconnect_LAR'] = tk.Button(master=self.client_App[name_Frame], text="DISCONNECT", fg="#000000", bg='#792899', width=10, command=self.stop_Connect)
		self.client_App['lbl_Name_App'] = tk.Label(master=self.client_App[name_Frame], text="CURRENCY RATE", font=("Algerian", 20), fg='#aba30a', bg="#000000")
		self.client_App['lbl_Username'] = tk.Label(master=self.client_App[name_Frame], text="Username", fg='#aba30a', bg="#000000", font=('verdana', 12))
		self.client_App['ent_Username'] = tk.Entry(master=self.client_App[name_Frame], width=20, bg='#aba30a', font=('verdana', 13))
		self.client_App['lbl_Password'] = tk.Label(master=self.client_App[name_Frame], text="Password", fg='#aba30a', bg="#000000", font=('verdana', 12))
		self.client_App['ent_Password'] = tk.Entry(master=self.client_App[name_Frame], width=20, bg='#aba30a', font=('verdana', 13), show="*")
		self.client_App['chb_Show_Value'] = tk.IntVar()
		self.client_App['chb_Show_Password'] = tk.Checkbutton(master=self.client_App[name_Frame], text="Show Password", bg="#000000", fg="#aba30a", activebackground="#000000", activeforeground="#aba30a", selectcolor="#000000", variable=self.client_App['chb_Show_Value'], command=self.show_Password)
		self.client_App['lbl_Notification'] = tk.Label(master=self.client_App[name_Frame], text="", fg='#aba30a', bg="#000000", font=('verdana', 8))		
  
		self.client_App['btn_Disconnect_LAR'].place(x=0, y=0)
		self.client_App['lbl_Name_App'].pack(pady=(50, 20))
		self.client_App['lbl_Username'].pack(pady=(15, 0))
		self.client_App['ent_Username'].pack()
		self.client_App['lbl_Password'].pack(pady=(20, 0))
		self.client_App['ent_Password'].pack()
		self.client_App['chb_Show_Password'].place(x=73, y=240)
		self.client_App['lbl_Notification'].pack(pady=(40, 0))

		self.client_App['btn_Login'] = tk.Button(master=self.client_App[name_Frame], text="LOG IN", bg="#aba30a", fg='#000000', width=10, command=self.request_Login) 
		self.client_App['btn_Register'] = tk.Button(master=self.client_App[name_Frame], text="REGISTER", bg="#aba30a", fg='#000000', width=10, command=self.request_Register) 
		self.client_App['btn_Login'].pack(pady=(30, 0))
		self.client_App['btn_Register'].pack(pady=15)


	def create_Frame_Search_Currency_Rate(self):
		name_Frame = "frm_Search_Currency_Rate"
		self.client_App[name_Frame] = tk.Frame(master=self.client_App["frm_Container"])
		self.client_App[name_Frame].grid(row=0, column=0, sticky="nsew")
		self.client_App[name_Frame].configure(bg="#000000")
		self.client_App[name_Frame].option_add("*TCombobox*Listbox.background", '#aba30a')
		self.client_App[name_Frame].option_add("*TCombobox*Listbox.foreground", 'black')
		self.client_App[name_Frame].option_add("*TCombobox*Listbox.selectBackground", 'black')
		self.client_App[name_Frame].option_add("*TCombobox*Listbox.selectForeground", '#aba30a')
		combostyle = ttk.Style()
		scrollbar = ttk.Style()
		combostyle.theme_create('combostyle', parent='alt', settings = {'TCombobox': {'configure': {'fieldbackground': '#aba30a', 'background': '#000000', 'arrowcolor': '#aba30a'}}})
		combostyle.theme_use('combostyle')
		combostyle.configure('Vertical.TScrollbar',background = "#aba30a", troughcolor='#000000', bordercolor='#aba30a', arrowcolor="#000000") 
		ttk.Style(self.client_App[name_Frame]).configure("TCombobox", selectbackground="#aba30a", selectforeground='#000000')
		scrollbar.element_create('CurrencyRates.Vertical.Scrollbar.trough', 'from', 'default')
		scrollbar.element_create('CurrencyRates.Vertical.Scrollbar.thumb', 'from', 'default')
		scrollbar.element_create('CurrencyRates.Vertical.Scrollbar.uparrow', 'from', 'default')
		scrollbar.element_create('CurrencyRates.Vertical.Scrollbar.downarrow', 'from', 'default')
		scrollbar.element_create('CurrencyRates.Vertical.Scrollbar.grip', 'from', 'default')
		scrollbar.layout('CurrencyRates.Vertical.TScrollbar',
    		[
        		('CurrencyRates.Vertical.Scrollbar.trough', {'children':
            		[('CurrencyRates.Vertical.Scrollbar.uparrow', {'side': 'top', 'sticky': ''}),
             		('CurrencyRates.Vertical.Scrollbar.downarrow', {'side': 'bottom', 'sticky': ''}),
             		('CurrencyRates.Vertical.Scrollbar.thumb', {'unit': '1', 'children':
                		 [('CurrencyRates.Vertical.Scrollbar.grip', {'sticky': ''})],
            		'sticky': 'nsew'})],
            		'sticky': 'ns'}),
    		])
		scrollbar.configure('CurrencyRates.Vertical.TScrollbar', background = '#000000', troughcolor = '#aba30a', bordercolor ='#000000', arrowcolor = '#aba30a')

  
		self.client_App['btn_Disconnect_SCR'] = tk.Button(master=self.client_App[name_Frame], text="DISCONNECT", bg='#792899', command=self.stop_Connect)
		self.client_App['btn_Log_Out'] = tk.Button(master=self.client_App[name_Frame], text="LOG OUT", bg='#792899', command=self.request_Logout, width=12)
		self.client_App['lbl_Greeting_Username'] = tk.Label(master=self.client_App[name_Frame], text="HELLO Duc Loi", font=("Algerian", 20), fg='#aba30a', bg="#000000")
		self.client_App['lbl_Year'] = tk.Label(master=self.client_App[name_Frame], text="Year", fg='#aba30a', bg="#000000")
		self.client_App['lbl_Month'] = tk.Label(master=self.client_App[name_Frame], text="Month", fg='#aba30a', bg="#000000")
		self.client_App['lbl_Day'] = tk.Label(master=self.client_App[name_Frame], text="Day", fg='#aba30a', bg="#000000")
		self.client_App['lbl_Base'] = tk.Label(master=self.client_App[name_Frame], text="Base", fg='#aba30a', bg="#000000")
		self.client_App['lbl_Currency'] = tk.Label(master=self.client_App[name_Frame], text="Currency", fg='#aba30a', bg="#000000")
  
		self.client_App['cb_Year_Value'] = tk.StringVar()
		self.client_App['cb_Year'] = ttk.Combobox(master=self.client_App[name_Frame], textvariable=self.client_App['cb_Year_Value'], state='readonly')
		self.client_App['cb_Year']['values'] = [i for i in range(1999, self.today.year + 1)]
		self.client_App['cb_Year']['values'] = list(reversed(self.client_App['cb_Year']['values']))
		self.client_App['cb_Month_Value'] = tk.StringVar()
		self.client_App['cb_Month'] = ttk.Combobox(master=self.client_App[name_Frame], textvariable=self.client_App['cb_Month_Value'], state='readonly')
		self.client_App['cb_Month']['values'] = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Month']		
		self.client_App['cb_Day_Value'] = tk.StringVar()
		self.client_App['cb_Day'] = ttk.Combobox(master=self.client_App[name_Frame], textvariable=self.client_App['cb_Day_Value'], state='readonly')
		self.client_App['cb_Day']['values'] = [i for i in range(1, 32)]
		self.client_App['cb_Day']['values'] += ('Day',)
		self.client_App['cb_Base_Value'] = tk.StringVar()
		self.client_App['cb_Base'] = ttk.Combobox(master=self.client_App[name_Frame], textvariable=self.client_App['cb_Base_Value'], state='readonly')
		self.client_App['cb_Currency_Value'] = tk.StringVar()
		self.client_App['cb_Currency'] = ttk.Combobox(master=self.client_App[name_Frame], textvariable=self.client_App['cb_Currency_Value'], state='readonly')
		self.client_App['btn_Search'] = tk.Button(master=self.client_App[name_Frame], text="Search", bg='#aba30a', fg="#000000", width=15, command=self.search_Currency_Rates)
		self.client_App['btn_Reset'] = tk.Button(master=self.client_App[name_Frame], text="Reset", bg='#aba30a', fg="#000000", width=15, command=self.request_Update_Data)
		self.client_App['txt_Rates_Table'] = tk.Text(master=self.client_App[name_Frame], width=149, height=20, relief=tk.SUNKEN, background="#000000", fg='#aba30a', highlightcolor='#aba30a', highlightbackground='#aba30a', highlightthickness=2, selectforeground='#000000', selectbackground="#aba30a")
		self.client_App['sb_Rates_Table'] = ttk.Scrollbar(master=self.client_App[name_Frame], orient=VERTICAL, style='CurrencyRates.Vertical.TScrollbar')
		self.client_App['txt_Rates_Table'].config(yscrollcommand=self.client_App['sb_Rates_Table'].set)
		self.client_App['sb_Rates_Table'].config(command=self.client_App['txt_Rates_Table'].yview)
		self.client_App['txt_Rates_Table'].insert(tk.END, "           DATETIME               ")
		self.client_App['txt_Rates_Table'].insert(tk.END, "               BASE               ")
		self.client_App['txt_Rates_Table'].insert(tk.END, "               CURRENCY               ")
		self.client_App['txt_Rates_Table'].insert(tk.END, "               RATE\n")
		self.client_App['lbl_Note'] = tk.Label(master=self.client_App[name_Frame], foreground='#792899', bg='#000000', font=("Algerian", 10), text="")
		self.client_App['btn_Disconnect_SCR'].grid(row=0, column=0, sticky="w", padx=(0, 13))	
		self.client_App['btn_Log_Out'].grid(row=0, column=6, sticky="e", padx=(13, 0))
		self.client_App['lbl_Greeting_Username'].grid(row=1, column=3, sticky="nsew", pady=30)
		self.client_App['lbl_Year'].grid(row=2, column=1, padx=(15, 35), sticky="w")
		self.client_App['lbl_Month'].grid(row=2, column=2, padx=35, sticky="w")
		self.client_App['lbl_Day'].grid(row=2, column=3, padx=35, sticky="w")
		self.client_App['lbl_Base'].grid(row=2, column=4, padx=35, sticky="w")
		self.client_App['lbl_Currency'].grid(row=2, column=5, padx=(35, 15), sticky="w")
  		
		self.client_App['cb_Year'].grid(row=3, column=1, padx=(15, 35))
		self.client_App['cb_Month'].grid(row=3, column=2, padx=35)
		self.client_App['cb_Day'].grid(row=3, column=3, padx=35)
		self.client_App['cb_Base'].grid(row=3, column=4, padx=35)
		self.client_App['cb_Currency'].grid(row=3, column=5, padx=(35, 15))
  
		self.client_App['btn_Search'].grid(row=4, column=2, pady=60, sticky="w", padx=35)
		self.client_App['btn_Reset'].grid(row=4, column=4, pady=60, sticky="w", padx=35)
		self.client_App['txt_Rates_Table'].place(x=0, y=270)
		self.client_App['sb_Rates_Table'].place(x=1180, y=272, height=324)
		self.client_App['lbl_Note'].place(x=0, y=610)


	def update_Rates_Table(self, data):
		new_data = list(reversed(data))
		self.client_App['txt_Rates_Table']['state'] = 'normal'

		
		self.client_App['txt_Rates_Table'].delete('2.0', tk.END)
		self.client_App['txt_Rates_Table'].insert(tk.END, '\n')
		for date in new_data:
			for currency in data[date]['rates']:
				self.client_App['txt_Rates_Table'].insert(tk.END, "         " + date) # 9
				self.client_App['txt_Rates_Table'].insert(tk.END, "                              " + data[date]['base']) # 30
				self.client_App['txt_Rates_Table'].insert(tk.END, "                                 " + currency)        # 33
				self.client_App['txt_Rates_Table'].insert(tk.END, "                                 " + str(data[date]['rates'][currency]) + "\n") # 33
		self.client_App['txt_Rates_Table']['state'] = 'disable'


	def search_Currency_Rates(self):
		data = {}
		year = self.client_App['cb_Year'].get()
		month = self.client_App['cb_Month'].get()
		if month != "Month": 
			month = datetime.strptime(month, "%B").month
		day = self.client_App['cb_Day'].get()
		base = self.client_App['cb_Base'].get()
		currency = self.client_App['cb_Currency'].get()

  
		if month != 'Month' and day != 'Day':
			if month < 10: month = '0' + str(month)
			if int(day) < 10: day = '0' + day
			Date = year + "-" + month + "-" + day
			try:
				Date = date.fromisoformat(Date)
				if int(year) < 2021: messagebox.showinfo(title="Notice", message="NOTE BELOW, DATA IS TAKEN FROM " + self.outdated_Date.isoformat())
				for DATE in self.received_Data:
					if Date.isoformat() == DATE:
						data[DATE] = {}
						data[DATE]['base'] = base
						factor = self.received_Data[DATE]['rates'][base]
						data[DATE]['rates'] = {}
						for cur in self.received_Data[DATE]['rates']:
							if cur == currency or currency == "Currency":
								data[DATE]['rates'][cur] = self.received_Data[DATE]['rates'][cur] / factor

				self.update_Rates_Table(data)

			except ValueError:
				messagebox.showwarning(title="Warning", message="INVALID DATE VALUE")
				return

		else:
			if int(year) < 2021: messagebox.showinfo(title="Notice", message="NOTE BELOW, DATA IS TAKEN FROM " + self.outdated_Date.isoformat())
			for DATE in self.received_Data:
				if date.fromisoformat(DATE).year == int(year):
					if month == 'Month' or date.fromisoformat(DATE).month == month:
						if day == 'Day' or date.fromisoformat(DATE).day == int(day):
							data[DATE] = {}
							data[DATE]['base'] = base
							factor = self.received_Data[DATE]['rates'][base]
							data[DATE]['rates'] = {}
							for cur in self.received_Data[DATE]['rates']:
								if cur == currency or currency == "Currency":
									data[DATE]['rates'][cur] = self.received_Data[DATE]['rates'][cur] / factor
			self.update_Rates_Table(data)


	def create_Socket(self):
		self.client_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.client_Socket.connect((self.server_Host, self.server_Port))
			self.show_Frame('frm_Login_And_Register')
			threading.Thread(target=self.check_Connect_Server, daemon=True).start()

			
		except WindowsError:
			self.show_Frame("frm_404")


	def request_Login(self, request="LOGIN"):
		try: 
			self.client_App['lbl_Notification']['text'] = ""
			username = self.client_App['ent_Username'].get()
			password = self.client_App['ent_Password'].get()
			if username == "" or password == "":
				self.client_App['lbl_Notification']['text'] = "The above fields cannot be empty!"
				return
			data = {'request': request, 'username': username, 'password': password}
			data = json.dumps(data)
			self.send_Prefix_Data(self.client_Socket, data)
			response = self.receive_Prefix_Data(self.client_Socket)
			if response == 'False': self.client_App['lbl_Notification']['text'] = "Username or password incorrect"
			else: 
				data = self.receive_Prefix_Data(self.client_Socket)
				data = json.loads(data)
				self.received_Data.update(data)
				self.outdated_Date = list(self.received_Data.keys())[0]
				self.outdated_Date = date.fromisoformat(self.outdated_Date)
				self.client_App['lbl_Note']['text'] = "*NOTE: Currency rates are taken since " + self.outdated_Date.isoformat()
				self.client_App['lbl_Greeting_Username']['text'] = "Hello " + username
				self.client_App['cb_Base']['values'] = [i for i in self.received_Data[self.today.isoformat()]['rates']]
				self.client_App['cb_Currency']['values'] = [i for i in self.received_Data[self.today.isoformat()]['rates']]
				self.client_App['cb_Currency']['values'] += ('Currency',)
				self.show_Frame('frm_Search_Currency_Rate')
				self.client_App['cb_Year'].set('2021')
				self.client_App['cb_Month'].set('Month')
				self.client_App['cb_Day'].set('Day')
				self.client_App['cb_Base'].set('EUR')
				self.client_App['cb_Currency'].set('Currency')
				self.update_Rates_Table(self.received_Data)

   
		except: 
			self.client_App['lbl_Notification']['text'] = "An error occurred while logging in. Please try again !!!"


	def request_Register(self, request="REGISTER"):
		try: 
			self.client_App['lbl_Notification']['text'] = ""
			username = self.client_App['ent_Username'].get()
			password = self.client_App['ent_Password'].get()
			if username == "" or password == "":
				self.client_App['lbl_Notification']['text'] = "The above fields cannot be empty!"
				return
			data = {'request': request, 'username': username, 'password': password}
			data = json.dumps(data)
			self.send_Prefix_Data(self.client_Socket, data)
			response = self.receive_Prefix_Data(self.client_Socket)
			if response == 'False': self.client_App['lbl_Notification']['text'] = "Account already exists"
			elif response == username: self.client_App['lbl_Notification']['text'] = "Username already exists"
			else: self.client_App['lbl_Notification']['text'] = "Account has been successfully registered"
   
		except: 
			self.client_App['lbl_Notification']['text'] = "An error occurred while registering. Please try again !!!"		


	def request_Update_Data(self):
		data = {'request': "UPDATE_DATA"}
		data = json.dumps(data)
		self.send_Prefix_Data(self.client_Socket, data)
		data = self.receive_Prefix_Data(self.client_Socket)
		data = json.loads(data)
		self.client_App['txt_Rates_Table']['state'] = 'normal'
		self.received_Data.update(data)
		self.client_App['cb_Year'].set('2021')
		self.client_App['cb_Month'].set('Month')
		self.client_App['cb_Day'].set('Day')
		self.client_App['cb_Base'].set('EUR')
		self.client_App['cb_Currency'].set('Currency')
		self.update_Rates_Table(self.received_Data)


	def request_Logout(self):
		data = {'request': "LOGOUT"}
		data = json.dumps(data)
		self.send_Prefix_Data(self.client_Socket, data)
		self.show_Frame('frm_Login_And_Register')


	def stop_Client(self):
		# Client con ket noi voi server
		data = {'request': "STOP_CONNECT"}
		data = json.dumps(data)
		try:
			self.send_Prefix_Data(self.client_Socket, data)
		except OSError:
			pass
		finally: self.client_Socket.close()


	def stop_Connect(self):
		data = {'request': "STOP_CONNECT"}
		data = json.dumps(data)
		self.send_Prefix_Data(self.client_Socket, data)
		self.client_Socket.close()
		self.client_App['ent_Username'].delete(0, tk.END)
		self.client_App['ent_Password'].delete(0, tk.END)
		self.show_Frame('frm_Connect')
		

	def send_Prefix_Data(self, conn, msg):
		msg = bytes(msg, self.message_Format)
		msg = struct.pack('>L', len(msg)) + msg
		conn.sendall(msg)


	def receive_Prefix_Data(self, conn):
		data = bytearray()
		while len(data) < 4:
			packet = conn.recv(4 - len(data))
			data.extend(packet)
		msglen = struct.unpack('>L', data)[0]
		del data[:]
		while len(data) < msglen:
			packet = conn.recv(msglen - len(data))
			data.extend(packet)
		return data.decode(self.message_Format)


	def check_Connect_Server(self):
		conn=self.client_Socket
		data = {'request': "CHECK_CONNECT"}
		data = json.dumps(data)

		print("Client connect to server with port: ", str(self.server_Port))
		try:
			while True:
				self.send_Prefix_Data(conn, data)
				time.sleep(0.001)
		except Exception as error:
			if str(error) == '[WinError 10054] An existing connection was forcibly closed by the remote host':
				messagebox.showerror(title="Error", message="DISCONNECT FROM SERVER", )
			else: pass
			
		finally:
			self.show_Frame('frm_Connect')
			self.client_App['ent_Username'].delete(0, tk.END)
			self.client_App['ent_Password'].delete(0, tk.END)
			print("Closing socket")
			conn.close()


	def run_Client(self):
		self.create_Socket()


	def run_App(self):
		self.client_App["window"] = tk.Tk()
		self.client_App["window"].resizable(width=False, height=False)
		self.client_App['window'].title("TCPClient")
		self.client_App['frm_Container'] = tk.Frame(self.client_App['window'])
		self.client_App['frm_Container'].pack(side="top", fill = 'both', expand = True)
		self.client_App['frm_Container'].grid_rowconfigure(0, weight=1)
		self.client_App['frm_Container'].grid_columnconfigure(0, weight=1)
  
		self.create_Frame_Connect_Server()
		self.create_Frame_404()
		self.create_Frame_Login_And_Register()
		self.create_Frame_Search_Currency_Rate()
		self.show_Frame("frm_Connect")


		self.client_App["window"].mainloop()
		if self.client_Socket:
			self.stop_Client()
		
  
	def run(self):
		self.run_App()


if __name__ == '__main__':
	Client = CLIENT()
	Client.run()
	print("End App")
	
