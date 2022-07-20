#! /usr/bin/env bash

openssl ecparam -name brainpoolP256r1 -genkey -out komponenten-pki-ca-key.pem

openssl req -x509 -key komponenten-pki-ca-key.pem \
    -outform pem \
    -out komponenten-pki-ca.pem -days 365 \
    -subj "/C=DE/ST=Berlin/L=Berlin/O=gematik/OU=gematik/CN=Komponenten-PKI-CA"

openssl ecparam -name brainpoolP256r1 -genkey -out vst-key.pem

openssl req -new -key vst-key.pem \
        -subj "/C=DE/ST=Berlin/L=Berlin/O=RKI/OU=RKI/CN=Vertrauensstelle Datenfreigabe ePA"\
        -out vst.csr -sha256

openssl x509 -req -in vst.csr -CA komponenten-pki-ca.pem -CAkey komponenten-pki-ca-key.pem\
        -CAcreateserial -out vst.pem -days 365 -sha256

openssl ecparam -name brainpoolP256r1 -genkey -out fdz-key.pem

openssl req -new -key fdz-key.pem \
        -subj "/C=DE/ST=Berlin/L=Berlin/O=Forschungsdatenzentrum/OU=Forschungsdatenzentrum/CN=Forschungsdatenzentrum Datenfreigabe ePA"\
        -out fdz.csr -sha256

openssl x509 -req -in fdz.csr -CA komponenten-pki-ca.pem -CAkey komponenten-pki-ca-key.pem\
        -CAcreateserial -out fdz.pem -days 365 -sha256

openssl ecparam -name brainpoolP256r1 -genkey -out as-key.pem

openssl req -new -key as-key.pem \
        -subj "/C=DE/ST=Berlin/L=Berlin/O=ePA Aktensystem/OU=Komponente Autorisierung/CN=ePA-AS Komponente Autorisierung"\
        -out as.csr -sha256

openssl x509 -req -in as.csr -CA komponenten-pki-ca.pem -CAkey komponenten-pki-ca-key.pem\
        -CAcreateserial -out as.pem -days 365 -sha256

