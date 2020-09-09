import requests, os
from prettytable import PrettyTable
from colorama import Fore, Back, Style
from time import sleep
from tqdm import tqdm

try:
	def clear():
		_ = os.system('cls' if os.name =='nt' else 'clear')	#'nt' for windows and 'posix' for linux

	print(Back.BLUE + Fore.WHITE + "CRYPTOCURRENCY DYNAMIC STATS" + Style.RESET_ALL)
	print("By default it will show " + Back.BLACK + Fore.RED + "TOP 10 every 5s" + Style.RESET_ALL)
	print()

	def tabchar():
		st = input("From which rank do you wanna see the table? : ")
		lim = input("How many do wanna see? (Maximum 100 possible): ")
		t = input("How frequently do you wanna refresh? : ")
		if not lim.isdecimal():
			lim = "10"
		if not st.isdecimal():
			st = "0"
		else:
			st = str(int(st) - 1)
		if not t.isdecimal():
			t = 5
		else:
			t = int(t)
		ranktab(st, lim, t)
	def tabcre(table, j):
		h1 = j["percent_change_1h"]
		if float(h1) > 0:
			h1 = Back.GREEN + Fore.WHITE + h1 + Style.RESET_ALL
		else:
			h1 = Back.RED + h1 + Style.RESET_ALL
		h24 = j["percent_change_24h"]
		if float(h24) > 0:
			h24 = Back.GREEN + Fore.WHITE + h24 + Style.RESET_ALL
		else:
			h24 = Back.RED + h24 + Style.RESET_ALL
		d7 = j["percent_change_7d"]
		if float(d7) > 0:
			d7 = Back.GREEN + Fore.WHITE + d7 + Style.RESET_ALL
		else:
			d7 = Back.RED + d7 + Style.RESET_ALL
		pbtc = round(float(j["price_btc"]) * 10000, 2)

		table.add_row([j["rank"],
						j["id"],
						j["symbol"],
						j["name"],
						round(float(j["price_usd"]), 2),
						pbtc,
						h1, h24, d7,
						j["market_cap_usd"],
						round(float(j["volume24"]), 3)])

	def ranktab(st, lim, t):
		url = "https://api.coinlore.net/api/tickers/?start=" + st + "&limit=" + lim
		request = requests.get(url)
		data = request.json()["data"]
		#print(data[0])
		
		table = PrettyTable([Fore.CYAN + "RANK", "ID", "SYMBOL", "NAME", "PRICE($)", "PRICE(btc)", "1h(%)", "24h(%)", "7d(%)", "MARKET CAP", "VOLUME24" + Style.RESET_ALL])
		
		for j in data:
			tabcre(table, j)

		clear()
		print(Back.BLUE + Fore.WHITE + "CRYPTOCURRENCY DYNAMIC STATS RANKED" + Style.RESET_ALL)
		print("Press " + Back.WHITE + Fore.BLACK + "CTRL + C" + Style.RESET_ALL + " to " + Back.BLACK + Fore.RED + "STOP" + Style.RESET_ALL)
		print(Back.YELLOW + Fore.WHITE + "START" + Style.RESET_ALL + " = " + str(int(st) + 1))
		print(Back.YELLOW + Fore.WHITE + "LIMIT" + Style.RESET_ALL + " = " + lim)
		printab(table, t)
		ranktab(st, lim, t)

	def printab(table, t):
		print()
		print(table)
		print()
		i = float(t)
		'''
		while i > 0:
			print(str(round(i, 1)), end="\r", flush=True)
			sleep(0.1)
			i -= 0.1
		'''
		for j in tqdm(range(100), desc=Fore.MAGENTA + "REFRESH BAR", ncols=66):
			sleep(i / 100)
		print(Back.WHITE + Fore.BLACK + "REFRESH" + Style.RESET_ALL)

	def cuschar():
		url = "https://api.coinlore.net/api/tickers/?start=0&limit=100"
		request = requests.get(url)
		data = request.json()["data"]
		l = sorted([[i["name"], i["symbol"], i["id"]] for i in data])

		for i in l:
			print(*i[::-1])
		
		print("\nEnter all the id nos then press " + Back.WHITE + Fore.BLACK + "ENTER" + Style.RESET_ALL + " to construct the custom table")
		cl = []
		i = 1
		prom = "Enter id 1: "
		a = input(prom)
		while a != "":
			try:
				cl += [int(a)]
				i += 1
			except:
				print(Back.BLACK + Fore.RED + "Enter valid id" + Style.RESET_ALL)
			prom = "Enter id " + str(i) + ": "
			a = input(prom)

		t = input("How frequently do you wanna refresh? : ")
		if t == "":
			t = 5
		else:
			t = int(t)
		custab(cl, t)

	def custab(cl, t):
		table = PrettyTable([Fore.CYAN + "RANK", "ID", "SYMBOL", "NAME", "PRICE($)", "PRICE(btc)", "1h(%)", "24h(%)", "7d(%)", "MARKET CAP", "VOLUME24" + Style.RESET_ALL])
		for i in cl:
			url = "https://api.coinlore.net/api/ticker/?id=" + str(i)
			request = requests.get(url)
			data = request.json()
			#print(dat)

			if data:
				tabcre(table, data[0])
			else:
				table.add_row(["-x-", i, "-x-", "-x-", "-x-", "-x-", "-x-", "-x-", "-x-", "-x-", "-x-"])
		
		clear()
		print(Back.BLUE + Fore.WHITE + "CRYPTOCURRENCY DYNAMIC STATS CUSTOM" + Style.RESET_ALL)
		print("Press " + Back.WHITE + Fore.BLACK + "CTRL + C" + Style.RESET_ALL + " to " + Back.BLACK + Fore.RED + "STOP" + Style.RESET_ALL)
		print(Back.YELLOW + Fore.WHITE + "COUNT" + Style.RESET_ALL + " = " + str(len(cl)))
		printab(table, t)
		custab(cl, t)

	c = input("Press " + Back.WHITE + Fore.BLACK + "ENTER" + Style.RESET_ALL + " for ranked table or any character for custom rows (only from " + Back.BLACK + Fore.RED + "TOP 100" + Style.RESET_ALL + "): ")

	if c == "":
		tabchar()
	else:
		cuschar()
	
except:
	print()
	print(Back.WHITE + Fore.BLACK + "END" + Style.RESET_ALL)