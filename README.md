# Forschungsdatenfreigabe elektronisch Patientenakte

Wie in [gemF\_ePA\_FDZ\_Anbindung](https://fachportal.gematik.de)
überblicksartig dargstellt, können bei Einwilligung der versicherten Person auf
dem ePA-Frontend des Versicherten (ePA-FdV) medizinische Daten zunächst
anonymisiert werden und diese dann mit Hilfe einer Vertrauensstelle (VST,
verantwortet vom RKI) pseudonymisiert werden. Diese pseudonymisierten
medizinischen Daten werden dann vom ePA-FdV an das Forschungsdatenzentrum (FDZ)
gesendet.

## Beispiel-Implementierung Schnittstellen

Vertrauensstelle: [vst.py](vst.py),
[Erläuterungen zur Schnittstelle](README-VST.md),
[VST-OpenAPI-Spezifikation (YAML)](openapi/openapi-vst.yaml).

Forschungsdatenzentrum: [fdz.py](vst.py),
[Erläuterungen zur Schnittstelle](README-FDZ.md),
[FDZ-OpenAPI-Spezifikation (YAML)](openapi/openapi-fdz.yaml). 

ePA Frontend des Versicherten: [epa-fdv.py](epa-fdv.py)

ePA Aktensystem: [as.py](as.py) (Notwendig für die Erzeugung der Auftragsnummer (AN), des Lieferpseudonyms (LP) und des Proxy-Tokens)

### Docker-Image

Eine lokale Instanz kann man auch leicht mit
dem [Dockerimage](https://hub.docker.com/r/gematik1/epa-forschungsdatenfreigabe-poc) starten

    docker pull gematik1/epa-forschungsdatenfreigabe-poc:1.1.0 
    docker run -it gematik1/epa-forschungsdatenfreigabe-poc:1.1.0 /bin/bash

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
    $> ./epa-fdv.py
    Beim AS (http://127.0.0.1:20001/datenfreigabe/token) (1) ein signiertes AN+LP-Tupel und  (2) eine signierte AN beziehen.

    Ergebnis: (1) eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsIng1YyI6WyJNSUlDQWpDQ0Fha0
    NGRmUyTVRZVXJYMjhVN2FYSm9XemIrWEYzcTlyTUFvR0NDcUdTTTQ5QkFNQ01IQXhDekFKQmdOVkJBWV
    RBa1JGTVE4d0RRWURWUVFJREFaQ1pYSnNhVzR4RHpBTkJnTlZCQWNNQmtKbGNteHBiakVRTUE0R0ExVU
    VDZ3dIWjJWdFlYUnBhekVRTUE0R0ExVUVDd3dIWjJWdFlYUnBhekViTUJrR0ExVUVBd3dTUzI5dGNHOX
    VaVzUwWlc0dFVFdEpMVU5CTUI0WERUSXlNRE13TVRFek5USXpPRm9YRFRJek1ETXdNVEV6TlRJek9Gb3
    dnWll4Q3pBSkJnTlZCQVlUQWtSRk1ROHdEUVlEVlFRSURBWkNaWEpzYVc0eER6QU5CZ05WQkFjTUJrSm
    xjbXhwYmpFWU1CWUdBMVVFQ2d3UFpWQkJJRUZyZEdWdWMzbHpkR1Z0TVNFd0h3WURWUVFMREJoTGIyMX
    diMjVsYm5SbElFRjFkRzl5YVhOcFpYSjFibWN4S0RBbUJnTlZCQU1NSDJWUVFTMUJVeUJMYjIxd2IyNW
    xiblJsSUVGMWRHOXlhWE5wWlhKMWJtY3dXakFVQmdjcWhrak9QUUlCQmdrckpBTURBZ2dCQVFjRFFnQU
    VraytOUDY4QWVVMXR6cis1UEFVZWtwWjNyTGtqU2h2ODhVSkpEQkFTSDh4emlYTU84TW1aU0p5SHZXRn
    g0NlB4Rm80SU5CZmErcmh2dXBUTkhmbm9WakFLQmdncWhrak9QUVFEQWdOSEFEQkVBaUI5ZXpNMEtBck
    IwWU9XVi9YeGV6eDhYNTVtdi9ZN1Rld2dxRUJSS0psV2xnSWdJckdZa1QvdStZWjdieStVOE5lVHAzN2
    8xWkZRMkJ2NStLL3paZGlmQUFjPSJdfQ.eyJ3biI6IkZYRkYwSW5rY3o4Q09CY3hiV1l5Y1Y0MDlERnZ
    pTUMxeldpUlgrYW5ObXM9IiwiZHAiOiJBVjljQmFMSVlHRmJuakdPK3kyMENUenBFeWNuSFpRaDQxL3l
    GRlVyNGhERkVjMjZiOGlFb3Ewd0g4UWFtbkdQRFZscm0vQUFoNFp3L1VMY2pWa3JobGoyaHhONkY2WGM
    4MzdCbDhVaHNUMXZyVTE4aHRBZXkzYWxZZVdLMld4QXpVVERubTBPaFE9PSIsImlhdCI6MTY2NjA4OTM
    2MC41MzcxOTYsImV4cCI6MTY2NjE3NTc2MC41MzcxOTYsImlzcyI6Imh0dHA6Ly9hdXRob3JpemF0aW9
    uLmFrdGVuc3lzdGVtLnRpIiwidnN0X2NlcnRfaGFzaCI6IkJtcjM1TkQzdzVrZW9LMVF0VVNLNmNrRC9
    1M3RBYXJ1NkhuaEYxTThWNnM9In0.WAKzoVGaIOGvZXde9J5SsBMC0VFPirLTcobAfFlYEhVXyWe2Uld
    -dA5RSbwZBrhYaRVCrWYW1UXVmRqW0rnklA

    Ergebnis: (2) eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsIng1YyI6WyJNSUlDQWpDQ0Fha0
    NGRmUyTVRZVXJYMjhVN2FYSm9XemIrWEYzcTlyTUFvR0NDcUdTTTQ5QkFNQ01IQXhDekFKQmdOVkJBWV
    RBa1JGTVE4d0RRWURWUVFJREFaQ1pYSnNhVzR4RHpBTkJnTlZCQWNNQmtKbGNteHBiakVRTUE0R0ExVU
    VDZ3dIWjJWdFlYUnBhekVRTUE0R0ExVUVDd3dIWjJWdFlYUnBhekViTUJrR0ExVUVBd3dTUzI5dGNHOX
    VaVzUwWlc0dFVFdEpMVU5CTUI0WERUSXlNRE13TVRFek5USXpPRm9YRFRJek1ETXdNVEV6TlRJek9Gb3
    dnWll4Q3pBSkJnTlZCQVlUQWtSRk1ROHdEUVlEVlFRSURBWkNaWEpzYVc0eER6QU5CZ05WQkFjTUJrSm
    xjbXhwYmpFWU1CWUdBMVVFQ2d3UFpWQkJJRUZyZEdWdWMzbHpkR1Z0TVNFd0h3WURWUVFMREJoTGIyMX
    diMjVsYm5SbElFRjFkRzl5YVhOcFpYSjFibWN4S0RBbUJnTlZCQU1NSDJWUVFTMUJVeUJMYjIxd2IyNW
    xiblJsSUVGMWRHOXlhWE5wWlhKMWJtY3dXakFVQmdjcWhrak9QUUlCQmdrckpBTURBZ2dCQVFjRFFnQU
    VraytOUDY4QWVVMXR6cis1UEFVZWtwWjNyTGtqU2h2ODhVSkpEQkFTSDh4emlYTU84TW1aU0p5SHZXRn
    g0NlB4Rm80SU5CZmErcmh2dXBUTkhmbm9WakFLQmdncWhrak9QUVFEQWdOSEFEQkVBaUI5ZXpNMEtBck
    IwWU9XVi9YeGV6eDhYNTVtdi9ZN1Rld2dxRUJSS0psV2xnSWdJckdZa1QvdStZWjdieStVOE5lVHAzN2
    8xWkZRMkJ2NStLL3paZGlmQUFjPSJdfQ.eyJ3biI6IkZYRkYwSW5rY3o4Q09CY3hiV1l5Y1Y0MDlERnZ
    pTUMxeldpUlgrYW5ObXM9IiwiaWF0IjoxNjY2MDg5MzYwLjUzNzE5NiwiZXhwIjoxNjY2MTc1NzYwLjU
    zNzE5NiwiaXNzIjoiaHR0cDovL2F1dGhvcml6YXRpb24uYWt0ZW5zeXN0ZW0udGkifQ.i52vCa5m_T5y
    oHWqFdR8T-U5T5MUo9HweHr50Ah8Lcx-iy9zsw-128N78x6b7qUQApTNg3CZNiOtpqbWDb7VOQ 

    Im Body von (1) befindet sich:
    {
        "dp": "AV9cBaLIYGFbnjGO+y20CTzpEycnHZQh41/yFFUr4hDFEc26b8iEoq0wH8QamnGPDVlrm/AAh4Zw/ULcjVkrhlj2hxN6F6Xc837Bl8UhsT1vrU18htAey3alYeWK2WxAzUTDnm0OhQ==",
        "exp": 1666175760.537196,
        "iat": 1666089360.537196,
        "iss": "http://authorization.aktensystem.ti",
        "vst_cert_hash": "Bmr35ND3w5keoK1QtUSK6ckD/u3tAaru6HnhF1M8V6s=",
        "wn": "FXFF0Inkcz8COBcxbWYycV409DFviMC1zWiRX+anNms="
    }

    Das signierte Tupel (s. o.) sende ich jetzt an die Vertrauensstelle.
    Response-Code: 201
    Ergebnis:
    {'status': 'ok'}

    Jetzt verschlüssele ich mein MIO für das FDZ und sende es an das FDZ inkl. AN
    Hex-Dump des Chiffrats was ich gleich auf http://127.0.0.1:20003/v1/epa/mio/55682e888191984f833627c09893a1e4807bcd18ad83ba60c2ecc18312b9e257 POST-te:
    01628758dc762332804a54d91382e9115bf4549d14b7fea750b4cd318ee29555a800040016a4
    22b03d85d7d53859b54eeed07b005e0b732f2a9d61c2973590c2768c540bb9c5318df66095485dcd
    eb1807bc934b45fd063e155d44ee049a27f9b7a0c414b7b6c598e4eb1789829a0b4d068df030d0fb
    547c33d29453313974585cf3c5ac87eafc18337a07bfd5ebd7fe685868378bb1e9b155d42e2acc93
    1261d1e55dcfe0c46c8cb8550bd7e6641d00f6094683d3a49c21a0be40828e271bbd46f020ec9e

    Response-Code: 201
    Ergebnis:
    {'status': 'ok'}

    Jetzt widerrufe ich die Datenfreigabe wieder für das eben freigegebene MIO
    Response-Code: 202
    Ergebnis:
    {'status': 'ok'}

    Jetzt widerrufe ich als Test viele MIOs auf einmal
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
