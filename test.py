def encrypt(text):
        encrypted_text = ""

        for char in text:
            encrypted_char = (ord(char) + 26)
            
            if encrypted_char > 126:
                encrypted_char -= 94

            encrypted_text += chr(encrypted_char)
        
        return encrypted_text
    

def decrypt(encrypted_text):
    decrypted_text = ""

    for char in encrypted_text:
        decrypted_char = (ord(char) - 26)
        
        if decrypted_char < 32:
            decrypted_char += 94

        decrypted_text += chr(decrypted_char)
    
    return decrypted_text


text = "Password : 13'a]d"
print(text)

encrypted_text = encrypt(text)
print("Encrypted Text:", encrypted_text)

decrypted_text = decrypt(encrypted_text)
print("Decrypted Text:", decrypted_text)