#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Das AS erzeugt (1) ein signiertes AN+LP-Tupel (JWT)
und (2) ein JWT mit nur der AN. Beide gehe an das ePA-FdV.
Das ePA-FdV sendet (1) an die VST und (2) an das FDZ."

"""

import base64, hashlib, json, secrets

from binascii import unhexlify, hexlify
from datetime import datetime, timedelta

from flask import Flask, jsonify

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def jb64e(data):
    """
    Removes any `=` used as padding from the encoded string.
    """
    if type(data) == "str":
        data = data.encode()

    encoded = base64.urlsafe_b64encode(data)
    return encoded.rstrip(b"=")

def jb64d(data):
    """
    Adds back in the required padding before decoding.
    """
    padding_len = 4 - (len(data) % 4)
    data = data + ("=" * padding_len)
    return base64.urlsafe_b64decode(data)

app = Flask(__name__)

@app.route('/datenfreigabe/token', methods=['GET'])
def my_token():

    # Einfach 32 Byte Zufall, entscheidend ist dass der Zufall an das LP per
    # Signatur gebunden wird (siehe folgend).
    an = secrets.token_bytes(32)

    ## Ich nehme als Beispiel folgende Nutzer-KVNR an
    KVNR = "A123456789"


    ##
    ## Teil 1: Lieferpseudonym (LP) m AS erzeugen
    ##

    # lp
    with open("pki/vst.der", "rb") as vst_cert_file:
        vst_cert_der = vst_cert_file.read()
        vst_cert_hash = base64.b64encode(hashlib.sha256(vst_cert_der).digest()).decode()
        vst_cert = x509.load_der_x509_certificate(vst_cert_der, default_backend())
        # das geladene Zertifikat muss jetzt in einer echten Implementierung
        # erst noch geprüft werden bevor der Schlüssel aus dem Zertifikat
        # wirklich benutzt wird ... nicht Teil des PoCs.
        vst_public_key = vst_cert.public_key()

    # Jetzt verschlüssele ich als AS (Komponente Autorisierung) die KVNR für die VST.
    # Das Chiffrat ist nach Pseudonymisierungskonzept das Lieferpseudonym (LP).
    private_key = ec.generate_private_key(ec.BrainpoolP256R1(), default_backend())
    pn = private_key.public_key().public_numbers()
    shared_secret = private_key.exchange(ec.ECDH(), vst_public_key)
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'', backend=default_backend())
    aes_key = hkdf.derive(shared_secret)
    plaintext = KVNR.encode()
    iv = secrets.token_bytes(12)
    ciphertext_aes = AESGCM(aes_key).encrypt(iv, plaintext, associated_data=None)
    x = unhexlify("{:x}".format(pn.x).zfill(64))
    y = unhexlify("{:x}".format(pn.y).zfill(64))

    lp = b'\x01' + x + y + iv + ciphertext_aes

    ##
    ## Teil 2: signierte AN+LP-Tupel (JWT) erzeugen
    ##

    # so nun AN+LP als signiertes Tupel (JWT) zusammenführen
    with open("pki/as.der", "rb") as as_cert_file:
        as_cert_der = as_cert_file.read()
        b_as_cert_der = base64.b64encode(as_cert_der).decode()

    # JSON Web Signature https://datatracker.ietf.org/doc/html/rfc7515
    header = {'alg': 'ES256', 'x5c': [b_as_cert_der]}
    b_header = jb64e(json.dumps(header).encode())
    my_now = datetime.utcnow()
    my_exp = my_now + timedelta(hours=24)
    body = {
            "wn"   : base64.b64encode(an).decode(),
            "dp"   : base64.b64encode(lp).decode(),
            "vst_cert_hash" : vst_cert_hash,
            "nbf"  : my_now.timestamp(),
            "iat"  : my_now.timestamp(),
            "exp"  : my_exp.timestamp(),
         }
    b_body = jb64e(json.dumps(body).encode())

    with open("pki/as-key.pem", "rb") as as_signing_key_file:
        as_private_key_data = as_signing_key_file.read()

    as_private_key = serialization.load_pem_private_key(as_private_key_data,
                     password=None, backend=default_backend())
    signature = as_private_key.sign(b_body, ec.ECDSA(hashes.SHA256()))
    b_signature = jb64e(signature)

    signierte_an_und_lp = (b_header + b"." + b_body + b"." + b_signature).decode()

    ##
    ## Teil 3: signierte AN-JWT erzeugen
    ##

    del body["dp"]
    if "vst_cert_hash" in body:
        del body["vst_cert_hash"]

    b_body = jb64e(json.dumps(body).encode())

    signature = as_private_key.sign(b_body, ec.ECDSA(hashes.SHA256()))
    b_signature = jb64e(signature)

    signierte_an = (b_header + b"." + b_body + b"." + b_signature).decode()

    return jsonify([signierte_an_und_lp, signierte_an]), 200

if __name__ == '__main__':

    app.run(port=20001, debug=True)

