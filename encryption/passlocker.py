from argon2 import PasswordHasher
import base64
import os
import stat
import platform
import argon2
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


class PasslockException(Exception):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg


class Passlocker:
    def __init__(self, master_password: str) -> None:
        try:
            salt, dkey_hash, ekey = self.load_key()
        except FileNotFoundError:
            self.new(master_password)
            salt, dkey_hash, ekey = self.load_key()

        dkey = self.derive_password(salt, master_password)
        if not self.verify(dkey_hash.decode(), dkey):
            raise PasslockException("Authentication Failed! - wrong password")

        self.derived_key: bytes = dkey
        self.encryption_key: bytes = ekey

    def check_os(self):
        return platform.system()

    def verify(self, dkey_hash, dkey):
        ph = PasswordHasher()
        try:
            return ph.verify(dkey_hash, dkey)
        except argon2.exceptions.VerifyMismatchError:
            return False

    def new(self, master_password: str):
        # deriving key from password
        salt: bytes = os.urandom(16)
        dkey: bytes = self.derive_password(salt, master_password)
        ph = PasswordHasher()
        dkey_hash = ph.hash(dkey).encode()

        # encrypting decryption key with derived key
        rkey: bytes = Fernet.generate_key()
        # key used for en/decrypting data
        ekey: bytes = Fernet(dkey).encrypt(rkey)

        # saving new keys to file
        self.write_key(salt, dkey_hash, ekey)

    def derive_password(self, salt: bytes, password: str) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA3_512(),
            length=32,
            salt=salt,
            iterations=4800000
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def encrypt(self, plaintext: str) -> bytes:
        encryptor = Fernet(
            Fernet(self.derived_key).decrypt(self.encryption_key))
        return encryptor.encrypt(plaintext.encode())

    def decrypt(self, cypher: bytes) -> str:
        encryptor = Fernet(
            Fernet(self.derived_key).decrypt(self.encryption_key))
        return encryptor.decrypt(cypher).decode()

    def encrypt_file(self, data: bytes) -> bytes:
        encryptor = Fernet(
            Fernet(self.derived_key).decrypt(self.encryption_key))
        encrypted_data = encryptor.encrypt(data)
        return encrypted_data

    def decrypt_file(self, data: bytes) -> bytes:
        encryptor = Fernet(
            Fernet(self.derived_key).decrypt(self.encryption_key))
        decrypted_data = encryptor.decrypt(data)
        return decrypted_data

    def write_key(self, salt: bytes, dkey_hash: bytes, ekey: bytes):
        encode_ekey = base64.urlsafe_b64encode(salt + dkey_hash + ekey)
        keyfile = None
        if self.check_os() == "Linux":
            if not (Path.home() / ".passlock").exists():
                (Path.home() / ".passlock").mkdir(mode=0o700)
                keyfile = str((Path.home() / ".passlock/passlock.key"))

        elif self.check_os() == "Windows":
            documents = Path.home() / "Documents"
            hidden_folder = documents / "passlock"
            if not hidden_folder.exists():
                hidden_folder.mkdir()
                os.system(f'attrib +h "{hidden_folder}"')
                keyfile = str(hidden_folder / "passlock.key")

        if keyfile is None:
            raise PasslockException(
                "Keyfile could not be written - OS not supported")

        with open(keyfile, 'wb') as key:
            key.write(encode_ekey)
        os.chmod(keyfile, stat.S_IRUSR | stat.S_IWUSR)

    def load_key(self) -> tuple[bytes, bytes, bytes]:
        keyfile = str(Path.home() / ".passlock/passlock.key")
        with open(keyfile, 'rb') as key:
            encode_ekey = key.read()
        decode_ekey = base64.urlsafe_b64decode(encode_ekey)
        return decode_ekey[:16], decode_ekey[16:113], decode_ekey[113:]
