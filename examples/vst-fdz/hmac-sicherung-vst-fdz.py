#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import json, jwt, secrets
from datetime import datetime, timedelta


gemeinsames_geheimnis_zwischen_vst_und_fdz = "dc0b6d9cffb4ad27e8c80d9c095ead027489a81f33bbba707fc1df037ea88056"

# von der VST an das FDZ zu übertragende Daten
# Auftragsnummer
an = "64c5c37d472f0c0a60eb5f27d63b2caa63196cde855e7617daa9df0320a3efbd"
# periodenübergreifendes Pseudonym
pp = "periodenübergreifendes Pseudonym für KVNR A123456789"

# Die Zeiten sind nicht absolut notwendig, nur best-practice
my_now = datetime.utcnow()
my_exp = my_now + timedelta(hours=24)

# es ist hilfreich bei der Analyse von Fehlerfällen jeden Datensatz mit einer
# eindeutige ID zu versehen (nicht absolut notwendig, aber hilfreich).
transaktions_id = secrets.token_hex(32)

body = {
        "nbf"  : my_now.timestamp(),
        "iat"  : my_now.timestamp(),
        "exp"  : my_exp.timestamp(),
        "transaktions_id" : transaktions_id,
        "wn"   : an,
        "pp"   : pp
       }

daten = jwt.encode(body, gemeinsames_geheimnis_zwischen_vst_und_fdz, algorithm="HS256")

print("Die VST hat folgende Informationen als Tupel zusammengebracht:")
print(json.dumps(body, sort_keys=True, indent=4))

print("""
Mit einem gemeinsamen Geheimnis zwischen VST und FDZ wird das Tupel über
HMAC (RFC-2104) integritäts- und authentitätsgesichert und anschließend
gemäß RFC-7515 (JSON Web Signature) kodiert:
""")

print(daten, "\n")

print("Das wird vom FDZ geprüft (HMAC-Sicherung, Grundlage gemeinsames Geheimnis):")

geprüfter_body = jwt.decode(daten, gemeinsames_geheimnis_zwischen_vst_und_fdz, algorithms=["HS256"])


print("Nach Prüfung kann das FDZ auf folgende Daten zugreifen:")
print(json.dumps(geprüfter_body, sort_keys=True, indent=4))

