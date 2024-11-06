from ldap3 import Server, Connection, ALL, MODIFY_ADD

# LDAP server and admin credentials
ldap_server = 'ldap://127.0.0.1:389'
admin_dn = 'cn=topg,dc=dolphin,dc=lmao'
admin_password = 'supahakka'

# New user details
new_user_dn = 'uid=newuser,ou=ccc,dc=dolphin,dc=lmao'
new_user_attributes = {
    'objectClass': ['inetOrgPerson'],
    'cn': 'New User',
    'sn': 'User',
    'uid': 'newuser',
    'mail': 'newuser@dolphin.lmao',
    'userPassword': 'password123',
    'title': 'Software Developerbbb',
    'l': 'India',
    'telephoneNumber': '+1234567899'
}

# Group details
developer_group_dn = 'cn=Developers,ou=Groups,dc=dolphin,dc=lmao'

# Connect to the LDAP server
server = Server(ldap_server, get_info=ALL)
conn = Connection(server, admin_dn, admin_password, auto_bind=True)

# Add the new user
conn.add(new_user_dn, attributes=new_user_attributes)
if conn.result['description'] == 'success':
    print(f"Successfully added user: {new_user_dn}")
else:
    print(f"Failed to add user: {conn.result}")

# Add the new user to the Developers group
conn.modify(developer_group_dn, {'member': [(MODIFY_ADD, [new_user_dn])]})
if conn.result['description'] == 'success':
    print(f"Successfully added user to Developers group: {new_user_dn}")
else:
    print(f"Failed to add user to Developers group: {conn.result}")

# Unbind the connection
conn.unbind()