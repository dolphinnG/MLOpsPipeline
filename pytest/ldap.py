from ldap3 import Server, Connection, ALL, NTLM
import os
# Define the LDAP server and connection parameters
ldap_server = 'ldap://openldap-dolphin-service:389'
# ldap_server = 'ldap://127.1.1.6:389'

ldap_user = 'cn=topg,dc=dolphin,dc=lmao'  # Replace with your LDAP user DN
ldap_password = 'supahakka'  # Replace with your LDAP password

# Create the server object
server = Server(ldap_server, get_info=ALL)

# Create the connection object
conn = Connection(server, user=ldap_user, password=ldap_password, authentication='SIMPLE')
envs = {k:v for k,v in os.environ.items() if 'LDAP' in k}
# Bind to the server
try:
    if not conn.bind():
        print('Error in bind:', conn.result)
    else:
        print('Successfully connected to the LDAP server')
except Exception as e:
    print('Error in bind:', e)

# Unbind the connection
conn.unbind()