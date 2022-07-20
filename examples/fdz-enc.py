#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import hashlib, secrets
from binascii import hexlify, unhexlify

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def fdz_enc(pt: str)->bytes:
    

    with open("../pki/fdz.der", "rb") as f:
        fdz_cert_der = f.read()
        fdz_cert = x509.load_der_x509_certificate(fdz_cert_der, default_backend())
        # das geladene Zertifikat muss jetzt in einer echten Implementierung 
        # erst noch geprüft werden bevor der öffentliche Schlüssel aus dem Zertifikat 
        # wirklich benutzt wird ... nicht Teil des PoCs.
        fdz_public_key = fdz_cert.public_key()
        fdz_pn = fdz_public_key.public_numbers()
        print("INFO: fdz_x={} fdz_y={}".format(hex(fdz_pn.x), hex(fdz_pn.y)))

    # Jetzt verschlüssele ich den plaintext (pt).
    private_key = ec.generate_private_key(ec.BrainpoolP256R1(), default_backend())
    print("INFO: d=", hex(private_key.private_numbers().private_value))
    pn = private_key.public_key().public_numbers()
    print("INFO: x={} y={}".format(hex(pn.x), hex(pn.y)))
    shared_secret = private_key.exchange(ec.ECDH(), fdz_public_key)
    print("INFO:", hexlify(shared_secret))
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'', backend=default_backend())
    aes_key = hkdf.derive(shared_secret)
    print("INFO:", hexlify(aes_key))
    plaintext = pt.encode()
    iv = secrets.token_bytes(12)
    print("INFO:", hexlify(iv))
    ciphertext_aes = AESGCM(aes_key).encrypt(iv, plaintext, associated_data=None)
    x = unhexlify("{:x}".format(pn.x).zfill(64))
    y = unhexlify("{:x}".format(pn.y).zfill(64))

    ct = b'\x01' + x + y + iv + ciphertext_aes

    return ct


def fdz_dec(ct: bytes)->str:
    
    # s ist jetzt Hexkodiert, im Produktivcode ist das Base64-kodiert
    # ... im Beispiel kann man Hex besser lesen, deswegen ...

    assert len(ct) >= 1 + 32 + 32 + 12 + 1 + 16
    assert ct[0] == 1

    # Den pivaten VST-Depseudonymisierungsschlüssel laden
    with open("../pki/fdz-key.pem", "rb") as f:
        fdz_private_key = serialization.load_pem_private_key(
            f.read(), password=None, backend=default_backend())

    print("INFO: FDZ-private-key", hex(fdz_private_key.private_numbers().private_value))
    pub_numbers = ec.EllipticCurvePublicNumbers(
        int.from_bytes(ct[1:1+32], byteorder='big'),
        int.from_bytes(ct[33:33+32], byteorder='big'),
        ec.BrainpoolP256R1())
    return ''
    #message_public_key = pub_numbers.public_key()

    # Diese Schritt würde dann im HSM geschehen
    shared_secret = fdz_private_key.exchange(ec.ECDH(), message_public_key)

    # Die restlichen Schritt ausserhalb des HSM: 

    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'', backend=default_backend())
    aes_key = hkdf.derive(shared_secret)

    # Die Nachricht wird jetzt mit AES/GCM entschlüsseln.
    aesgcm = AESGCM(aes_key)
    iv = ct[1+32+32:1+32+32+12]; assert len(iv) == 12
    ciphertext = ct[1+32+32+12:]
    pt = aesgcm.decrypt(iv, ciphertext, associated_data=None)

    return pt.decode()


if __name__ == '__main__':
    
    plaintext = "Ich in ein anonymisiertes medizinische Datenobjekt oder ein VST-JWT."
    print(f"{plaintext=}")

    my_ct = fdz_enc(plaintext)
    print("hexdump der chiffrats:", hexlify(my_ct).decode())

    my_pt = fdz_dec(my_ct)
    print("entschlüsseltes Chiffrat:", my_pt)
    
