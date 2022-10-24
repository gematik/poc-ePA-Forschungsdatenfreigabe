#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
AN = Auftragsnummer = working number = wn
LP = Lieferpseudonym = delivery pseudonym = dp

Das AS erzeugt auf Anfrage durch das ePA-FdV
    (1) ein signiertes AN+LP-Tupel (JWT) und 
    (2) ein JWT mit nur der AN.

Beide gehen an das ePA-FdV. Das ePA-FdV sendet (1) an die VST und (2) an das
FDZ.

"""

import base64, hashlib, json, secrets, jwt

from binascii import unhexlify, hexlify
from datetime import datetime, timedelta

from flask import Flask, jsonify, request

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


app = Flask(__name__)

# die konkrete URL kann das AS<->ePA-FdV selbst definierten ... ist also
# nur als Beispiel hier zu verstehen.
@app.route('/datenfreigabe/token', methods=['GET'])
def my_token():

    # Einfach 32 Byte Zufall, entscheidend ist dass der Zufall an das LP per
    # Signatur gebunden wird (siehe folgend).
    an = secrets.token_bytes(32)

    ## Ich nehme als Beispiel folgende Nutzer-KVNR an
    KVNR = "A123456789"


    ##
    ## Teil 1: Lieferpseudonym (LP) im AS erzeugen
    ##

    # lp
    with open("pki/vst.der", "rb") as vst_cert_file:
        vst_cert_der = vst_cert_file.read()
        vst_cert_hash = base64.b64encode(hashlib.sha256(vst_cert_der).digest()).decode()
        vst_cert = x509.load_der_x509_certificate(vst_cert_der, default_backend())
        # das geladene Zertifikat muss jetzt in einer echten Implementierung
        # erst noch geprüft werden bevor der Schlüssel aus dem Zertifikat
        # wirklich benutzt wird ... nicht Teil des PoCs.
        # Die TI-PKI-Zertifikatsprüfung ist schon in den AS implementiert.
        vst_public_key = vst_cert.public_key()

    # Jetzt verschlüssele ich als AS (Komponente Autorisierung) die KVNR für die VST.
    # Das Chiffrat ist nach Pseudonymisierungskonzept das Lieferpseudonym (LP).
    # Für das Pseudonymisierungskonzept ist wichtig, dass es gerade ein
    # randomisierendes Verschlüsselungsverfahren ist.
    # Das ist eine normale ECIES-Verschlüsselung (vgl. E-Rezept etc.).

    private_key = ec.generate_private_key(ec.BrainpoolP256R1(), default_backend())
    pn = private_key.public_key().public_numbers()
    shared_secret = private_key.exchange(ec.ECDH(), vst_public_key)
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'', backend=default_backend())
    aes_key = hkdf.derive(shared_secret)
    plaintext = KVNR.encode()
    iv = secrets.token_bytes(12)
    ciphertext_aes = AESGCM(aes_key).encrypt(iv, plaintext, associated_data=None)
    # kann man natürlich auch mit pn.x.to_bytes(length=32, byteorder="big", signed=False) 
    # machen ... ich mache es mal hier "per Hand" um deutlicher zu machen was
    # eigentlich hier passiert
    x = unhexlify("{:x}".format(pn.x).zfill(64))
    y = unhexlify("{:x}".format(pn.y).zfill(64))

    # analog E-Rezept-ECIES-Verschlüsselung
    lp = b'\x01' + x + y + iv + ciphertext_aes

    ##
    ## Teil 2: signierte AN+LP-Tupel (JWT) erzeugen
    ##

    # so nun AN+LP als signiertes Tupel (JWT) zusammenführen
    with open("pki/as.der", "rb") as as_cert_file:
        as_cert_der = as_cert_file.read()
        # RFC-7515#4.1.6 -> hier base64 und nicht base64urlsafe
        b_as_cert_der = base64.b64encode(as_cert_der).decode()

    with open("pki/as-key.pem", "rb") as as_signing_key_file:
        as_private_key_data = as_signing_key_file.read()
        as_private_key = serialization.load_pem_private_key(as_private_key_data,
                         password=None, backend=default_backend())

    # JSON Web Signature https://datatracker.ietf.org/doc/html/rfc7515
    my_now = datetime.utcnow()
    my_exp = my_now + timedelta(hours=24)

    body = { "wn"   : base64.b64encode(an).decode(),
             "dp"   : base64.b64encode(lp).decode(),
             "iat"  : my_now.timestamp(),
             "exp"  : my_exp.timestamp(),
             "iss"  : "http://authorization.aktensystem.ti",
             "vst_cert_hash" : vst_cert_hash }

    signierte_an_und_lp = jwt.encode(body, as_private_key, \
                algorithm="ES256", headers={"x5c" : [b_as_cert_der]})

    ##
    ## Teil 3: signierte AN-JWT erzeugen
    ##

    # Lieferpseudonym löschen: Im Token für das FDZ, ist dieses nicht
    # enthalten
    del body["dp"]

    if "vst_cert_hash" in body:
        del body["vst_cert_hash"]

    signierte_an = jwt.encode(body, as_private_key, \
                algorithm="ES256", headers={"x5c" : [b_as_cert_der]})

    print(request.headers)
    return jsonify([signierte_an_und_lp, signierte_an]), 200

if __name__ == '__main__':

    app.run(port=20001, debug=True)

