import os
import io, csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import threading
from collections import OrderedDict
import socket

class TrataLista():
    def __init__(self, base_folder, base_archive):
        self.base_folder = base_folder
        self.base_archive = base_archive

    def parealista(self):
        a_rodar = []
        rodados = []
        try:
            with io.open(self.base_folder+'Retornos/'+str(socket.gethostname())+'_Retorno.csv', 'r', encoding="utf-8") as resultgeral:
                lines = resultgeral.read()
                io_string = io.StringIO(lines)
                for ln in csv.reader(io_string, delimiter=',', quotechar='|'):
                    rodados.append(ln[1])
        except:
            pass

        with io.open(self.base_folder+self.base_archive, 'r', encoding="utf-8") as base:
            lines = base.read()
            io_string = io.StringIO(lines)
            # next(io_string)
            for ln in csv.reader(io_string, delimiter=';', quotechar='|'):
                if ln[1] in rodados:
                    pass
                else:
                    lista = [word.strip() for word in ln if word.strip() != '']
                    final_list = list(OrderedDict.fromkeys(lista))
                    a_rodar.append(final_list)

        print("Arquivo Base: {} - Saldo: {} - Rodados {} ".format(self.base_archive, len(a_rodar), len(rodados)))

        return a_rodar

class RodaWhats(threading.Thread):
    def __init__(self, base_folder, lista, profile):
        threading.Thread.__init__(self)
        self.base_folder = base_folder
        self.base_archive = base_archive
        self.lista = lista
        self.profile = profile

    def run(self):
        self.credito(self.lista, self.profile)

    def credito(self, clientes, usuario):
        lock = threading.Lock()
        self.chrome_options = Options()
        self.chrome_options.add_argument('--disable-infobars')  # para desbolquear o acesso
        self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        #self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument('log-level=3')
        self.chrome_options.add_argument(f"--user-data-dir=C:/Temp/perfil1")
        # self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # para ignorar warnings
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.clientes = clientes


        for cliente in clientes:
            tamanho = len(cliente)-3
            returned = [cliente[0], cliente[1], cliente[2]]
            for i in range(tamanho):
                i = i + 3
                print('Pesquisando {} - {}'.format(cliente, cliente[i]))
                self.driver.get("https://web.whatsapp.com/send?phone=55{}".format(cliente[i]))
                x_arg_err = "//*[@class='x12lqup9 x1o1kx08']"
                x_arg_ok = "//*[@class='x1c4vz4f x2lah0s xdl72j9 x1i4ejaq x1y332i5']"

                if len(cliente[i]) < 11:
                    returned.append(cliente[i])
                    returned.append("Numero Fixo")
                    print(returned)
                    continue

                while True:
                    try:
                        self.driver.find_element(By.CLASS_NAME, '_aigw ')
                        print("Executando pilha")
                        time.sleep(2)
                        break
                    except:
                        print("Aguardando index")
                        time.sleep(2)

                while True:
                    try:
                        time.sleep(3)
                        self.driver.find_element(By.XPATH,x_arg_ok)
                        returned.append(cliente[i])
                        returned.append("Numero OK")
                        break
                    except:
                        time.sleep(3)
                        try:
                            self.driver.find_element(By.XPATH,x_arg_err)
                            returned.append(cliente[i])
                            returned.append("Numero Invalido")
                            break
                        except:
                            pass

            print(returned)
            lock.acquire()
            with open(self.base_folder+'Retornos/'+str(socket.gethostname())+'_Retorno.csv', 'a', encoding='utf8', newline='\n') as geral:
                writer = csv.writer(geral)
                writer.writerow(returned)
                returned.clear()
            lock.release()
        self.driver.close()

base_folder = 'Retornos/.csv'
base_archive = 'input.csv.csv'

wpcred = TrataLista(base_folder, base_archive).parealista()
n = 1
splited = [wpcred[i::n] for i in range(n)]

for i in range(n):
    profile = 'Profile {}'.format(i)
    thread = RodaWhats(base_folder, splited[i], profile)
    thread.start()
