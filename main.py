import requests
import threading
import time
import json
from colorama import Fore, Back, Style

def read_wallet(filename):
    with open(filename, "r") as file:
        crypto_data = json.load(file)
    return crypto_data

def update_invest(crypto, amount,value,operation):
    try:
        with open("invest.json", "r") as file:
            config_data = json.load(file)
    except FileNotFoundError:
        config_data = {}
    try:
        with open("wallet.json", "r") as file2:
            config_data2 = json.load(file2)
    except FileNotFoundError:
        config_data2 = {}

    if crypto in config_data and config_data2:
        saldo=int(config_data[crypto])
        last_uds=float(config_data2[crypto])
        if operation=="buy":
            new_amount = amount + saldo
            uds=float(amount)/float(value)
            last_uds=last_uds+uds
            print(Fore.GREEN+f"Compraste {amount} eur de {crypto} a {value}")
            
        elif operation=="sell":
            if amount>saldo:
                all_in=input(Fore.RED+f"No hay fondos suficientes, su saldo de {crypto} es de {saldo}.\nSi desea vender todo escriba y, de lo contrario escriba lo que sea: ")
                if all_in=="y":
                    new_amount=0  
                    last_uds=0
                    print(Fore.YELLOW+f"Vendiste {saldo} eur de {crypto} a {value}")
                else:
                    new_amount=saldo
                    print(Fore.YELLOW+f"No vendiste {crypto}")
            else:
                new_amount= saldo - amount
                uds=float(amount)/float(value)
                last_uds=last_uds-uds
                print(Fore.YELLOW+f"Vendiste {amount} eur de {crypto} a {value}")
    else:
        new_amount = amount
        uds=float(amount)/float(value)
        last_uds= uds

    config_data[crypto] = int(new_amount)
    config_data2[crypto] = float(last_uds)

    with open("invest.json", "w") as file:
        json.dump(config_data, file, indent=4)
    with open("wallet.json", "w") as file2:
        json.dump(config_data2, file2, indent=4)

def checkPrice(crypto,currency):
    # URL de la API para obtener el precio de Bitcoin
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies={currency}"
    try:
        response = requests.get(url)
        data = response.json()
        # Obtener el precio de Bitcoin en USD
        value = data[f'{crypto}'][f'{currency}']
    except Exception as e:
        print(Fore.RED+f"Error al obtener el precio de {crypto}:", e)
    return value

def commands(command):
    parts = command.split()
    if len(parts) >= 2 and parts[0] == "b":
        try:
            amount=int(parts[1])
            value=checkPrice(crypto,currency)
            update_invest(crypto,amount,value,"buy")

        except Exception as e:
            print(Fore.RED+"No has introducido un numero valido",e)
    elif len(parts) >= 2 and parts[0] == "s":
        try:
            amount=int(parts[1])
            value=checkPrice(crypto,currency)
            update_invest(crypto,amount,value,"sell")
            
        except Exception as e:
            print(Fore.RED+"No has introducido un numero valido",e)
    else:
        print(Fore.RED+"Comando no valido")

def console_input_thread():
    while True:
        command = input(Fore.BLUE+"")
        commands(command)

def option1(crypto,currency):
    # Iniciar el hilo para recibir comandos desde la consola
    input_thread = threading.Thread(target=console_input_thread)
    input_thread.start()

    while True:
        value=checkPrice(crypto,currency)
        print(Fore.WHITE+f"El precio actual de {crypto} es {value} {currency}")
        time.sleep(10)

def option2():
    currency="eur"
    try:
        with open("invest.json", "r") as file:
            config_data = json.load(file)
    except FileNotFoundError:
        config_data = {}
    try:
        with open("wallet.json", "r") as file2:
            config_data2 = json.load(file2)
    except FileNotFoundError:
        config_data2 = {}
    for crypto in config_data:
        dinero_invertido=int(config_data[crypto])
        unidades_crypto=float(config_data2[crypto])
        valor_crypto=checkPrice(crypto,currency)
        valor_patrimonio=valor_crypto*unidades_crypto
        profit=float(valor_patrimonio)-float(dinero_invertido)
        print(Fore.WHITE+f"- Compraste {unidades_crypto} {crypto.capitalize()} por {dinero_invertido} eur.\nValor aproximado actual de: {valor_patrimonio}")
        if profit>0:
            print(Fore.GREEN+f"Profit: {str(profit)} eur")
        else:
            print(Fore.RED+f"Profit: {str(profit)} eur")

    
def option3():
    url = "https://api.coingecko.com/api/v3/coins/list?include_platform=false"
    try:
        response = requests.get(url)
        data = json.loads(response.text)

        ids_only = [item["id"] for item in data]

        with open("ids.json", "w") as file:
            json.dump(ids_only, file, indent=4)
        print(Fore.GREEN + "Coins refreshed successfully!")
    except Exception as e:
        print(Fore.RED + f"An error ocurred while getting IDs: {e}")

while True:
    print(Fore.WHITE+   "    __________  _____   ____  ______    ____  __ __ ____________   ____  ____  ______ \n"+
                        "   / ____/ __ \/  _/ | / /  |/  /   |  / __ \/ //_// ____/_  __/  / __ )/ __ \/_  __/ \n"+
                        "  / /   / / / // //  |/ / /|_/ / /| | / /_/ / ,<  / __/   / /    / __  / / / / / /    \n"+
                        " / /___/ /_/ // // /|  / /  / / ___ |/ _, _/ /| |/ /___  / /    / /_/ / /_/ / / /     \n"+
                        " \____/\____/___/_/ |_/_/  /_/_/  |_/_/ |_/_/ |_/_____/ /_/    /_____/\____/ /_/  by Mochaaless    \n"+
                        "                                                                                       ")

    print(Fore.WHITE+"Seleccione una opción:")
    print(Fore.WHITE+"1. Check Market")
    print(Fore.WHITE+"2. Check Wallet")
    print(Fore.WHITE+"3. Refrescar coins")
    print(Fore.WHITE+"4. Salir")

    opcion = input(Fore.WHITE+">>> ")
    if(opcion=="1"):
        crypto = input(Fore.WHITE+"Que crypto desea: ")
        print("\n")
        currency="eur"
        option1(crypto,currency)
    elif(opcion=="2"):
        print("\n")
        option2()
    elif(opcion=="3"):
        print("\n")
        option3()
    elif(opcion=="4"):
        exit()    
    else:
        print("\n")
        print(Fore.RED+"Seleccion no disponible")
    pass
