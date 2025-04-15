import socket
import os
import shutil

def server(host='localhost', port=8082):
    data_payload = 2048
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)

    print(f"Servidor iniciado em {host}:{port}")

    while True:
        print("Aguardando conexão do cliente...")
        client, address = sock.accept()
        print(f"Conexão com {address} estabelecida.")

        try:
            while True:
                data = client.recv(data_payload)
                if not data:
                    print("Cliente desconectado.")
                    break  # Cliente fechou conexão

                operacao = data.decode('utf-8').strip()
                print(f"Operação recebida: {operacao}")

                if operacao == "1":
                    
                    caminho_absoluto = os.path.dirname(os.path.abspath(__file__))
                    nome_pasta = "raiz"
                    caminho_diretorio = os.path.join(caminho_absoluto, nome_pasta)
                    arquivos = os.listdir(caminho_diretorio)
                    resposta = "Arquivos no diretório atual:\n" + "\n".join(arquivos)

                    client.send(resposta.encode('utf-8'))

                elif operacao.lower() == "sair":
                    resposta = "Conexão encerrada pelo cliente."
                    client.send(resposta.encode('utf-8'))
                    break

                elif operacao == "2":
                    nome_caminho_b = b""
                    while True:
                        parte = client.recv(data_payload)
                        if not parte:
                            break
                        nome_caminho_b += parte
                        if len(parte) < data_payload:
                            break
                    nome_caminho = nome_caminho_b.decode('utf-8')
                    caminho_absoluto = os.path.dirname(os.path.abspath(__file__))
                    nome_pasta = "raiz"
                    caminho_diretorio = os.path.join(caminho_absoluto, nome_pasta)
                    caminho_final = os.path.join(caminho_diretorio, nome_caminho)

                    try:
                        if not os.path.exists(caminho_final):
                            raise FileNotFoundError(f"O caminho '{nome_caminho}' não foi encontrado.")
                        if os.path.isdir(caminho_final):
                            try:
                                for item in os.listdir(caminho_final):
                                    item_path = os.path.join(caminho_final, item)
                                    if os.path.isfile(item_path):
                                        os.remove(item_path)
                                    elif os.path.isdir(item_path):
                                        shutil.rmtree(item_path)
                                resposta = f"Todos os arquivos e pastas dentro de '{nome_caminho}' foram deletados com sucesso."
                            except Exception as e:
                                resposta = f"Erro ao limpar o diretório '{nome_caminho}': {str(e)}"

                        if os.path.isfile(caminho_final):
                            try:
                                os.remove(caminho_final)
                                resposta = f"Arquivo '{nome_caminho}' deletado com sucesso."
                            except FileNotFoundError:
                                resposta = f"Arquivo '{nome_caminho}' não encontrado."
                            except Exception as e:
                                resposta = f"Erro ao deletar arquivo: {str(e)}"

                    except FileNotFoundError:
                        resposta = f"Arquivo '{nome_caminho}' não encontrado."
                    except Exception as e:
                        resposta = f"Erro ao deletar arquivo: {str(e)}"
                    finally:
                        client.send(resposta.encode('utf-8'))

                elif operacao == "3":
                    dados_b = b""
                    while True:
                        parte = client.recv(data_payload)
                        if not parte:
                            break
                        dados_b += parte
                        if len(parte) < data_payload:
                            break

                    dados = dados_b.decode('utf-8').strip()
                    nome_origem, nome_destino = dados.split("|||")

                    try:
                        caminho_absoluto = os.path.dirname(os.path.abspath(__file__))
                        nome_pasta = "raiz"
                        caminho_diretorio = os.path.join(caminho_absoluto, nome_pasta)
                        caminho_origem = os.path.join(caminho_diretorio, nome_origem)
                        caminho_destino = os.path.join(caminho_diretorio, nome_destino)

                        shutil.copy(caminho_origem, caminho_destino)
                        resposta = f"Arquivo '{nome_origem}' copiado com sucesso para '{nome_destino}'."
                    except FileNotFoundError:
                        resposta = f"Arquivo de origem '{nome_origem}' não encontrado."
                    except Exception as e:
                        resposta = f"Erro ao copiar arquivo: {str(e)}"
                    finally:
                        client.send(resposta.encode('utf-8'))

                elif operacao == "4":
                    nome_caminho_b = b""
                    while True:
                        parte = client.recv(data_payload)
                        if not parte:
                            break
                        nome_caminho_b += parte
                        if len(parte) < data_payload:
                            break
                        
                    nome_caminho = nome_caminho_b.decode('utf-8').strip()

                    caminho_absoluto = os.path.dirname(os.path.abspath(__file__))
                    caminho_diretorio = os.path.join(caminho_absoluto, "raiz")
                    caminho_final = os.path.join(caminho_diretorio, nome_caminho)
                    print("ola sou o baixar")
                    try:
                        if not os.path.exists(caminho_final):
                            raise FileNotFoundError(f"O caminho '{nome_caminho}' não foi encontrado.")
                        
                        # Se for diretório, compacta antes de enviar
                        if os.path.isdir(caminho_final):
                            print("ola sou o dir")
                            temp = b"DIRETORIO:"
                            zip_path = shutil.make_archive(caminho_final, 'zip', caminho_final)
                            with open(zip_path, "rb") as f:
                                temp += f.read()
                                client.sendall(temp)
                            os.remove(zip_path)  # Limpa após envio

                        elif os.path.isfile(caminho_final):
                            print("ola sou o file")
                            data = b"ARQUIVO:"
                            with open(caminho_final, "rb") as f:
                                data += f.read()
                                client.sendall(data)
                    except FileNotFoundError:
                        print("ola sou o filenotfounderror")
                        resposta = f"ERRO: Arquivo '{nome_caminho}' não encontrado."
                        client.send(resposta.encode('utf-8'))
                    except Exception as e:
                        client.send(f"ERRO: Erro ao processar GET: {str(e)}".encode('utf-8'))

                else:
                    resposta = "Código de operação não reconhecido."
                    client.send(resposta.encode('utf-8'))


        finally:
            client.close()
            print("Conexão finalizada.\n")

server()