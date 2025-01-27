from pyjop import *

SimEnv.connect() and SimEnvManager.first().reset(stop_code=False)

text = MessageSniffer.first().get_cipher_text()

ord_F = ord('F')
first_letter = text[0]
shift = ord_F - ord(first_letter)

enc_password = text[67:72]
password = ""

for char in enc_password:
    shifted = chr(ord(char) + shift)
    password += shifted

DataExchange.first().set_data("passcode", int(password))
