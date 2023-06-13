import string
import secrets
import os
import random


class PasswordGenerator():
    @classmethod
    def gen_password(cls, length):
        chars = string.ascii_letters + string.digits + string.punctuation
        stage_1 = "".join(chars[c % len(chars)] for c in os.urandom(length))
        while True:
            password = ''.join(secrets.choice(
                f'{stage_1}' + chars) for _ in range(length)).replace(" ", "")
            if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                    and sum(c.isdigit() for c in password) >= 3):
                break

        return password


class PassphraseGenerator():
    @classmethod
    def gen_passphrase(cls, num_words: int, complexity: bool = False) -> str:
        rng = random.Random()
        words = [cls.generate_random_word(rng, complexity)
                 for _ in range(num_words)]
        return " ".join(words)

    @classmethod
    def generate_random_word(cls, rng, complexity):
        word_length = rng.randint(4, 6)
        vowels = ['a', 'e', 'i', 'o', 'u']
        consonants = [
            'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
            'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w',
            'x', 'y', 'z'
        ]

        word = ''.join(
            secrets.choice(vowels) if rng.random() < 0.5 else secrets.choice(
                consonants) for _ in range(word_length))

        if complexity:
            return cls.add_complexity(rng, word)
        else:
            return word

    @classmethod
    def add_complexity(cls, rng, word):
        modified_word = ''

        for c in word:
            if rng.random() < 0.3:
                modified_word += c.upper()
            else:
                modified_word += c

        if rng.random() < 0.3:
            special_chars = string.punctuation
            random_char = secrets.choice(special_chars)
            random_index = secrets.randbelow(len(modified_word))
            modified_word = modified_word[:random_index] + \
                random_char + modified_word[random_index:]
        elif rng.random() < 0.3:
            random_digit = str(secrets.randbelow(9))
            random_index = secrets.randbelow(len(modified_word))
            modified_word = modified_word[:random_index] + \
                random_digit + modified_word[random_index:]

        return modified_word


class TokenGenerator():
    @classmethod
    def gen_token(cls, length) -> str:
        return secrets.token_hex(length)


class SecretkeyGenerator():
    @classmethod
    def gen_secret_key(cls, length) -> str:
        return secrets.token_urlsafe(length)
