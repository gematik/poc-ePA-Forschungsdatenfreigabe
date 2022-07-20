# Vertrauensstelle: Erläuterungen zur Schnittstelle

Das FdV ist erfolgeich am AS eingeloggt.
Dann kann es für die Datenfreigabe ein vom AS erzeugte signiertes Tupel
(Auftragsnummer (AN) und Lieferpseudonym (LP)) erhalten.

Beispiel für ein signiertes Tupel

    eyJhbGciOiAiRVMyNTYiLCAieDVjIjogWyJNSUlDQWpDQ0Fha0NGRmUyTVRZVXJYMjhVN2FYSm9XemIr
    WEYzcTlyTUFvR0NDcUdTTTQ5QkFNQ01IQXhDekFKQmdOVkJBWVRBa1JGTVE4d0RRWURWUVFJREFaQ1pY
    SnNhVzR4RHpBTkJnTlZCQWNNQmtKbGNteHBiakVRTUE0R0ExVUVDZ3dIWjJWdFlYUnBhekVRTUE0R0Ex
    VUVDd3dIWjJWdFlYUnBhekViTUJrR0ExVUVBd3dTUzI5dGNHOXVaVzUwWlc0dFVFdEpMVU5CTUI0WERU
    SXlNRE13TVRFek5USXpPRm9YRFRJek1ETXdNVEV6TlRJek9Gb3dnWll4Q3pBSkJnTlZCQVlUQWtSRk1R
    OHdEUVlEVlFRSURBWkNaWEpzYVc0eER6QU5CZ05WQkFjTUJrSmxjbXhwYmpFWU1CWUdBMVVFQ2d3UFpW
    QkJJRUZyZEdWdWMzbHpkR1Z0TVNFd0h3WURWUVFMREJoTGIyMXdiMjVsYm5SbElFRjFkRzl5YVhOcFpY
    SjFibWN4S0RBbUJnTlZCQU1NSDJWUVFTMUJVeUJMYjIxd2IyNWxiblJsSUVGMWRHOXlhWE5wWlhKMWJt
    Y3dXakFVQmdjcWhrak9QUUlCQmdrckpBTURBZ2dCQVFjRFFnQUVraytOUDY4QWVVMXR6cis1UEFVZWtw
    WjNyTGtqU2h2ODhVSkpEQkFTSDh4emlYTU84TW1aU0p5SHZXRng0NlB4Rm80SU5CZmErcmh2dXBUTkhm
    bm9WakFLQmdncWhrak9QUVFEQWdOSEFEQkVBaUI5ZXpNMEtBckIwWU9XVi9YeGV6eDhYNTVtdi9ZN1Rl
    d2dxRUJSS0psV2xnSWdJckdZa1QvdStZWjdieStVOE5lVHAzN28xWkZRMkJ2NStLL3paZGlmQUFjPSJd
    fQ.eyJ3biI6ICIyMXVHNjhlUC9nbFRGbWt1ZTFiUG03c2s1MGd5aUtiVUZ6ck1vL0ErMWljPSIsICJkc
    CI6ICJBU3lpWHp4cHo5ajBkaWY2bVJUTGViczNXLzVNWkZPOHY5S2JFeDNLQjkvdmt2TW5XWGN6UHZyM
    Gl3MENmT3lLRkZjYkNRbG54cEQ5VjJBS2I2TE4zeUw0MnFUMkpDczdDWi9qV2NuejU0Y052aVdqbExhV
    m4zeDMvdjJUaVFPOXJETHdqQzQwRmc9PSIsICJ2c3RfY2VydF9oYXNoIjogIkJtcjM1TkQzdzVrZW9LM
    VF0VVNLNmNrRC91M3RBYXJ1NkhuaEYxTThWNnM9IiwgIm5iZiI6IDE2NTA4ODM3MDYuMTMxNzQ2LCAia
    WF0IjogMTY1MDg4MzcwNi4xMzE3NDYsICJleHAiOiAxNjUwOTcwMTA2LjEzMTc0Nn0.MEQCICcAwLE28
    5mRpv5HT8b3-hmVpD9JRyaPR4_n7YWoO4hyAiBGf1sEhMnPTTmegmgZmmKOBDV1EvEgo3OtGOK4mFgzh
    Q

    Im Body befindet sich:
    {
        "dp": "ASyiXzxpz9j0dif6mRTLebs3W/5MZFO8v9KbEx3KB9/vkvMnWXczPvr0iw0CfOyKFFcbCQlnxpD9V2AKb6LN3yL42qT2JCs7CZ/jWcnz54cNviWjlLaVn3x3/v2TiQO9rDLwjC40Fg==",
        "exp": 1650970106.131746,
        "iat": 1650883706.131746,
        "nbf": 1650883706.131746,
        "vst_cert_hash": "Bmr35ND3w5keoK1QtUSK6ckD/u3tAaru6HnhF1M8V6s=",
        "wn": "21uG68eP/glTFmkue1bPm7sk50gyiKbUFzrMo/A+1ic="
    }

Der `vst_cert_hash` ist der SHA-256 Hashwert des VST-Zertifiakts was das AS zur
Erzeugung des LP verwendet hat. Das AS kann dieses VST-Zertifikat vom VST über 
den Pfadnamen /v1/epa/certificate bezieehen.
Da Zertifikate ein Gültigkeitsdauer besitzen, kann das VST auch zwei aktuell
gültige Zertifikate besitzen (rollierendes Update). Mit dem Hashwert kann das
VST leichter erfahren, welches Zertifkat das AN verwendet hat.

Wie in der [OpenAPI-Spezifikation](../openapi/openapi-vst.yaml) dargestellt,
sendet der Client (ePA-FdV), per HTTP-POST das signierte Tupel an die VST 
mit der URL `/epa/signed_an_lp`. Im Gutfall erhält er den HTTP-Status-Code 201.

