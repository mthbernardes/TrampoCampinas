#!/usr/bin/python
# coding=utf-8

from lxml import html
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib, requests, sqlite3, getpass, time, os, smtplib, sys

def banner():
	print '''
████████╗██████╗  █████╗ ███╗   ███╗██████╗  ██████╗
╚══██╔══╝██╔══██╗██╔══██╗████╗ ████║██╔══██╗██╔═══██╗
   ██║   ██████╔╝███████║██╔████╔██║██████╔╝██║   ██║
   ██║   ██╔══██╗██╔══██║██║╚██╔╝██║██╔═══╝ ██║   ██║
   ██║   ██║  ██║██║  ██║██║ ╚═╝ ██║██║     ╚██████╔╝
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝      ╚═════╝

 ██████╗ █████╗ ███╗   ███╗██████╗ ██╗███╗   ██╗ █████╗ ███████╗
██╔════╝██╔══██╗████╗ ████║██╔══██╗██║████╗  ██║██╔══██╗██╔════╝
██║     ███████║██╔████╔██║██████╔╝██║██╔██╗ ██║███████║███████╗
██║     ██╔══██║██║╚██╔╝██║██╔═══╝ ██║██║╚██╗██║██╔══██║╚════██║
╚██████╗██║  ██║██║ ╚═╝ ██║██║     ██║██║ ╚████║██║  ██║███████║
 ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
'''
	print

def menu():
    os.system('clear')
    banner()
    print "[+] - Bem-vindo ao TRAMPO CAMPINAS - [+]"
    print "[+] - O primeiro aplicativo desenvolvida para ajudar você na procura de um novo emprego - [+]"
    print "[+] - Desenvolvido por G4mBl3r - [+]"
    print "[+] - Envie seu Curriculo de forma automatica, OTIMIZE seu TEMPO - [+]"
    print "[+] - Duvidas/Sugestões envie um e-mal para gambler@tutanota.com  - [+]"
    print
    print "-" * 130
    print
    print "[1] - Procurar empregos"
    print "[2] - Configurações iniciais"
    print
    print "[0] - Sair"
    print
    menu_opcao()

def menu_opcao():
    opcao = raw_input( "[+] - Selecione uma opção[0-2]: ")
    if opcao == '1':
        procura_emprego()
    elif opcao == '2':
        cria_db()
    elif opcao == '0':
        sys.exit()
    else:
        menu()

def connecta_banco():
	try:
		banco = sqlite3.connect("fj.db")
		cursor = banco.cursor()
		print
		return banco, cursor
	except:
		print "[!] - Nao foi possivel conectar ao banco de dados - [!]"
		exit()

def cria_db():
	try:
		banco,cursor = connecta_banco()
		print "[+] - Criando tabela de Login - [+]"
		cursor.execute("CREATE TABLE login (conta text, senha text, anexo text)")
		print "[+] - Tabela de Login criada - [+]"
	except:
		print "[!] - Nao foi possivel criar a tabela login - [!]"
		pass

	try:
		print
		print "[+] - Criando tabela de registro - [+]"
		cursor.execute("CREATE TABLE registro (url text, data text)")
		print "[+] - Tabela de registro criada - [+]"
	except:
		print "[!] - Nao foi possivel criar a tabela registro - [!]"
		pass
	configuracao(banco,cursor)

def configuracao(banco,cursor):
	conta = raw_input("[+] - Insira sua conta de e-mail do gmail: ")
	senha = getpass.getpass("[+] - Insira sua senha do e-mail digitado anteriormente: ")
	anexo = raw_input("[+] - Insira o arquivo com o anexo que deseja enviar: ")

	try:
		cursor.execute("INSERT INTO login VALUES (?,?,?);", (conta,senha,anexo))
		banco.commit()
		print "[+] - Cadastro registrado com sucesso - [+]"
	except:
		print "[!] - Nao foi possivel realizar o cadastro - [!]"
	raw_input("Pressione ENTER para continuar")
	menu()

def consulta_infos():
	banco,cursor = connecta_banco()
	sql = "SELECT * FROM login"
	cursor.execute(sql)
	for row in cursor.fetchall():
		conta, senha, anexo = row
	return conta,senha,anexo

def verifica_envio(link):
	banco, cursor = connecta_banco()
	cursor.execute("SELECT * FROM registro")
	for row in cursor.fetchall():
		url, data = row
		if link in url:
			print "[+] - Foi enviado um curriculo para essa vaga no dia, "+data
			print
		else:
			pass

def procura_emprego():
	busca = raw_input("[+] - Digite o nome da vaga ou uma palavra-chave: ").replace(' ','+').lower()
	url = "http://empregacampinas.com.br/page/1/?s="+busca
	#prox_pagina = 0
	while True:
		try:
			r = requests.get(url, timeout=2)
			tree = html.fromstring(r.content)
			vagas = tree.xpath('//*[@id="article"]/div/div/div/div/a/h2/text()')
			link = tree.xpath('//*[@id="article"]/div/div/div/div/a[@title]/@href')
			if len(vagas) > 1:
				qtd_vagas = len(vagas) - 1
			else:
				qtd_vagas = len(vagas)

			pagina = url.split('/')[4]
			info_vaga(qtd_vagas,pagina,vagas,link)
			#PEGA NOVA URL
			url = tree.xpath('//*[@class="nextpostslink"]/@href')[0]
		except:
			menu()

def info_vaga(qtd_vagas,pagina,vagas,link):
	for i in range(0,qtd_vagas):
		os.system('clear')
		#Pagina
		print "[+] - Pagina :"+pagina
		print "-"*130
		print
		#Vaga
		print vagas[i].strip()
		print

		#Entra link da vaga
		acesso_vaga = requests.get(link[i].strip())
		tree_2 = html.fromstring(acesso_vaga.content)

		#Descricao
		print "[+] - Descrição: "
		desc = tree_2.xpath('//*[@id="article"]/div/div[2]/div/p[1]/text()')
		print ''.join(desc).encode('utf-8')
		print

		#Responsabilidades
		print "[+] - Responsabilidades: "
		resp = tree_2.xpath('//*[@id="article"]/div/div[2]/div/p[3]/text()')
		print ''.join(resp).encode('utf-8')
		print

		#Salario
		print "[+] - Salario: "
		salario = tree_2.xpath('//*[@id="article"]/div/div[2]/div/p[5]/text()')
		print ''.join(salario).encode('utf-8')
		print

		#Observacao
		print "[+] - Observação: "
		obs = tree_2.xpath('//*[@id="article"]/div/div[2]/div/p[7]/text()')
		print ''.join(obs).encode('utf-8')
		print

		#E-mail
		print "[+] - E-mail: "
		email = tree_2.xpath('//a[starts-with(@href, "mailto")]/text()')
		print email[0]
		print

		verifica_envio(link[i])

		#Vagas
		print "Vaga",i+1,"de",qtd_vagas
		print
		print "-"*130

		#Enviar ou Nao
		if info_vaga_opcao() is True:
			envia_email(email[0],link[i])

def info_vaga_opcao():
	opcao = raw_input('[+] - Enviar curriculo([s]/n/0)?').lower()
	if len(opcao) > 1 or len(opcao) < 1:
		return False
	elif opcao == 's':
		return True
	elif opcao == 'n':
		return False
	elif opcao == '0':
		menu()
	else:
		return False

def envia_email(email_empresa,link):
	banco, cursor = connecta_banco()
	conta, senha, file_anexo = consulta_infos()
	data = time.strftime("%d/%m/%Y")
	cursor.execute("INSERT INTO registro(url,data) VALUES (?,?)", (link,data))
	banco.commit()
	file = open('email.txt')
	conteudo = file.read()
	print "[+] - Preparando e-mail e anexo para envio - [+]"
	mail = MIMEMultipart()
	mail["Subject"] = "Vaga Emprega Campinas"
	mail["From"] = conta
	mail["Reply-to"] = conta
	mail["To"] = email_empresa

	print "[+] - Inserindo Mensagem ao corpo do E-mail - [+]"
	texto = MIMEText(conteudo)
	mail.attach(texto)
	anexo = MIMEApplication(open(file_anexo,"rb").read())
	anexo.add_header('Content-Disposition', 'attachment', filename=file_anexo)
	mail.attach(anexo)
	try:
		gm = smtplib.SMTP("smtp.gmail.com", 587)
		gm.ehlo()
		gm.starttls()
		gm.ehlo()
		gm.login(conta, senha)
		gm.sendmail(mail['From'], mail['To'], mail.as_string())
		gm.close()
		print "[+] - E-mail enviado com Sucesso - [+]"
		print "[+] - Boa sorte estamos torcendo por você - [+]"
	except:
		print "[!] - Não foi possivel enviar o email - [!]"
		pass
	raw_input("Pressione ENTER para continuar")

def checagem():
	if os.path.exists('fj.db') is True:
		main()
	else:
		cria_db()
		main()

def main():
	menu()

checagem()
