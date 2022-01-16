from datetime import datetime
from bs4 import BeautifulSoup
import csv
import requests
import time
import smtplib


data = datetime.today().strftime('%d-%m-%y')
tags = ["last_12_35", "last_17_35", "last_3_35", "last_2_35", "last_4_35", "last_15_35", "last_1_35"]
moedas = ['dolar', 'euro', 'libra', 'iene', 'suico', 'canadense', 'autraliano']


def obter_html():
    user_agent = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) Chrome/86.0.4240.198 Safari/537.36'}
    url = 'https://br.investing.com/currencies/exchange-rates-table'
    print(f'fazendo contato com --> {url}')
    time.sleep(0.2)
    response = requests.get(url, headers=user_agent)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def extraindo_valores(soup):
    cambio = {}
    list_cambio = [data]
    for tag, moeda in zip(tags, moedas):
        cambio[moeda] = soup.find('td', id=tag).get_text().strip()
        list_cambio.append(soup.find('td', id=tag).get_text().strip())
    return cambio, list_cambio


def imprime(cambio):
    print(f'data --> {data}')
    print('COTAÇÕES'.center(30, '-'))
    for k, v in cambio.items():
        print(k.ljust(20, '.') + str(v).rjust(10))


def save_csv(list_cambio):
    with open('cambio.csv', 'a') as cambio_file:
        csv_file = csv.writer(cambio_file)
        csv_file.writerow(list_cambio)


def enviar_email(mensagem):
    smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
    if smtp_obj.ehlo()[0] != 250:
        raise Exception('Conexão com o servido de email falhou')

    if smtp_obj.starttls()[0] != 220:
        raise Exception('não foi possivel habilitar a criptografia')

    if smtp_obj.login('email@origem.com', 'senha')[0] != 235:
        raise Exception('o login não foi bem sucedito')

    smtp_obj.sendmail('email@origem.com', 'email@destino.com', mensagem)
    smtp_obj.quit()


objeto_soup = obter_html()
dicio, lista = extraindo_valores(objeto_soup)

while True:
    print('')
    print('Cotações de moedas'.center(30, '-'))
    print('1 - ver cotações\n2 - salvar cotações em aquivo csv\n3 - enviar cotações para e-mail\n4 - sair')
    r = input('digite o codigo numerico: ')
    if r == '1':
        imprime(dicio)
    elif r == '2':
        print('salvando cotações no arquivo csv')
        time.sleep(0.2)
        save_csv(lista)
    elif r == '3':
        with open('cambio.csv', 'r') as obj_csv:
            csv_reader = csv.reader(obj_csv)
            csv_data = list(csv_reader)

        lista_cotacao = [' '.join(csv_data[0]), ' '.join(csv_data[1])]
        mensagem = '\n'.join(lista_cotacao)
        enviar_email(mensagem)

    elif r == '4':
        break
