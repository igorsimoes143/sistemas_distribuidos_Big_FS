import socket
import os
import zipfile

def client(host='localhost', port=8082):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.connect(server_address)

    try:
        while True:
            print("\nMenu de operações:")
            print("1 - Listar arquivos do diretório atual")
            print("2 - Deletar arquivo")
            print("3 - copiar arquivo")
            print("4 - Baixar arquivo ou diretório")
            print("sair - Encerrar conexão")
            opcao = input("Digite o número da operação desejada: ").strip()
            sock.sendall(opcao.encode('utf-8'))

            if opcao.lower() == "sair":
                print("Encerrando conexão com o servidor.")
                break
            
            #Listar
            if opcao == "1":
                resposta = b""
                while True:
                    parte = sock.recv(2048)
                    if not parte:
                        break
                    resposta += parte
                    if len(parte) < 2048:
                        break

                print("\nResposta do servidor:\n", resposta.decode('utf-8'))

            #Deletar
            if opcao == "2":
                nome_arquivo = input("Digite o nome do arquivo a ser deletado: ").strip()
                sock.sendall(nome_arquivo.encode('utf-8'))
                resposta = b""
                while True:
                    parte = sock.recv(2048)
                    if not parte:
                        break
                    resposta += parte
                    if len(parte) < 2048:
                        break

                print("\nResposta do servidor:\n", resposta.decode('utf-8'))

            #copiar
            if opcao == "3":
                nome_origem = input("Digite o nome do arquivo de origem: ").strip()
                nome_destino = input("Digite o nome do arquivo de destino: ").strip()

                sock.sendall(f"{nome_origem}|||{nome_destino}".encode('utf-8'))

                resposta = b""
                while True:
                    parte = sock.recv(2048)
                    if not parte:
                        break
                    resposta += parte
                    if len(parte) < 2048:
                        break
                    
                print("\nResposta do servidor:\n", resposta.decode('utf-8'))
            
            #baixar
            if opcao == "4":
                nome = input("Digite o nome do arquivo ou diretório para baixar: ").strip()
                sock.sendall(nome.encode('utf-8'))
            
                # Recebe a resposta
                dados_recebidos = b""
                while True:
                    parte = sock.recv(2048)
                    if not parte:
                        break
                    dados_recebidos += parte
                    if len(parte) < 2048:
                        break
                

                if dados_recebidos.startswith(b"ERRO:"):#Dado recebido eh mensagem de erro
                        resposta_str = dados_recebidos.decode('utf-8')
                        print(f"Erro do servidor: {resposta_str[5:]}")  # Remove 'ERRO:'

                elif dados_recebidos.startswith(b"ARQUIVO:"):#dado recebido eh arquivo
                    conteudo = dados_recebidos[len(b"ARQUIVO:"):]
                    with open(f"{nome}", "wb") as f:
                        f.write(conteudo)
                    print(f"Arquivo '{nome}' salvo com sucesso.")

                elif dados_recebidos.startswith(b"DIRETORIO:"):#dado recebido eh diretorio
                    # Remover o prefixo 'DIRETORIO:'
                    dados_zip = dados_recebidos[10:]  # 'DIRETORIO:' tem 10 caracteres
                    with open(f"{nome}.zip", "wb") as f:
                        f.write(dados_zip)
                    # Descompactar o arquivo ZIP recebido
                    with zipfile.ZipFile(f"{nome}.zip", 'r') as zip_ref:
                        zip_ref.extractall(nome)  # Extrai para uma pasta com o nome do diretório
                    os.remove(f"{nome}.zip")  # Remove o arquivo ZIP após descompactar
                    print(f"Diretório '{nome}' foi baixado e descompactado.")
        
    finally:
        sock.close()

client()