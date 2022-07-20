# Beispieldurchlauf


    $ ./hmac-sicherung-vst-fdz.py
    Die VST hat folgende Informationen als Tupel zusammengebracht:
    {
        "exp": 1647520324.473555,
        "iat": 1647433924.473555,
        "nbf": 1647433924.473555,
        "pp": "perioden\u00fcbergreifendes Pseudonym f\u00fcr KVNR A123456789",
        "transaktions_id": "75e45614428e950cc114e72e66e9b642205fcdaafc13fc04ed9045b02255688e",
        "wn": "64c5c37d472f0c0a60eb5f27d63b2caa63196cde855e7617daa9df0320a3efbd"
    }

    Mit einem gemeinsamen Geheimnis zwischen VST und FDZ wird das Tupel über
    HMAC (RFC-2104) integritäts- und authentitätsgesichert und anschließend
    gemäß RFC-7515 (JSON Web Signature) kodiert:

    eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYmYiOjE2NDc0MzM5MjQuNDczNTU1LCJpYXQiOjE2NDc0MzM5MjQuNDczNTU1LCJleHAiOjE2NDc1MjAzMjQuNDczNTU1LCJ0cmFuc2FrdGlvbnNfaWQiOiI3NWU0NTYxNDQyOGU5NTBjYzExNGU3MmU2NmU5YjY0MjIwNWZjZGFhZmMxM2ZjMDRlZDkwNDViMDIyNTU2ODhlIiwid24iOiI2NGM1YzM3ZDQ3MmYwYzBhNjBlYjVmMjdkNjNiMmNhYTYzMTk2Y2RlODU1ZTc2MTdkYWE5ZGYwMzIwYTNlZmJkIiwicHAiOiJwZXJpb2Rlblx1MDBmY2JlcmdyZWlmZW5kZXMgUHNldWRvbnltIGZcdTAwZmNyIEtWTlIgQTEyMzQ1Njc4OSJ9.NHKLI7UyzPTQyCYMi-FM9xWMzPmUx-ymbRCmCoPdfL4 

    Das wird vom FDZ geprüft (HMAC-Sicherung, Grundlage gemeinsames Geheimnis):
    Nach Prüfung kann das FDZ auf folgende Daten zugreifen:
    {
        "exp": 1647520324.473555,
        "iat": 1647433924.473555,
        "nbf": 1647433924.473555,
        "pp": "perioden\u00fcbergreifendes Pseudonym f\u00fcr KVNR A123456789",
        "transaktions_id": "75e45614428e950cc114e72e66e9b642205fcdaafc13fc04ed9045b02255688e",
        "wn": "64c5c37d472f0c0a60eb5f27d63b2caa63196cde855e7617daa9df0320a3efbd"
    }
