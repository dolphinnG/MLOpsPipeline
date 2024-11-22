# CA
openssl genpkey -algorithm RSA -out dolphin.rootCA.key -pkeyopt rsa_keygen_bits:2048
openssl req -x509 -new -nodes -key dolphin.rootCA.key -sha256 -days 3650 -out dolphin.rootCA.crt -config ca.cnf -extensions v3_ca




# Server. Just for reference, not used in the project. Cert-manager will generate the server certificate.
# openssl genpkey -algorithm RSA -out my-org-new.key -pkeyopt rsa_keygen_bits:2048
# openssl req -new -key my-org-new.key -out my-org-new.csr -config dolphin.cnf -reqexts v3_req
# openssl x509 -req -in my-org-new.csr -CA my-org.com.crt -CAkey my-org.com.key -CAcreateserial \ 
# -out my-org-new.crt -days 365 -extensions v3_req -extfile dolphin.cnf