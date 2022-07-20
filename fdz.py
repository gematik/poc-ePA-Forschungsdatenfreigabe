#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Forschungsdatenzentrum (FDZ) Schnittstelle zur Übertragung der
pseudonymisierten medizinischen Daten (ePA)
"""

import base64, json, re

from flask import Flask, request, jsonify
from binascii import hexlify, unhexlify


def jb64d(data):
    """
    Adds back in the required padding before decoding.
    """
    padding_len = 4 - (len(data) % 4)
    data = data + ("=" * padding_len)
    return base64.urlsafe_b64decode(data)

app = Flask(__name__)

@app.route('/v1/epa/certificate', methods=['GET'])
def get_certificate():

    with open("pki/fdz.der", "rb") as cert_file:
        cert_data = certfile.read()

    return Response(cert_data, mimetype='application/pkix-cert')

@app.route('/v1/epa/mio/<p_document_id>', methods=['POST', 'DELETE'])
def mio_upload_or_delete(p_document_id: str):

    if not re.match(r"^[0-9a-f]{64}$", p_document_id):
        return jsonify({"status" : "fail", "descr": "parameter doid invalid"}), 400

    if 'Signed-WN' not in request.headers:
        return jsonify({"status" : "fail", "descr": "no Signed-WN header variable found"}), 400

    # todo Signatur der WN (JWT) prüfen
    body_data = request.headers['Signed-WN'].split(".")[1]
    body = json.loads(jb64d(body_data))
    wn = body["wn"]

    if request.method == 'DELETE':
        # Schreibe den Löschauftrag in die FDZ-Message-queue
        # ...
        # und den FdV kann ich schon einen 202-Ist-So-Gut-Wie-Erledigt 
        # senden
        return jsonify({"status" : "ok"}), 202

    if request.content_type == "application/octet-stream":

        # Im Produktcode würde man (weil es nicht viel kostet und aus 
        # best-practise-Gründen) prüfen ob die hex-kodierung ok ist.
        print("Auftragsnummer ist", wn)

        # hier wäre es ein valides Vorgehen, das verschlüsselte MIO
        # auf Schnittstellen-Ebene erst einmal zu akzeptieren und erst
        # später/tiefer im FDZ die Entschlüsselung (bspw. mit Beteiligung
        # eines HSM) vorzunehmen.
        print("Für das FDZ verschlüsselte MIO (als Hexdump):")
        data = request.get_data()
        print(hexlify(data).decode())

        # Für die Entschlüsselung des Chiffrats vgl. examples/fdz-dec.py

        return jsonify({"status" : "ok"}), 201
    else:
        return jsonify({"status" : "fail", "descr" : "invalid mimetype"}), 415

@app.route('/v1/epa/mios', methods=['DELETE'])
def do_multiple_withdraws():

    if request.content_type != "application/json":
        return jsonify({"status" : "fail", "descr": "wrong mimetype"}), 400

    my_post_data = request.get_data().decode()
    try:
        my_array = json.loads(my_post_data)
    except:
        return jsonify({"status" : "fail", "descr": "err parsing json input"}), 400

    if len(my_array) == 0:
        return jsonify({"status" : "fail", "descr": "empty array?"}), 400

    for identifyer in my_array:
        if not re.match(r"^[0-9a-f]{64}$", identifyer):
            return jsonify({"status" : "fail", "descr": "one element of p_document_id-s invalid"}), 400

    # Im FDZ die Löschung von Daten mit ID doid durchführen bzw. initiieren.

    return jsonify({"status" : "ok"}), 202

@app.route('/v1/epa/wn-pp', methods=['POST'])
def pp_upload():

    if request.content_type == "application/octet-stream":

        print("Für das FDZ verschlüsselte AN+PP-Tupel (als Hexdump):")
        data = request.get_data()
        print(hexlify(data).decode())
        # Das speichere ich mir als FDZ lokal irgendwo hin (message-queue / 
        # directory etc.).

        # Für die Entschlüsselung des Chiffrats vgl. examples/fdz-dec.py
        # Die Entschlüsselung findet asynchron im FDZ statt, der Client (VST) bekommt
        # unabhängig davon erst mal ein 201-Created.

        return jsonify({"status" : "ok"}), 201
    else:
        return jsonify({"status" : "fail", "descr" : "invalid mimetype"}), 415


if __name__ == '__main__':

    app.run(port=20003, debug=True)

