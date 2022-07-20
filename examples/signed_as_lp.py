#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import hashlib, json, secrets
from datetime import datetime, timedelta
from base64 import b64encode, urlsafe_b64encode
from binascii import unhexlify

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# Einfach 32 Byte Zufall, entscheidend ist dass der Zufall (Auftragsnummer)
# an das LP per Signatur gebunden wird (siehe folgend).
an = secrets.token_bytes(32)

# lp
## Ich nehme als Beispiel folgende Nutzer-KVNR an
KVNR = "A123456789" 

with open("../pki/vst.der", "rb") as f:
    vst_cert_der = f.read()
    vst_cert_hash = b64encode(hashlib.sha256(vst_cert_der).digest()).decode()
    vst_cert = x509.load_der_x509_certificate(vst_cert_der, default_backend())
    # das geladene Zertifikat muss jetzt in einer echten Implementierung 
    # erst noch geprüft werden bevor der Schlüssel aus dem Zertifikat 
    # wirklich benutzt wird ... nicht Teil des PoCs.
    vst_public_key = vst_cert.public_key()

# Jetzt verschlüssele ich als AS (Komponente Autorisierung) die KVNR für die VST.
# Das Chiffrat ist nach Pseudonymisierungskonzept das Lieferpseudonym (LB).
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

# so nun das als signiertes Tupel (JSON Web Signatur) zusammenführen
with open("../pki/as.der", "rb") as f:
    as_cert_der = f.read()
    B_as_cert_der = b64encode(as_cert_der).decode() 

# JSON Web Signature https://datatracker.ietf.org/doc/html/rfc7515
header = {'alg': 'ES256', 'x5c': [B_as_cert_der]}
B_header = urlsafe_b64encode(json.dumps(header).encode())
my_now = datetime.utcnow()
my_exp = my_now + timedelta(hours=1)
body = { 
        "wn"   : b64encode(an).decode(),
        "dp"   : b64encode(lp).decode(),
        "vst_cert_hash" : vst_cert_hash,
        "nbf"  : my_now.isoformat(),
        "iat"  : my_now.isoformat(),
        "exp"  : my_exp.isoformat(),
        "ocsp" : "... ocsp-response ..."
     }
B_body = urlsafe_b64encode(json.dumps(body).encode())

with open("../pki/as-key.pem", "rb") as f:
    as_private_key_data = f.read()

as_private_key = serialization.load_pem_private_key(as_private_key_data,
                 password=None, backend=default_backend())
signature = as_private_key.sign(B_body, ec.ECDSA(hashes.SHA256()))
B_signature = urlsafe_b64encode(signature)

signierte_an_und_lp = (B_header + b"." + B_body + b"." + B_signature).decode()

print(signierte_an_und_lp)

