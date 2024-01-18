from utils import *

# 自定义映射表，这里使用简单的替换方式进行加密
characters = 'abcdefgIJKLMNOPhijklmnopqrs123tuvwxyzABCDEFG.HQRSTUVWXYZ0456789' 

def encrypt(char):
    index = (characters.find(char) + 5) % len(characters)
    return characters[index]

def decrypt(char):
    index = (characters.find(char) - 5) % len(characters) 
    return characters[index]

def encrypt_string(input_string):
    encrypted_string = ""
    for char in input_string:
        # 如果字符在映射表中，将其替换为映射表中的对应字符，否则保留原字符
        encrypted_string += encrypt(char)

    return encrypted_string

def decrypt_string(encrypted_string):
    decrypted_string = ""
    for char in encrypted_string:
        # 如果字符在反向映射表中，将其替换为反向映射表中的对应字符，否则保留原字符
        decrypted_string += decrypt(char)

    return decrypted_string

# # 待加密的字符串
# original_string = "www.google.com"

# # 加密字符串
# encrypted = encrypt_string(original_string)
# print("加密后的字符串:", encrypted)

# # 解密字符串
# decrypted = decrypt_string(encrypted)
# print("解密后的字符串:", decrypted)


if __name__ == "__main__":
    m = 5 # 你要映射的范围
    for url in url_to_ip:
        encrypt_url = encrypt(url)
        result = string_to_int_hash(encrypt_url, m)
        print('url:', url, end=' ')
        print("Mapped Integer:", result)
