import requests
import csv
import io
import json
import threading
import time

class Validador(threading.Thread):
    lock = threading.Lock()

    def __init__(self, clientes):
        threading.Thread.__init__(self)
        self.clientes = clientes

    def run(self):
        self.rodar()

    def rodar(self):
        for cliente in self.clientes:
            cpf, email = cliente
            cpf = cpf.zfill(11)
            print(f"{threading.current_thread().name} Pesquisando CPF `{cpf}` com email `{email}`")

            try:
                api_key = ''
                url = f'https://api.mails.so/v1/validate?email={email}'

                headers = {
                    'x-mails-api-key': api_key
                }

                response = requests.get(url, headers=headers)
                response.raise_for_status()
                clients = response.json()

                cli = [cpf] + list(clients['data'].values())
                with Validador.lock:
                    with open('output.csv', 'a', newline='\n', encoding='utf-8') as file:
                        writer = csv.writer(file, delimiter=';')
                        writer.writerow(cli)
            except Exception as e:
                print(f"Erro ao processar CPF `{cpf}`: {e}")


def parear_arquivos():
    rodados = []
    try:
        with open('output.csv', mode='r', encoding='utf-8') as file:
            data = file.read()
            data_io = io.StringIO(data)
            for linerodadoOK in csv.reader(data_io, delimiter=';'):
                cpf = str(linerodadoOK[0]).zfill(11)
                rodados.append(cpf)
    except FileNotFoundError:
        print("Criando arquivo de output")
        header = ['id', 'email', 'username', 'domain', 'did_you_mean', 'mx_record', 'provider', 'score', 'isv_format',
                  'isv_domain', 'isv_mx', 'isv_noblock', 'isv_nocatchall', 'isv_nogeneric', 'is_disposable', 'is_free',
                  'avatar', 'result', 'reason']
        with open('output.csv', 'a', newline='\n', encoding='utf-8') as file:
            writer = csv.writer(file,delimiter=';')
            writer.writerow(header)

    list_client = []
    with open('input.csv', mode='r', encoding='utf-8') as file:
        data = file.read()
        data_io = io.StringIO(data)
        next(data_io)  # Pulando cabeçalho
        print(f"Clientes Pesquisados {len(set(rodados))}")
        print(f"Arquivo de Input {len(list_client)}")
        print("Removendo Intersecções")

        for lineclient in csv.reader(data_io, delimiter=';'):
            cpf = str(lineclient[0]).zfill(11)
            email = str(lineclient[1])
            if cpf not in rodados:
                list_client.append((cpf, email))
    return list_client


while True:
    try:
        list_client = parear_arquivos()

        print(f"Clientes Pendentes: {len(list_client)}")

        n = 15
        print(f"Dividindo listas em {n}")
        splited = [list_client[i::n] for i in range(n)]
        for r in range(n):
            print(f"Lista {r} com {len(splited[r])} clientes")

        # Criando e iniciando as threads
        threads = []
        for r in range(n):
            thread = Validador(splited[r])
            threads.append(thread)
            thread.start()

        # Esperando todas as threads terminarem
        for thread in threads:
            thread.join()

        print("Processamento concluído.")
        break

    except Exception as e:
        print(f"Erro inesperado: {e}. Reiniciando...")
        time.sleep(5)
