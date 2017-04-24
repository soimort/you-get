import sys
import hashlib

from ctypes import byref, c_void_p, c_buffer, c_char, c_uint16, c_uint32, c_int32, c_char_p, POINTER, Structure

from http.cookiejar import Cookie, CookieJar, MozillaCookieJar

from Crypto.Cipher import AES
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend


# https://chromium.googlesource.com/chromium/src/+/master/components/os_crypt/os_crypt_linux.cc#80
# https://chromium.googlesource.com/chromium/src/+/master/components/os_crypt/keychain_password_mac.mm#50
def key_mac(browser="Chromium"):
    service_name = ("Chromium Safe Storage" if browser == "Chromium" else "Chrome Safe Storage")

    # from github: keyring/backends/_OS_X_API.py
    noErr = 0
    _sec = ctypes.CDLL('/System/Library/Frameworks/Security.framework/Versions/A/Security')
    SecKeychainFindGenericPassword = _sec.SecKeychainFindGenericPassword
    SecKeychainFindGenericPassword.argtypes = (
        c_void_p,
        c_uint32,
        c_char_p,
        c_uint32,
        c_char_p,
        POINTER(c_uint32),  # passwordLength
        POINTER(c_void_p),  # passwordData
        POINTER(sec_keychain_item_ref),  # itemRef
    )
    SecKeychainFindGenericPassword.restype = c_uint32
    SecKeychainItemFreeContent = _sec.SecKeychainItemFreeContent
    SecKeychainItemFreeContent.argtypes = (
        c_void_p, c_void_p,
    )
    SecKeychainItemFreeContent.restype = c_uint32

    passwdlen = c_uint32()
    passwd    = c_void_p()
    status = SecKeychainFindGenericPassword(None,
                                            len(service_name),
                                            service_name,
                                            len(browser),
                                            browser,
                                            passwdlen,
                                            passwd,
                                            None,
                                            )
    if status != noErr: return ""
    password = ctypes.create_string_buffer(passwdlen.value)
    ctypes.memmove(password, passwd.value, passwdlen.value)
    SecKeychainItemFreeContent(None, passwd)
    return password.raw.decode('utf-8')
def key(browser="Chromium"):
    if sys.platform == "linux":
        return "peanuts"	# v10
    elif sys.platform == "darwin":
        return key_mac(browser)
    return ""


# https://chromium.googlesource.com/chromium/src/+/master/crypto/symmetric_key.cc#53
def encrypt_key(key, salt, iterations, key_size_in_bits):
    return hashlib.pbkdf2_hmac("sha1", key, salt, iterations, key_size_in_bits / 8)


def decode(ciphertext):
    if not ciphertext: return ciphertext

    if sys.platform == "win32":
        return decode_windows(ciphertext)

    passwd = key(browser="Chromium") or key(browser="Chrome")

    if not passwd: return ""
    if sys.platform == "linux":
        text = decode_linux(ciphertext, passwd)
    elif sys.platform == "darwin":
        text = decode_macos(ciphertext, passwd)
    else: return ciphertext

    right = text[-1]
    if type(right) != int: right = ord(right)
    return text[:-right].decode('utf-8', 'replace')


# https://chromium.googlesource.com/chromium/src/+/master/components/os_crypt/os_crypt_linux.cc#182
# avaliable versions: v10
def decode_linux(ciphertext, key="peanuts"):
    # Salt for Symmetric key derivation.
    kSalt = b"saltysalt"
    # Key size required for 128 bit AES.
    kDerivedKeySizeInBits = 128
    # Constant for Symmetic key derivation.
    kEncryptionIterations = 1
    # Size of initialization vector for AES 128-bit.
    kIVBlockSizeAES128 = 16

    encrypted = encrypt_key(key.encode("utf-8"), kSalt, kEncryptionIterations, kDerivedKeySizeInBits)	# v10
    iv = kIVBlockSizeAES128 * b" "
    return AES.new(encrypted, AES.MODE_CBC, iv).decrypt(ciphertext[3:])
    # cipher = Cipher(algorithms.AES(encrypted), modes.CBC(iv), backend=default_backend())
    # d = cipher.decryptor()
    # return d.update(ciphertext[3:]) + d.finalize()


# https://chromium.googlesource.com/chromium/src/+/master/components/os_crypt/os_crypt_win.cc#48
def decode_windows(ciphertext):
    from ctypes import cdll, windll
    from ctypes.wintypes import DWORD

    class DATA_BLOB(Structure):
        _fields_ = [("cbData", DWORD), ("pbData", POINTER(c_char))]

    def decrypt(ciphertext):
        memcpy = cdll.msvcrt.memcpy
        CryptUnprotectData = windll.crypt32.CryptUnprotectData
        LocalFree = windll.kernel32.LocalFree

        bufferIn = c_buffer(ciphertext, len(ciphertext))
        blobIn = DATA_BLOB(len(ciphertext), bufferIn)
        blobOut = DATA_BLOB()
        if CryptUnprotectData(byref(blobIn), None, None, None, None, None, byref(blobOut)):
            cbData = int(blobOut.cbData)
            pbData = blobOut.pbData
            buffer = c_buffer(cbData)
            memcpy(buffer, pbData, cbData)
            LocalFree(pbData)
            return buffer.raw
        else:
            return ""
    return decrypt(ciphertext)


# https://chromium.googlesource.com/chromium/src/+/master/components/os_crypt/os_crypt_mac.mm#133
# avaliable versions: v10
# TODO: need test
def decode_macos(ciphertext, key=""):
    # Salt for Symmetric key derivation.
    kSalt = b"saltysalt"
    # Key size required for 128 bit AES.
    kDerivedKeySizeInBits = 128
    # Constant for Symmetic key derivation.
    kEncryptionIterations = 1003
    # TODO(dhollowa): Refactor to allow dependency injection of Keychain.
    use_mock_keychain = False

    encrypted = encrypt_key(key.encode("utf-8"), kSalt, kEncryptionIterations, kDerivedKeySizeInBits)	# v10
    iv = kIVBlockSizeAES128 * b" "
    return AES.new(encrypted, AES.MODE_CBC, iv).decrypt(ciphertext[3:])
    # cipher = Cipher(algorithms.AES(encrypted), modes.CBC(iv), backend=default_backend())
    # d = cipher.decryptor()
    # return d.update(ciphertext[3:]) + d.finalize()


def load_cookies(a):
    try:
        cookies = MozillaCookieJar(a)
        cookies.load()
    except:
        import sqlite3

        cookies = MozillaCookieJar()
        con = sqlite3.connect(a)
        cur = con.cursor()

        tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()

        stmt = ""
        for t in tables:
            if t[0] == "cookies":
                stmt = "SELECT host_key, path, secure, expires_utc, name, value, encrypted_value FROM cookies"; break
            elif t[0] == "moz_cookies":
                stmt = "SELECT host, path, isSecure, expiry, name, value FROM moz_cookies"; break
        if not stmt: return

        items = cur.execute(stmt).fetchall()
        con.close()

        for item in items:
            value = item[5]
            if len(item) == 7 and not value: value = decode(item[-1])
            c = Cookie(0, item[4], value,
                       None, False,
                       item[0],
                       item[0].startswith('.'),
                       item[0].startswith('.'),
                       item[1], False,
                       item[2],
                       item[3], item[3]=="",
                       None, None, {})
            cookies.set_cookie(c)
        return cookies
