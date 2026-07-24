from pwdlib import PasswordHash

class Hash():
    @staticmethod
    def hash_pass(password):
        password_hash = PasswordHash.recommended()
        hashed_pass = password_hash.hash(password)
        return hashed_pass