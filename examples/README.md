# Beispiel Lieferpseudonym-Erzegung:

Im Beispiel erzeuge ich zwei Mal für KVNR = "A123456789" ein Lieferpseudonym.

Da ein
[IND-CCA2](https://de.wikipedia.org/wiki/Ciphertext_Indistinguishability#IND-CCA)-sicheres
Verschlüsselungsverfahren verwendet wird (vgl. Pseudonymisierungskonzept) ist
das Lieferpseudonym bei jeder Erzeugung -- obwohl die KVNR im Beispiel konstant
ist -- ein anderes.

Beispiel-Durchlauf:

    $ ./lieferpseudonym.py
    >>> Das Aktensystem erzeugt das LP (was dann als signierte AN+LP Tupel an das FdZ->VST geht).
    Hexdump des Lieferpseudonym ist: 016d88d0b9f6a8e563275013a264aa490a06a12fa6a1878
    be1053885127cc5703c95a4ba7773db56ae842f35eacf11853d512e22189357e4b127e7da00cd54b
    f98cc58acb4bbfd7f3455b827f7fcf5db1871f5cb6454180e5ad11d5d30bd1fbaecd9960d4fc993 

    Hexdump des Lieferpseudonym ist: 0189905f61ee4b1e54bd43858f9b550fe5a234a337452e8
    e57451bf80293c0991794a88eec515a8ce8d8ef216df56340d23310ba62f04c65994fa636e7d0f7b
    d36f691411adf51edf08726037ea4c61bc06d5bc1f57d1d0837ed1f1aad962c36f02449214f8da7 

    >>> Als VST kenne ich den privaten Schlüssel
    Depseudonymisierung: KVNR=A123456789


# Beispiel Erzeugung Lieferpseudonym + Auftragsnummer + Signatur im Aktensystem

Wenn ein FdV erfolgeich am AS eingeloggt ist (d. h. insbesondere die
Nutzerauthentifizierung hat erfolgreich stattgefunden), dann kann es sich für
die Forschungsfreigabe ein vom AS erzeugte signiertes Tupel (Auftragsnummer
(AN) und Lieferpseudonym (LP)) abholen.
Das AS erzeugt AN und LP und bindet anschließend die beiden Werte durch eine
umhüllende Signatur an einander.

Durch die Prüfung in der VST kann die VST sich sicher sein, dass sich nicht 
jemand beliebige Lieferpseudonyme für KVNR=1, ..., 10^10 ausgedacht hat.
Das AS bestätigt mit der Signatur die korrekte Erzeugung des LP.

Die Erzeugung des LP und der AN plus JSON-Web-Signature 
[RFC-7515](https://datatracker.ietf.org/doc/html/rfc7515)
durch das AS im Beispiel:


	./signed_as_lp.py
	eyJhbGciOiAiRVMyNTYiLCAieDVjIjogWyJNSUlDQWpDQ0Fha0NGRmUyTVRZVXJYMjhVN2FY
	Sm9XemIrWEYzcTlyTUFvR0NDcUdTTTQ5QkFNQ01IQXhDekFKQmdOVkJBWVRBa1JGTVE4d0RRWURWUVFJ
	REFaQ1pYSnNhVzR4RHpBTkJnTlZCQWNNQmtKbGNteHBiakVRTUE0R0ExVUVDZ3dIWjJWdFlYUnBhekVR
	TUE0R0ExVUVDd3dIWjJWdFlYUnBhekViTUJrR0ExVUVBd3dTUzI5dGNHOXVaVzUwWlc0dFVFdEpMVU5C
	TUI0WERUSXlNRE13TVRFek5USXpPRm9YRFRJek1ETXdNVEV6TlRJek9Gb3dnWll4Q3pBSkJnTlZCQVlU
	QWtSRk1ROHdEUVlEVlFRSURBWkNaWEpzYVc0eER6QU5CZ05WQkFjTUJrSmxjbXhwYmpFWU1CWUdBMVVF
	Q2d3UFpWQkJJRUZyZEdWdWMzbHpkR1Z0TVNFd0h3WURWUVFMREJoTGIyMXdiMjVsYm5SbElFRjFkRzl5
	YVhOcFpYSjFibWN4S0RBbUJnTlZCQU1NSDJWUVFTMUJVeUJMYjIxd2IyNWxiblJsSUVGMWRHOXlhWE5w
	WlhKMWJtY3dXakFVQmdjcWhrak9QUUlCQmdrckpBTURBZ2dCQVFjRFFnQUVraytOUDY4QWVVMXR6cis1
	UEFVZWtwWjNyTGtqU2h2ODhVSkpEQkFTSDh4emlYTU84TW1aU0p5SHZXRng0NlB4Rm80SU5CZmErcmh2
	dXBUTkhmbm9WakFLQmdncWhrak9QUVFEQWdOSEFEQkVBaUI5ZXpNMEtBckIwWU9XVi9YeGV6eDhYNTVt
	di9ZN1Rld2dxRUJSS0psV2xnSWdJckdZa1QvdStZWjdieStVOE5lVHAzN28xWkZRMkJ2NStLL3paZGlm
	QUFjPSJdfQ==.eyJhbiI6ICJlQk9abkx5ekNtOEp2ZDhjUTZ6a2hLUHVxZGVBQUN1VFc4OHdmRG5vd2V
	ZPSIsICJscCI6ICJBWXJiM0dWcUZuaHRqSStFd3VZaHMyc0NSM2NlLzg0UU9mTkhzQVdzcnJNVW1sR2J
	GMllqMWhCb3NxYldpMzNvcEkxbFkveGlCNCtZNlFWbTdKSlBzUExScnlLbVc0dHVseCtFaW9BeC9BZFZ
	5MEVRYjhDZjRkWTg3UFc4ZVlXYzQxSnY0UGVvSXc9PSIsICJ2c3RfY2VydF9oYXNoIjogIkJtcjM1TkQ
	zdzVrZW9LMVF0VVNLNmNrRC91M3RBYXJ1NkhuaEYxTThWNnM9IiwgIm5iZiI6ICIyMDIyLTAzLTEwVDE
	5OjU5OjExLjIyNjUwMyIsICJpYXQiOiAiMjAyMi0wMy0xMFQxOTo1OToxMS4yMjY1MDMiLCAiZXhwIjo
	gIjIwMjItMDMtMTBUMjA6NTk6MTEuMjI2NTAzIiwgIm9jc3AiOiAiLi4uIG9jc3AtcmVzcG9uc2UgLi4
	uIn0=.MEMCH137AjQXsyfrwi9We7t5nzQTqLNxE6YZTM2ZCJox6fMCIBy5I2CbjhhXhGSJLq1GXokjXs
	QEWt2iWl6sOPOKiJyO

Das kann man bspw. auf [jwt.io](https://jwt.io/) in die "Encoded Paste a Token here" 
Eingabefläche kopieren und kann dann den Inhalt ansehen.

# Beispiel FDZ-Encryption


	$ ./fdz-enc.py
	plaintext='Ich in ein anonymisiertes medizinische Datenobjekt oder ein VST-JWT.'
	INFO: fdz_x=0x17b08f214ef66568016350d0d26766c4271ee12a48b7191b7bb857abd8ea3d31 
              fdz_y=0x40f30ac680ffb8192007fac0ca71f92fe06225b1a2527eb61d6ded9e31f4be30
	INFO: d= 0x6f9a1583c255c3fb4a20c1e8a645fadb28ad14856c39d9208fafb6fbee411c7c
	INFO: x=0x62594c6c12a777ca8f474acf4b8d1411ffa1bd55c52166680b313e73899223d8 
              y=0x6cd330cea879ca5283ec4a4efcc10d233ff7c816326236e36b60de399e867f9c
	INFO: b'4e7d542eb11459c2de2d0e110c05ea7dd4606f1c65283c637bed88d386788099'
	INFO: b'c466748cedc914a8c258d932b2a87b6b2619f3568eea8a4db04048cf25aec172'
	INFO: b'96033cd56d03f880a10ece8e'
	hexdump der chiffrats: 0162594c6c12a777ca8f474acf4b8d1411ffa1bd55c521666
	80b313e73899223d86cd330cea879ca5283ec4a4efcc10d233ff7c816326236e36b60de399e867f9
	c96033cd56d03f880a10ece8e80391384275349125475bf3df43611d32a4fdebb0fb29f8da2488dd
	b455bd640047eaa0ad9436d3987f7fb9b9aee59589fdddffd96ade969f51b5789f5ce8fdf6b4d777
        e21e93a8a2e7bcc9cda269247093cc56c
	INFO: FDZ-private-key 0x78afc92233446435f0500c99130a03a8da61e7a78c4ae2afb4ea08cefd628848



