# Forschungsdatenfreigabe elektronisch Patientenakte

Wie in [gemF\_ePA\_FDZ\_Anbindung](https://fachportal.gematik.de)
überblicksartig dargstellt, können bei Einwilligung der versicherten Person auf
dem ePA-Frontend des Versicherten (ePA-FdV) medizinische Daten zunächst
anonymisiert werden und diese dann mit Hilfe einer Vertrauensstelle (VST,
verantwortet vom RKI) pseudonymisiert werden. Diese pseudonymisierten
medizinischen Daten werden dann vom ePA-FdV an das Forschungsdatenzentrum (FDZ, verantwortet vom BfArM)
gesendet.

## Beispiel-Implementierung Schnittstellen

Vertrauensstelle: [vst.py](vst.py),
[Erläuterungen zur Schnittstelle](README-VST.md),
[VST-OpenAPI-Spezifikation (YAML)](openapi/openapi-vst.yaml),
[VST-OpenAPI-Spezifikation (JSON)](openapi/openapi-vst.json)

Forschungsdatenzentrum: [fdz.py](vst.py),
[Erläuterungen zur Schnittstelle](README-FDZ.md),
[FDZ-OpenAPI-Spezifikation (YAML)](openapi/openapi-fdz.yaml),
[FDZ-OpenAPI-Spezifikation (JSON)](openapi/openapi-fdz.json)

ePA Frontend des Versicherten: [epa-fdv.py](epa-fdv.py)

ePA Aktensystem: [as.py](as.py) (Notwendig für die Erzeugung der Auftragsnummer (AN), des Lieferpseudonyms (LP) und des
Proxy-Tokens)

### Docker-Image

Eine lokale Instanz kann man auch leicht mit
dem [Dockerimage](https://hub.docker.com/r/gematik1/epa-forschungsdatenfreigabe-poc)
starten

    docker pull gematik1/epa-forschungsdatenfreigabe-poc:1.0.0
    docker run -it --entrypoint /bin/bash gematik1/epa-forschungsdatenfreigabe-poc:1.0.0

Dann hat man eine interaktive Shell in der man eingibt:

    ./start.sh
    ./epa-fdv

Toll.

Wenn man tiefer einsteigen möchte, mit

    tmux at

in die tmux-session gehen und mit Ctrl+A plus 1 bis 4 zwischen den Fenstern
hin und her schalten. D. h., `Ctrl+A 1` geht ins das erste Fenstern etc.

### Komponenten/Services per "Hand" starten

Wer nicht das Docker-Image verwenden möchte, kann die REST-Services auch per "Hand" starten:

    ./as.py
    ./vst.py
    ./fdz.py

### Beispieldurchlauf

    [a@h fdz]$ ./epa-fdv.py 
    Beim AS (http://127.0.0.1:20001/datenfreigabe/token) (1) ein signiertes AN+LP-Tupel und  (2) signierte AN beziehen.

    Ergebnis: (1) eyJhbGciOiAiRVMyNTYiLCAieDVjIjogWyJNSUlDQWpDQ0Fha0NGRmUyTVRZVX
    JYMjhVN2FYSm9XemIrWEYzcTlyTUFvR0NDcUdTTTQ5QkFNQ01IQXhDekFKQmdOVkJBWVRBa1JGTVE4d0
    RRWURWUVFJREFaQ1pYSnNhVzR4RHpBTkJnTlZCQWNNQmtKbGNteHBiakVRTUE0R0ExVUVDZ3dIWjJWdF
    lYUnBhekVRTUE0R0ExVUVDd3dIWjJWdFlYUnBhekViTUJrR0ExVUVBd3dTUzI5dGNHOXVaVzUwWlc0dF
    VFdEpMVU5CTUI0WERUSXlNRE13TVRFek5USXpPRm9YRFRJek1ETXdNVEV6TlRJek9Gb3dnWll4Q3pBSk
    JnTlZCQVlUQWtSRk1ROHdEUVlEVlFRSURBWkNaWEpzYVc0eER6QU5CZ05WQkFjTUJrSmxjbXhwYmpFWU
    1CWUdBMVVFQ2d3UFpWQkJJRUZyZEdWdWMzbHpkR1Z0TVNFd0h3WURWUVFMREJoTGIyMXdiMjVsYm5SbE
    lFRjFkRzl5YVhOcFpYSjFibWN4S0RBbUJnTlZCQU1NSDJWUVFTMUJVeUJMYjIxd2IyNWxiblJsSUVGMW
    RHOXlhWE5wWlhKMWJtY3dXakFVQmdjcWhrak9QUUlCQmdrckpBTURBZ2dCQVFjRFFnQUVraytOUDY4QW
    VVMXR6cis1UEFVZWtwWjNyTGtqU2h2ODhVSkpEQkFTSDh4emlYTU84TW1aU0p5SHZXRng0NlB4Rm80SU
    5CZmErcmh2dXBUTkhmbm9WakFLQmdncWhrak9QUVFEQWdOSEFEQkVBaUI5ZXpNMEtBckIwWU9XVi9YeG
    V6eDhYNTVtdi9ZN1Rld2dxRUJSS0psV2xnSWdJckdZa1QvdStZWjdieStVOE5lVHAzN28xWkZRMkJ2NS
    tLL3paZGlmQUFjPSJdfQ.eyJ3biI6ICJNajlzb0JZVUNhU2Jmajc0TUxjWWhwaGZUUHM0OTlzTDFRZWF
    wR2VhRDlNPSIsICJkcCI6ICJBUmNNeFozT2dicllXUG1RcWdCV1ljdmdzOXdkVWZ4YjFlaTRBT0dhWmp
    rSUdtRTdjTE9YdkN5Tklwb3VhQy80cVhnMXhqZDRMdEV2ZnlVV1F5MjBhTzRGWTJmb2xXMGY5ODdVUkx
    UMWJXeUkvOGtMeGRaTjVDMVl6d2hQeFJJVC9mVHllZ3lMY1E9PSIsICJ2c3RfY2VydF9oYXNoIjogIkJ
    tcjM1TkQzdzVrZW9LMVF0VVNLNmNrRC91M3RBYXJ1NkhuaEYxTThWNnM9IiwgIm5iZiI6IDE2NDk5MTQ
    0MTcuNTg5NTQ0LCAiaWF0IjogMTY0OTkxNDQxNy41ODk1NDQsICJleHAiOiAxNjUwMDAwODE3LjU4OTU
    0NH0.MEUCIFeqbMq0-vN0UwimkeD9YoTy_7gQftubs6bR76hfIzlrAiEAo18W84UG6BXL2nM1__iqxjf
    RQzU3q27cX5-mVV-0DUI

    Ergebnis: (2) eyJhbGciOiAiRVMyNTYiLCAieDVjIjogWyJNSUlDQWpDQ0Fha0NGRmUyTVRZVX
    JYMjhVN2FYSm9XemIrWEYzcTlyTUFvR0NDcUdTTTQ5QkFNQ01IQXhDekFKQmdOVkJBWVRBa1JGTVE4d0
    RRWURWUVFJREFaQ1pYSnNhVzR4RHpBTkJnTlZCQWNNQmtKbGNteHBiakVRTUE0R0ExVUVDZ3dIWjJWdF
    lYUnBhekVRTUE0R0ExVUVDd3dIWjJWdFlYUnBhekViTUJrR0ExVUVBd3dTUzI5dGNHOXVaVzUwWlc0dF
    VFdEpMVU5CTUI0WERUSXlNRE13TVRFek5USXpPRm9YRFRJek1ETXdNVEV6TlRJek9Gb3dnWll4Q3pBSk
    JnTlZCQVlUQWtSRk1ROHdEUVlEVlFRSURBWkNaWEpzYVc0eER6QU5CZ05WQkFjTUJrSmxjbXhwYmpFWU
    1CWUdBMVVFQ2d3UFpWQkJJRUZyZEdWdWMzbHpkR1Z0TVNFd0h3WURWUVFMREJoTGIyMXdiMjVsYm5SbE
    lFRjFkRzl5YVhOcFpYSjFibWN4S0RBbUJnTlZCQU1NSDJWUVFTMUJVeUJMYjIxd2IyNWxiblJsSUVGMW
    RHOXlhWE5wWlhKMWJtY3dXakFVQmdjcWhrak9QUUlCQmdrckpBTURBZ2dCQVFjRFFnQUVraytOUDY4QW
    VVMXR6cis1UEFVZWtwWjNyTGtqU2h2ODhVSkpEQkFTSDh4emlYTU84TW1aU0p5SHZXRng0NlB4Rm80SU
    5CZmErcmh2dXBUTkhmbm9WakFLQmdncWhrak9QUVFEQWdOSEFEQkVBaUI5ZXpNMEtBckIwWU9XVi9YeG
    V6eDhYNTVtdi9ZN1Rld2dxRUJSS0psV2xnSWdJckdZa1QvdStZWjdieStVOE5lVHAzN28xWkZRMkJ2NS
    tLL3paZGlmQUFjPSJdfQ.eyJ3biI6ICJNajlzb0JZVUNhU2Jmajc0TUxjWWhwaGZUUHM0OTlzTDFRZWF
    wR2VhRDlNPSIsICJuYmYiOiAxNjQ5OTE0NDE3LjU4OTU0NCwgImlhdCI6IDE2NDk5MTQ0MTcuNTg5NTQ
    0LCAiZXhwIjogMTY1MDAwMDgxNy41ODk1NDR9.MEQCIBqs9ifzol7F9a1sd4RoFL_DbP9D5CQip8BN8N
    v34EUrAiAysi0HyFkgMhRamYt58KeMFmFgd86aoAquwQnaQJX1cw 

    Im Body von (1) befindet sich:
    {
        "dp": "ARcMxZ3OgbrYWPmQqgBWYcvgs9wdUfxb1ei4AOGaZjkIGmE7cLOXvCyNIpouaC/4qXg1xjd4LtEvfyUWQy20aO4FY2folW0f987URLT1bWyI/8kLxdZN5C1YzwhPxRIT/fTyegyLcQ==",
        "exp": 1650000817.589544,
        "iat": 1649914417.589544,
        "nbf": 1649914417.589544,
        "vst_cert_hash": "Bmr35ND3w5keoK1QtUSK6ckD/u3tAaru6HnhF1M8V6s=",
        "wn": "Mj9soBYUCaSbfj74MLcYhphfTPs499sL1QeapGeaD9M="
    }

    Das signierte Tupel (s. o.) sende ich jetzt an die Vertrauensstelle.
    Response-Code: 201
    Ergebnis:
    {'status': 'ok'}

    Jetzt verschlüssele ich mein MIO für das FDZ und sende es an das FDZ inkl. AN
    Hex-Dump des Chiffrats was ich gleich auf http://127.0.0.1:20003/v1/epa/mio/50351ab26628ee7c4af6617e0ba677648ab879b4e1885ac86f516e69b41a6409 POST-te:
    012007350a04a9530cdcb0c96f99c6bf7a435acf000be7a971aca89bca30243a6686d156ff36
    0ada27db05ad03fe2c7c3d15ceb4902b08baecb7bba0fdca03f1ddab0d806f7018cdd7c273e63a59
    2276ff4b654dae8366a2fe66c8e6a60c1c923061f5cca030a45796600028422e8caf1ff1000740d7
    ad082e99e13d29bb2bfb4e3ea64ea4cb54120fa5b4f151ad90a3eb5929083d3b29805a7fda6795d7
    5d1cb491b2f20d00f8c0b31ca7a57b749700eb9fcaf2f110dfa7aa166b03b84fdac6bb5900d1e1
    Response-Code: 201
    Ergebnis:
    {'status': 'ok'}

    Jetzt widerrufe ich die Datenfreigabe wieder für das eben freigegebene MIO
    Response-Code: 202
    Ergebnis:
    {'status': 'ok'}

# License

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the
License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "
AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.
