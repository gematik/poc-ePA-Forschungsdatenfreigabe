#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import base64, hashlib, json

from flask import Flask, request, Response, jsonify, make_response

from collections import defaultdict

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidSignature

app = Flask(__name__)

@app.route('/v1/epa/certificate', methods=['GET'])
def get_certificate():

    with open("pki/vst.der", "rb") as cert_file:
        cert_data = certfile.read()

    return Response(cert_data, mimetype='application/pkix-cert')

def jb64d(data):
    """
    Adds back in the required padding before decoding.
    """
    padding_len = 4 - (len(data) % 4)
    data = data + ("=" * padding_len)
    return base64.urlsafe_b64decode(data)

@app.route('/v1/epa/signed_wn_dp', methods=['POST'])
def post_signed_wn_dp():

    if request.content_type == 'application/jwt':

        # Hier muss man im Produktivcode testen, ob der client auch
        # korrekt unicode verwendet, oder einen Ärgern möchte.
        post_data = request.get_data().decode()

        ar = post_data.split(".")
        if len(ar) != 3:
            return jsonify({"status" : "invalid request"}), 400

        with open("pki/as.der", "rb") as f:
            as_cert_der = f.read()

        # Im Produktivcode würde man das "signierende" Zertifikat aus dem 
        # Header-Teil der JSON-Web-Signature extrahieren und das Zertifikat
        # erst prüfen und dann erst für die folgende Signaturprüfung verwenden.
        # Hier lade ich es aus dem lokalen Dateisystem.
        as_cert = x509.load_der_x509_certificate(as_cert_der, default_backend())
        public_key = as_cert.public_key()

        try:
            signature = jb64d(ar[-1])
            # Signatur des AS prüfen 
            public_key.verify(signature, ar[1].encode(), ec.ECDSA(hashes.SHA256()))
            my_body = json.loads(jb64d(ar[1]))
            my_body = defaultdict(lambda: "", my_body)
        except InvalidSignature:
            print("sigfail")
            return jsonify({"status" : "sig-fail"}), 401
        except Exception as e:
            print("Fehler", str(e))
            return jsonify({"status" : "fail"}), 400

        an = my_body["wn"]

        # hier sollte man im Produktivcode die AN als preiswerten Sanity-Check
        # prüfen (Mindestlänge, korrekte Kodierung (Base64))
        print("Auftragsnummer ist", an) 

        # LP entschlüsseln und auf korrekte Konstruktion prüfen
        # kann man an dieser Stelle machen oder auch nicht (AS-Erzeugung des LP ist 
        # überprüfte Funktionalität) ... es wäre auch ok sich darauf zu verlassen.
        
        # vgl. dafür auch examples/lieferpseudonym.py

        return jsonify({"status" : "ok"}), 201
    else:
        return jsonify({"status" : "invalid mimetype"}), 415
        # 415 = Unsupported Media Type


if __name__ == '__main__':

    app.run(port=20002, debug=True)

