# desencription.py
from cryptography.fernet import Fernet
from django.conf import settings  # Para acceder a la clave secreta FERNET_KEY si está almacenada en settings.py

def decrypt_private_key(encrypted_private_key):
    """
    Desencripta la clave privada cifrada utilizando Fernet.

    Args:
        encrypted_private_key (str): La clave privada cifrada en formato Base64.

    Returns:
        str: La clave privada desencriptada en formato hexadecimal.
    """
    # Clave secreta para el cifrado (asegúrate de que esté almacenada de forma segura)
    fernet_key = settings.FERNET_KEY  # Usamos la clave almacenada en settings.py o en otro lugar seguro.
    
    # Inicializamos el objeto Fernet con la clave secreta
    cipher_suite = Fernet(fernet_key)

    # Desencriptar la clave privada cifrada (no decodificarla como utf-8)
    decrypted_key = cipher_suite.decrypt(encrypted_private_key.encode())

    # La clave privada debe ser binaria, si la necesitas en formato hexadecimal:
    return decrypted_key.hex()  # Convertirla a hexadecimal para ser usada más adelante

