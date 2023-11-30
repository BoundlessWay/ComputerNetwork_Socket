import socket
import threading
import time
import tkinter as tk
from tkinter import ttk
import json
from urllib.request import urlopen
from datetime import date
import os
import struct


HOST = '192.168.56.1'
# HOST = '127.0.0.1'
PORT = 5566
DATE = "2021-01-01"


class SERVER:
	def __init__(self):
		self.all_Connections = []
		self.server_Host =HOST
		self.server_Port = PORT
		self.message_Format = "utf8"
		self.server_Socket = 0
		self.server_App = {}
		self.current_Path = os.path.abspath(os.getcwd())
		self.database_Path = os.path.join(self.current_Path, "Database")
		self.accounts_Json = os.path.join(self.database_Path, 'accounts.json')
		self.base_API_URL = 'http://api.exchangeratesapi.io/v1/'
		self.access_API_Key = "access_key=MRgmpBZny5rtHro3rtXtIg5moSE2Kpoq"
		# Ngày bắt đầu lấy dữ liệu từ API
		# Vì nếu lấy full data từ API thì quá nhiều (từ 1999) nên đặt 1 limit có thể thay đổi
		self.outdated_Date = date.fromisoformat(DATE)
		self.today = date.today()
		if not os.path.exists(self.database_Path):
			os.makedirs(self.database_Path)
		if not os.path.exists(self.accounts_Json):
			with open(self.accounts_Json, 'w') as file:
				pass


	def auto_Input_IP_And_Port(self):
		if self.server_App['chb_Value'].get() == 1:
			self.server_App['ent_IP_Address'].delete(0, tk.END)
			self.server_App['ent_Port'].delete(0, tk.END)
			self.server_App['ent_IP_Address'].insert(0, self.server_Host)
			self.server_App['ent_Port'].insert(0, str(self.server_Port))
		else:
			self.server_App['ent_IP_Address'].delete(0, tk.END)
			self.server_App['ent_Port'].delete(0, tk.END)
  
  
	def connect_Server(self):
		if (self.server_App["ent_IP_Address"].get() == self.server_Host and self.server_App["ent_Port"].get() == str(self.server_Port)):
			self.server_App["ent_IP_Address"].config(state="disable")
			self.server_App["ent_Port"].config(state="disable")
			self.server_App['chb_Automatic']['state'] = 'disable'
			self.show_Notification("Connecting...\nConnect server successful\nRunning on server...\nServer has been already\n")
			self.server_App["btn_Connect"]["state"]="disabled"
			self.server_App["btn_Connect"]["bg"] = self.server_App["btn_Stop"].cget("background")
			self.server_App["btn_Stop"]["state"] = "normal"
			self.server_App["btn_Stop"]["bg"] = "red"
			threading.Thread(target=self.run_Server, daemon=True).start()
		else:
			self.show_Notification("Ip Address and Port are wrong\nConnect unsuccessful\n")


	def create_Socket(self):
		try:
			self.server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server_Socket.bind((self.server_Host, self.server_Port))
			self.server_Socket.listen(10)
			self.show_Notification("Server is waiting for connections...\n")
			self.accept_Connections()
		except socket.error as msg:
			self.show_Notification("Socket creation error: " + str(msg) + "\nRetrying...\n")
			self.create_Socket()


	def accept_Connections(self):
		while True:
			try:
				conn, address = self.server_Socket.accept()
				self.server_Socket.setblocking(1)
				self.all_Connections.append(conn)
				nofi = "Connected to " + conn.getpeername()[0] + "." + str(conn.getpeername()[1]) + "\n"
				self.show_Notification(nofi)
				self.server_App['status_Archives'][conn] = []
				self.server_App['status_Archives'][conn].append("Client: IP(" + conn.getpeername()[0] + "), Port(" + str(conn.getpeername()[1]) + ")\n")
				self.update_Status()
				threading.Thread(target=self.response_Client, args=(conn,), daemon=True).start()

			except OSError as error:
				return


	def show_Notification(self, msg):
		self.server_App["txt_Notification_Box"].config(state="normal")
		self.server_App["txt_Notification_Box"].insert(tk.END, msg)
		self.server_App["txt_Notification_Box"].config(state="disable")
 
 
	def clear_Notification(self):
		self.server_App["txt_Notification_Box"].config(state="normal")
		self.server_App["txt_Notification_Box"].delete("1.0", tk.END)
		self.server_App["txt_Notification_Box"].config(state="disable")
 
 
	def update_Status(self):
		self.server_App["txt_Status_Box"].config(state="normal")
		self.server_App["txt_Status_Box"].delete("1.0", tk.END)
		for conn in self.all_Connections:
			for s in self.server_App['status_Archives'][conn]:
				self.server_App["txt_Status_Box"].insert(tk.END, s)
		self.server_App["txt_Status_Box"].config(state="disable")
 

	def broadcast(self, msg):
		for conn in self.all_Connections:
			
			conn.sendall(bytes(msg, self.message_Format))


	def stop_Connect(self):
		for conn in self.all_Connections:
			del self.server_App['status_Archives'][conn]
			conn.close()

		del self.all_Connections[:]
		self.server_App["ent_IP_Address"].config(state="normal")
		self.server_App["ent_Port"].config(state="normal")	
		self.server_App['chb_Automatic']['state'] = 'normal'
		self.server_App["btn_Stop"]["state"] = "disable"
		self.server_App["btn_Stop"]["bg"] = self.server_App["btn_Connect"].cget("background")
		self.server_App["btn_Connect"]["state"]="normal"
		self.server_App["btn_Connect"]["bg"] = "green"
		self.show_Notification("Disconnect to server !!!\n")
		self.update_Status()
		self.server_Socket.close()


	def accept_Registration(self, username, password):
		with open(self.accounts_Json, 'r') as file:
			data = file.read()
			if not data:
				data = {}
				data[username] = password
			else:
				data = json.loads(data)
				if username in data:
					if data[username] == password: return False
					return username
				data[username] = password
		with open(self.accounts_Json, 'w') as file:
			json.dump(data, file)
		return True


	def accept_Login(self, username, password):
		with open(self.accounts_Json, 'r') as file:
			data = file.read()
			if not data: return False
			data = json.loads(data)
			if username in data and data[username] == password: return True
			else: return False


	def get_Data_By_Date(self, date):
		file_Name = os.path.join(self.database_Path, date + '.json')
		
		try:
			with open(file_Name, 'r') as file:
				data = json.load(file)
				return data
		except FileNotFoundError: return {}
		

	def get_Data_By_Currency(self, currency):
		start_Day = self.outdated_Date.toordinal()
		end_Day = self.today.toordinal()
		result = {}

		for day in range(start_Day, end_Day + 1):
			day = date.fromordinal(day)
			file_Name = os.path.join(self.database_Path, day.isoformat() + '.json')
   
			try:
				with open(file_Name, 'r') as file:
					data = json.load(file)
					data = json.loads(data)
					result[day.isoformat()] = data['rates'][currency]
			except FileNotFoundError: continue
		return result


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


	def send_Prefix_Data(self, conn, msg):
		msg = bytes(msg, self.message_Format)
		msg = struct.pack('>L', len(msg)) + msg
		conn.sendall(msg)


	def send_Currency_Rate(self, conn, just_Latest):
		all_Currency_Rate = {}
		if not just_Latest:
			start_Day = self.outdated_Date.toordinal()
			end_Day = self.today.toordinal()

			for day in range(start_Day, end_Day + 1):
				day = date.fromordinal(day)
				file_Name = os.path.join(self.database_Path, day.isoformat() + '.json')
	
				if not os.path.isfile(file_Name):
					request = ''.join((self.base_API_URL, day.isoformat(), '?', self.access_API_Key))
					data = urlopen(request).read().decode()
				
					with open(file_Name, 'w') as file:
						json.dump(data, file)

				with open(file_Name, 'r') as file:
					data = file.read()
					data = json.loads(data)
					all_Currency_Rate[day.isoformat()] = {}
					all_Currency_Rate[day.isoformat()]['base'] = data['base']
					all_Currency_Rate[day.isoformat()]['rates'] = data['rates']
					
		else:
			latest_Date = self.today
			file_Name = os.path.join(self.database_Path, latest_Date.isoformat() + '.json')
			with open(file_Name, 'r') as file:
				data = file.read()
				data = json.loads(data)
				all_Currency_Rate[latest_Date.isoformat()] = {}
				all_Currency_Rate[latest_Date.isoformat()]['base'] = data['base']
				all_Currency_Rate[latest_Date.isoformat()]['rates'] = data['rates']		
		print(type(all_Currency_Rate))	
		all_Currency_Rate = json.dumps(all_Currency_Rate)
		self.send_Prefix_Data(conn, all_Currency_Rate)


	def response_Client(self, conn):
		# Check for the first time login
		login_First_Time = False
 
		while True:
			try:
				data = self.receive_Prefix_Data(conn)
				data = json.loads(data)
				if data['request'] != "CHECK_CONNECT": print(data)

				if data['request'] == "STOP_CONNECT":

					del self.server_App['status_Archives'][conn]
					self.all_Connections.remove(conn)
					self.update_Status()
					addr = conn.getpeername()[0] + "." + str(conn.getpeername()[1])

					self.show_Notification("Disconnect to " + addr + "\n")
					conn.close()

				elif data['request'] == "REGISTER":
					username = data['username']
					password = data['password']
		
					response = str(self.accept_Registration(username, password))
					self.send_Prefix_Data(conn, response)
					if response == "True":
						msg = conn.getpeername()[0] + "." + str(conn.getpeername()[1]) + " registered account successfully - Username: " + username + " - Password: " + password + "\n"
						self.show_Notification(msg)
				
				elif data['request'] == "LOGIN":
					username = data['username']
					password = data['password']
		
					response = str(self.accept_Login(username, password))
					self.send_Prefix_Data(conn, response)
					if response == "True":
						msg = conn.getpeername()[0] + "." + str(conn.getpeername()[1]) + " has logged in - Username: " + username + "\n"
						self.show_Notification(msg)
						self.server_App['status_Archives'][conn].append("        Username: " + username + "\n")
						self.update_Status()
						self.send_Currency_Rate(conn, login_First_Time)
						login_First_Time = True

				elif data['request'] == "UPDATE_DATA":
					self.send_Currency_Rate(conn, True)
		
				elif data['request'] == "LOGOUT":
					username = self.server_App['status_Archives'][conn][1][18:]
					del self.server_App['status_Archives'][conn][1]
					msg = conn.getpeername()[0] + "." + str(conn.getpeername()[1]) + " has logged out of " + username
					self.show_Notification(msg)
					self.update_Status()
     
				else: pass
			except:
				return
			
		
	def run_App(self):
		self.server_App["window"] = tk.Tk()
		self.server_App["window"].title("TCPServer")
		self.server_App["window"].resizable(width=False, height=False)

		self.server_App["frm_Control"] = tk.Frame(relief=tk.SUNKEN, borderwidth=3, master=self.server_App["window"])
		self.server_App["frm_Control"].grid(row=0, column=0, ipady=20, sticky="nsew")


		self.server_App["lbl_Control"] = tk.Label(master=self.server_App["frm_Control"], text="CONTROL")
		self.server_App["lbl_Control"].grid(row = 0, column=2, sticky="nsew", pady=20)

		self.server_App["lbl_IP_Address"] = tk.Label(master=self.server_App["frm_Control"], text="IP Address")
		self.server_App["ent_IP_Address"] = tk.Entry(master=self.server_App["frm_Control"], width=20, border=3)
		self.server_App['chb_Value'] = tk.IntVar()
		self.server_App['chb_Automatic'] = tk.Checkbutton(master=self.server_App["frm_Control"], text="Automatic", command=self.auto_Input_IP_And_Port, variable=self.server_App['chb_Value'])
		self.server_App["lbl_IP_Address"].grid(row=1, column=0, sticky="w", padx=20)
		self.server_App["ent_IP_Address"].grid(row=2, column=0, padx=20)
		self.server_App['chb_Automatic'].grid(row=3, column=0, sticky='w', padx=15, pady=(10, 0))	

		self.server_App["lbl_Port"] = tk.Label(master=self.server_App["frm_Control"], text="Port")
		self.server_App["ent_Port"] = tk.Entry(master=self.server_App["frm_Control"], width=20, border=3)
		self.server_App["lbl_Port"].grid(row=1, column=1, sticky="w", padx=20)
		self.server_App["ent_Port"].grid(row=2, column=1, padx=20)

		self.server_App["btn_Connect"] = tk.Button(master=self.server_App["frm_Control"], width=10, text="Connect", bg="green", fg="white", command=self.connect_Server)
		self.server_App["btn_Connect"].grid(row=2, column=2, padx=30, sticky="e")
		self.server_App["btn_Stop"] = tk.Button(master=self.server_App["frm_Control"], width=10, text="Stop", state="disabled", fg="white", command=self.stop_Connect)
		self.server_App["btn_Stop"].grid(row=2, column=3, padx=30, sticky="e")
		self.server_App["btn_Clear"] = tk.Button(master=self.server_App["frm_Control"], width=10, text="Clear", command=self.clear_Notification, fg="black", bg="cyan")
		self.server_App["btn_Clear"].grid(row=2, column=4, padx=30, sticky="e")

		self.server_App["frm_Dialog_Box"] = tk.Frame(master=self.server_App["window"])
		self.server_App["frm_Dialog_Box"].grid(row=1, column=0, sticky="nsew")

		self.server_App["lbl_Notification"] = tk.Label(master=self.server_App["frm_Dialog_Box"], text="Notification", borderwidth=3, relief=tk.SUNKEN)
		self.server_App["lbl_Notification"].grid(row=0, column=0, sticky="nsew")
		self.server_App["txt_Notification_Box"] = tk.Text(master=self.server_App["frm_Dialog_Box"], width=60, borderwidth=3, relief=tk.SUNKEN, bg="white", state='disable')
		self.server_App["txt_Notification_Box"].grid(row=1, column=0, sticky="nsew")

		self.server_App["lbl_Status"] = tk.Label(master=self.server_App["frm_Dialog_Box"], text="Status", borderwidth=3, relief=tk.SUNKEN)
		self.server_App["lbl_Status"].grid(row=0, column=1, sticky="nsew")
		self.server_App['status_Archives'] = {}
		self.server_App["txt_Status_Box"] = tk.Text(master=self.server_App["frm_Dialog_Box"], width=40, borderwidth=3, relief=tk.SUNKEN, bg="white")
		self.server_App["txt_Status_Box"].grid(row=1, column=1, sticky="nsew")
		self.server_App["txt_Status_Box"].config(state="disable")


		# Start the application
		self.server_App["window"].mainloop()


	def run_Server(self):
		self.create_Socket()


	def update_Database(self):
		start_Day = self.outdated_Date.toordinal()
		end_Day = self.today.toordinal()
  
		for day in range(start_Day, end_Day + 1):
			day = date.fromordinal(day)
			file_Name = os.path.join(self.database_Path, day.isoformat() + '.json')

			if not os.path.isfile(file_Name):
				request = ''.join((self.base_API_URL, day.isoformat(), '?', self.access_API_Key))
				data = urlopen(request).read().decode()
				
				with open(file_Name, 'w') as file:
					data = json.loads(data)
					json.dump(data, file)

		while True:
			day = date.fromordinal(end_Day)
			request = ''.join((self.base_API_URL, day.isoformat(), '?', self.access_API_Key))
			data = urlopen(request).read().decode()
   
			with open(file_Name, 'w') as file:
				data = json.loads(data)
				json.dump(data, file)
			time.sleep(1800)


	def run(self):
		self.run_App()



if __name__ == '__main__':
	Server = SERVER()
	print(Server.current_Path)
	
 
