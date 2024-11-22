# CA
openssl genpkey -algorithm RSA -out dolphin.rootCA.key -pkeyopt rsa_keygen_bits:2048
openssl req -x509 -new -nodes -key dolphin.rootCA.key -sha256 -days 3650 -out dolphin.rootCA.crt -config ca.cnf -extensions v3_ca




# Server. Just for reference, not used in the project. Cert-manager will generate the server certificate.
openssl genpkey -algorithm RSA -out openldap.key -pkeyopt rsa_keygen_bits:2048
openssl req -new -key openldap.key -out openldap.csr -config openldap.cnf -reqexts v3_req
openssl x509 -req -in openldap.csr -CA dolphin.rootCA.crt -CAkey dolphin.rootCA.key -CAcreateserial \ 
-out openldap.crt -days 365 -extensions v3_req -extfile openldap.cnf


# turn crt into jks 
# Convert the .crt and .key files into a PKCS12 file:
openssl pkcs12 -export -in dolphin.rootCA.crt -inkey dolphin.rootCA.key \ 
-out dolphin.p12 -name dolphin -CAfile dolphin.rootCA.crt -caname root 

# Import the PKCS12 file into a Java KeyStore (.jks):
keytool -importkeystore -deststorepass lmaohehe -destkeypass lmaohehe -destkeystore keystore.jks \ 
-srckeystore dolphin.p12 -srcstoretype PKCS12 -srcstorepass lmaohehe -alias dolphin

# Import the CA certificate into the truststore:
keytool -import -trustcacerts -file dolphin.rootCA.crt -alias root -keystore truststore.jks -storepass lmaohehe