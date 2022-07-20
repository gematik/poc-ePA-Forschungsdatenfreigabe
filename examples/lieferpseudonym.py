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


def Beispiel_Lieferpseudonym_erzeugen():
    
    # LP
    ## Ich nehme als Beispiel folgende Nutzer-KVNR an
    KVNR = "A123456789" 

    with open("../pki/vst.der", "rb") as f:
        vst_cert_der = f.read()
        vst_cert = x509.load_der_x509_certificate(vst_cert_der, default_backend())
        # das geladene Zertifikat muss jetzt in einer echten Implementierung 
        # erst noch geprüft werden bevor der öffentliche Schlüssel aus dem Zertifikat 
        # wirklich benutzt wird ... nicht Teil des PoCs.
        vst_public_key = vst_cert.public_key()
        vst_pn = vst_public_key.public_numbers()
        print("INFO: vst_x={} vst_y={}".format(hex(vst_pn.x), hex(vst_pn.y)))

    # Jetzt verschlüssele ich als AS (Komponente Autorisierung) die KVNR für die VST.
    # Das Chiffrat ist nach Pseudonymisierungskonzept das Lieferpseudonym (LP).
    private_key = ec.generate_private_key(ec.BrainpoolP256R1(), default_backend())
    print("INFO: d=", hex(private_key.private_numbers().private_value))
    pn = private_key.public_key().public_numbers()
    print("INFO: x={} y={}".format(hex(pn.x), hex(pn.y)))
    shared_secret = private_key.exchange(ec.ECDH(), vst_public_key)
    print("INFO:", hexlify(shared_secret))
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'', backend=default_backend())
    aes_key = hkdf.derive(shared_secret)
    print("INFO:", hexlify(aes_key))
    plaintext = KVNR.encode()
    iv = secrets.token_bytes(12)
    print("INFO:", hexlify(iv))
    ciphertext_aes = AESGCM(aes_key).encrypt(iv, plaintext, associated_data=None)
    x = unhexlify("{:x}".format(pn.x).zfill(64))
    y = unhexlify("{:x}".format(pn.y).zfill(64))

    lp = b'\x01' + x + y + iv + ciphertext_aes

    return hexlify(lp).decode()


def Beispiel_Lieferpseudoynm_depseudonymisierung(s: str):
    
    # s ist jetzt Hexkodiert, im Produktivcode ist das Base64-kodiert
    # ... im Beispiel kann man Hex besser lesen, deswegen ...

    lp = unhexlify(s.encode())

    assert len(lp) == 1 + 32 + 32 + 12 + 10 + 16
    assert lp[0] == 1

    # Den pivaten VST-Depseudonymisierungsschlüssel laden
    with open("../pki/vst-key.pem", "rb") as f:
        vst_private_key = serialization.load_pem_private_key(
            f.read(), password=None, backend=default_backend())

    print("INFO: VST-private-key", hex(vst_private_key.private_numbers().private_value))
    pub_numbers = ec.EllipticCurvePublicNumbers(
        int.from_bytes(lp[1:1+32], byteorder='big'),
        int.from_bytes(lp[33:33+32], byteorder='big'),
        ec.BrainpoolP256R1())
    message_public_key = pub_numbers.public_key()

    # Diese Schritt würde dann im HSM geschehen
    shared_secret = vst_private_key.exchange(ec.ECDH(), message_public_key)

    # Die restlichen Schritt ausserhalb des HSM: 

    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'', backend=default_backend())
    aes_key = hkdf.derive(shared_secret)

    # Die Nachricht wird jetzt mit AES/GCM entschlüsseln.
    aesgcm = AESGCM(aes_key)
    iv = lp[1+32+32:1+32+32+12]; assert len(iv) == 12
    ciphertext = lp[1+32+32+12:]
    KVNR = aesgcm.decrypt(iv, ciphertext, associated_data=None)

    return KVNR.decode()


if __name__ == '__main__':
    
    print(">>> Das Aktensystem erzeugt das LP (was dann als signierte AN+LP Tupel an das FdZ->VST geht).")

    print("Hexdump des Lieferpseudonym ist:", Beispiel_Lieferpseudonym_erzeugen(),"\n")
    print("Hexdump des Lieferpseudonym ist:", Beispiel_Lieferpseudonym_erzeugen(),"\n")

    print(">>> Als VST kenne ich den privaten Schlüssel")

    print("Depseudonymisierung: KVNR={}".format(Beispiel_Lieferpseudoynm_depseudonymisierung(
                    Beispiel_Lieferpseudonym_erzeugen())))

