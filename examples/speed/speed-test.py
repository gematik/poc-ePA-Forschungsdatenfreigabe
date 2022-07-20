#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import base64, json, hashlib, requests, secrets, sys, time
from datetime import datetime, timedelta

from binascii import hexlify, unhexlify

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def jb64d(data):
    """
    Adds back in the required padding before decoding.
    """
    padding_len = 4 - (len(data) % 4)
    data = data + ("=" * padding_len)
    return base64.urlsafe_b64decode(data)

if __name__ == '__main__':

    AS_URL_1 = "http://127.0.0.1:20001/datenfreigabe/token"

    # Ich nehme im Beispiel an, dass ich als ePA-FdV schon am AS vollständig
    # eingeloggt bin.

    print(f"Beim AS ({AS_URL_1}) (1) ein signiertes AN+LP-Tupel und",
          " (2) signierte AN beziehen.")
    response = requests.get(
                    AS_URL_1,
                    headers={"SOAP_Access_Token" : "...AC-Token..."},
                    timeout=5
                )
    assert response.status_code == requests.codes.ok
    [signed_wn_dp_tupel, signed_wn] = response.json(); 
    print("\nErgebnis: (1)", signed_wn_dp_tupel)
    print("\nErgebnis: (2)", signed_wn, "\n")

    # Nur mal als Info den Body des signierten LP+AN-Tupel anzeigen
    body_data = signed_wn_dp_tupel.split(".")[1]
    body = json.loads(jb64d(body_data))
    print("Im Body von (1) befindet sich:\n", json.dumps(body, sort_keys=True, indent=4), sep='')

    print("\nDas signierte Tupel (s. o.) sende ich jetzt an die Vertrauensstelle.")
    VST_URL = "http://127.0.0.1:20002/v1/epa/signed_wn_dp"

    my_session = requests.Session()
    start = time.time()
    for _ in range(0,1000):
        response = my_session.post(
                        VST_URL,
                        headers={'Content-Type': 'application/jwt'},
                        data=signed_wn_dp_tupel,
                        timeout=5
                    )
        #print("Response-Code:", response.status_code)
        assert response.status_code == 201

        j = response.json(); 
        #print("Ergebnis:\n", j, sep='')

    ende = time.time()

    print("Dauer:", ende-start)

#    print("\nJetzt verschlüssele ich mein MIO für das FDZ und sende es an das FDZ inkl. AN")
#    # für ein Datenobjekt erzeugt das ePA-FdV zufällig einen 256-Bit data oject id
#    p_document_id = secrets.token_hex(32)
#
#    FDZ_URL = f"http://127.0.0.1:20003/v1/epa/mio/{p_document_id}"
#
#    with open("data/mio_1.txt", "rb") as f:
#        plaintext = f.read()
#        assert plaintext
#
#    with open("pki/fdz.der", "rb") as f:
#        fdz_cert_der = f.read()
#        fdz_cert_hash = base64.b64encode(hashlib.sha256(fdz_cert_der).digest()).decode()
#        fdz_cert = x509.load_der_x509_certificate(fdz_cert_der, default_backend())
#        # das geladene Zertifikat muss jetzt in einer echten Implementierung 
#        # erst noch geprüft werden bevor der Schlüssel aus dem Zertifikat 
#        # wirklich benutzt wird ... nicht Teil des PoCs.
#        fdz_public_key = fdz_cert.public_key()
#
#    private_key = ec.generate_private_key(ec.BrainpoolP256R1(), default_backend())
#    pn = private_key.public_key().public_numbers()
#    shared_secret = private_key.exchange(ec.ECDH(), fdz_public_key)
#    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'', backend=default_backend())
#    aes_key = hkdf.derive(shared_secret)
#    iv = secrets.token_bytes(12)
#    ciphertext_aes = AESGCM(aes_key).encrypt(iv, plaintext, associated_data=None)
#    x = unhexlify("{:x}".format(pn.x).zfill(64))
#    y = unhexlify("{:x}".format(pn.y).zfill(64))
#
#    ciphertext = b'\x01' + x + y + iv + ciphertext_aes
#
#    print(f"Hex-Dump des Chiffrats was ich gleich auf {FDZ_URL} POST-te:")
#    print(hexlify(ciphertext).decode())
#
#    response = requests.post(
#                    FDZ_URL,
#                    headers={'Signed-WN'     : signed_wn,
#                             'FDZ-Cert-Hash' : fdz_cert_hash,
#                             'Content-Type'  : 'application/octet-stream'},
#                    data=ciphertext,
#                    timeout=5
#                )
#    print("Response-Code:", response.status_code)
#    assert response.status_code == 201
#
#    j = response.json(); 
#    print("Ergebnis:\n", j, sep='')
#
#    print("\nJetzt widerrufe ich die Datenfreigabe wieder für das eben freigegebene MIO")
#
#    response = requests.delete(
#                    FDZ_URL,
#                    headers={'Signed-WN'     : signed_wn},
#                    timeout=5
#                )
#
#    print("Response-Code:", response.status_code)
#    assert response.status_code in [200, 202]
#
#    j = response.json(); 
#    print("Ergebnis:\n", j, sep='')
#
#    print("\nJetzt widerrufe ich als Test viele MIOs auf einmal")
#
#    FDZ_URL = f"http://127.0.0.1:20003/v1/epa/mios"
#
#    response = requests.delete(
#                    FDZ_URL,
#                    headers={'Signed-WN'     : signed_wn},
#                    json = [secrets.token_hex(32) for _ in range(0,10)],
#                    timeout=5
#                )
#    print("Response-Code:", response.status_code)
#    assert response.status_code in [200, 202]
#
#    j = response.json(); 
#    print("Ergebnis:\n", j, sep='')
#
