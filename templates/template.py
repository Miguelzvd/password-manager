import sys
import os

sys.path.append(os.path.abspath(os.curdir))

from model.password import Password
from views.password_views import FernetHasher

action = input("Digite 1 para salvar uma nova senha ou 2 para ver uma senha salva: ")

if action == "1":
    if len(Password.get()) == 0:
        key, path = FernetHasher.create_key(archive=True)
        print("Sua chave foi criada com sucesso, salve-a com cuidado!")
        print(f'Chave: {key.decode("utf-8")}')
        if path:
            print(
                "Chave salva no arquivo, lembre-se de remover o arquivo após transferir de local"
            )
            print(f"Caminho: {path}")
    else:
        key = input(
            "Digite sua chave usada para criptografia, use sempre  mesma chave: "
        )

    domain = input("Dominio: ")
    password = input("Password: ")
    fernet_user = FernetHasher(key)
    pass1 = Password(
        domain=domain, password=fernet_user.encrypt(password).decode("utf-8")
    )
    pass1.save()

elif action == "2":
    domain = input("Dominio: ")
    key = input("Key: ")
    fernet_user = FernetHasher(key)
    data_results = Password.get()

    for data in data_results:
        if domain in data["domain"]:
            password = fernet_user.decrypt(data["password"])
    if password:
        print(f"Sua senha é: {password}, para o domínio: {domain}")
    else:
        print(f"Nenhuma senha encontrada para o dominio procurado: {password}")
