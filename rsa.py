import random
from des import encryption_dynamic, decryption_dynamic

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_prime_in_range(start, end):
    prime = random.randint(start, end)
    i = 0
    while not is_prime(prime):
        i += 1
        print(f"trial {i} generate prime number")
        prime = random.randint(start, end)
    return prime

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    _, x, _ = extended_gcd(e, phi)
    return x % phi

def generate_keypair():
    # Menggunakan ukuran kunci yang lebih besar untuk keamanan
    # p = generate_prime_in_range(9223372036854775700, 9223372036854775807)
    # q = generate_prime_in_range(9223372036854775700, 9223372036854775807)
    # while p == q:
    #     q = generate_prime_in_range(100, 200)
    p = 9223372036854775783
    q = 9223372036854775761

    n = p * q
    phi = (p - 1) * (q - 1)

    # Menggunakan e = 65537 (bilangan prima Fermat ke-4) sebagai standar
    e = 65537
    while gcd(e, phi) != 1:
        print("get gcd between e and phi")
        e = random.randrange(3, phi, 2)

    print("get mod inverse")
    d = mod_inverse(e, phi)
    return ((e, n), (d, n))

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, byteorder='big')

def bytes_to_int(x: bytes) -> int:
    return int.from_bytes(x, byteorder='big')

def rsa_encrypt_des_key(des_key: str, public_key):
    """
    Mengenkripsi kunci DES menggunakan RSA
    :param des_key: str - kunci DES dalam bentuk string
    :param public_key: tuple (e, n) - kunci publik RSA
    :return: int - kunci DES terenkripsi
    """
    e, n = public_key
    des_key_int = int.from_bytes(des_key.encode(), byteorder='big')
    if des_key_int >= n:
        raise ValueError("Kunci DES terlalu besar untuk RSA key size yang diberikan")
    return pow(des_key_int, e, n)

def rsa_decrypt_des_key(encrypted_des_key: int, private_key, key_length=64):
    """
    Mendekripsi kunci DES yang terenkripsi
    :param encrypted_des_key: int - kunci DES terenkripsi
    :param private_key: tuple (d, n) - kunci private RSA
    :param key_length: int - panjang kunci dalam bits
    :return: str - kunci DES yang sudah didekripsi
    """
    d, n = private_key
    des_key_int = pow(encrypted_des_key, d, n)
    des_key_bytes = int_to_bytes(des_key_int)
    return des_key_bytes.decode()

def hybrid_encrypt(message: str, des_key: str, rsa_public_key):
    """
    Mengenkripsi pesan menggunakan DES dan mengenkripsi kunci DES menggunakan RSA
    :param message: str - pesan yang akan dienkripsi
    :param des_key: str - kunci DES
    :param rsa_public_key: tuple (e, n) - kunci publik RSA
    :return: tuple (encrypted_message, encrypted_des_key)
    """

    # Enkripsi pesan menggunakan DES
    encrypted_message = encryption_dynamic(message, des_key)

    # Enkripsi kunci DES menggunakan RSA
    encrypted_des_key = rsa_encrypt_des_key(des_key, rsa_public_key)

    print(encrypted_message, encrypted_des_key)

    return encrypted_message, encrypted_des_key

def hybrid_decrypt(encrypted_message: str, encrypted_des_key: int, rsa_private_key):
    """
    Mendekripsi pesan yang dienkripsi menggunakan sistem hybrid
    :param encrypted_message: str - pesan terenkripsi
    :param encrypted_des_key: int - kunci DES terenkripsi
    :param rsa_private_key: tuple (d, n) - kunci private RSA
    :return: str - pesan yang sudah didekripsi
    """
    # Dekripsi kunci DES
    des_key = rsa_decrypt_des_key(encrypted_des_key, rsa_private_key)

    # Dekripsi pesan menggunakan kunci DES yang sudah didekripsi
    decrypted_message = decryption_dynamic(encrypted_message, des_key)

    print(encrypted_message, encrypted_des_key)

    return decrypted_message
