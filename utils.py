import hashlib

url_to_ip = {
    "www.google.com": "172.217.3.100",   # Google 20
    "www.baidu.com": "220.181.38.148",   # Baidu 24 
    "www.yahoo.com": "98.137.11.163",    # Yahoo 16
    "www.microsoft.com": "40.76.4.15",   # Microsoft 26
    "www.twitter.com": "104.244.42.65",  # Twitter 30 
    "www.instagram.com": "52.200.238.83", # Instagram 10
}

def string_to_int_hash(input_string, m):
    sha1_hash = hashlib.sha1(input_string.encode()).hexdigest()  # 计算字符串的 SHA-1 哈希值
    sha1_int = 2 * int(sha1_hash, 16)  # 将哈希值转换为整数
    mapped_int = sha1_int % (2 ** m)  # 将整数映射到指定范围
    return mapped_int


if __name__ == "__main__":
    m = 5
    for url in url_to_ip:
        result = string_to_int_hash(url, m)
        print('url:', url, end=' ')
        print("Mapped Integer:", result)
