import requests, os
from prettytable import PrettyTable
from colorama import Fore, Back, Style
from time import sleep

def clear():
	_ = os.system('cls' if os.name =='nt' else 'clear')	#'nt' for windows and 'posix' for linux

print(Back.BLUE + Fore.WHITE + "CRYPTOCURRENCY DYNAMIC STATS" + Style.RESET_ALL)
print("By default it will show " + Back.BLACK + Fore.RED + "TOP 10 every 5s" + Style.RESET_ALL)
print()
st = input("From which rank do you wanna see the table? : ")
lim = input("How many do wanna see? (Maximum 100 possible): ")
t = input("How frequently do you wanna refresh? : ")
if lim == "":
	lim = "10"
if st == "":
	st = "0"
else:
	st = str(int(st) - 1)
if t == "":
	t = 5
else:
	t = int(t)

def crytab():
	url = "https://api.coinlore.net/api/tickers/?start=" + st + "&limit=" + lim
	request = requests.get(url)
	data = request.json()["data"]
	#print(data[0])
	
	table = PrettyTable(["RANK", "SYMBOL", "NAME", "PRICE($)", "PRICE(btc)", "1h(%)", "24h(%)", "7d(%)", "MARKET CAP", "VOLUME24"])
	
	for j in data:
		
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
					   j["symbol"],
					   j["name"],
					   round(float(j["price_usd"]), 2),
					   pbtc,
					   h1, h24, d7,
					   j["market_cap_usd"],
					   round(float(j["volume24"]), 3)])
	
	clear()
	print(Back.BLUE + Fore.WHITE + "CRYPTOCURRENCY DYNAMIC STATS" + Style.RESET_ALL)
	print("Press " + Back.WHITE + Fore.BLACK + "CTRL + C" + Style.RESET_ALL + " to " + Back.BLACK + Fore.RED + "STOP" + Style.RESET_ALL)
	print(Back.YELLOW + Fore.WHITE + "START" + Style.RESET_ALL + " = " + st)
	print(Back.YELLOW + Fore.WHITE + "LIMIT" + Style.RESET_ALL + " = " + lim)
	print()
	print(table)
	print()
	for i in range(t, 0, -1):
		print(i)
		sleep(1)
	print(Back.WHITE + Fore.BLACK + "REFRESH" + Style.RESET_ALL)
	crytab()

crytab()
print(Back.WHITE + Fore.BLACK + "END" + Style.RESET_ALL)