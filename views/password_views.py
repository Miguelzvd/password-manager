import base64
import string
import secrets
import hashlib
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken


class FernetHasher:

    RANDOM_STRING_CHARS = string.ascii_lowercase + string.ascii_uppercase
    BASE_DIR = Path(__file__).resolve().parent.parent
    KEY_DIR = BASE_DIR / "keys"

    def __init__(self, key):
        if not isinstance(key, bytes):
            key = key.encode()

        self.fernet = Fernet(key)

    @classmethod
    def _get_random_string(cls, length=25):
        string = ""
        for i in range(length):
            string = string + secrets.choice(cls.RANDOM_STRING_CHARS)
        return string

    @classmethod
    def create_key(cls, archive=False):
        value = (
            cls._get_random_string()
        )  # utiliza o metodo criado anteriormente para gerar uma string aleatoria de 25 caracteres
        hasher = hashlib.sha256(
            value.encode("utf-8")
        ).digest()  # utiliza a lib de hash para criar um hash da string gerada e depois converte o hash do valor dessa string para o tipo string novamente
        key = base64.b64encode(hasher)  # salva o valor da chave em base64
        if archive:
            return key, cls.archive_key(key)
        return key, None

    @classmethod
    def archive_key(cls, key):
        file = "key.key"
        while Path(
            cls.KEY_DIR / file
        ).exists():  # faz uma verificação para saber se o primeiro arquivo foi criado
            file = f"key_{cls._get_random_string(length=5)}.key"

        with open(
            cls.KEY_DIR / file, "wb"
        ) as arq:  # pega o path do KEY_DIR e diz que vai ser gerado um arquivo chamado "keys.txt". O wb significa que vai fazer uma escrita em binario
            arq.write(key)

        return cls.KEY_DIR / file

    def encrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()
        return self.fernet.encrypt(value)

    def decrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()
        try: 
            return self.fernet.decrypt(value).decode()
        except InvalidToken as e:
            return 'Token inválido'


fernet_caio = FernetHasher('+3RAv/RrEa/M7qYOR6tHjel4kJl18Kc4M3lFmuyssDk=')
print(fernet_caio.decrypt('gAAAAABnJCpxRP6CpdoYEW1THqP9rCgpl2f3PulmTn6HMUHO1CViJG3ZBaZuhXC6WJX9qDhk_gEaWzEH98sJP_AabEcqJJhMJQ=='))
