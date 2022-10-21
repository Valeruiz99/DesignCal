def claveEncriptada(cadena):
    if cadena != "":
        #hash password pbkdf2_hmac+sha256
        import hashlib
        #pasar a secretos.... ****************************
        salt = '999adsiSenaCFDCM2022x'
        input_string = cadena
        salted_input_string = input_string+salt
        password_hash =hashlib.sha256(salted_input_string.encode('utf-8')).hexdigest()
        return password_hash
    else:
        return ""