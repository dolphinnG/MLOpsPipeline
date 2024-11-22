#!/bin/bash

# bin/kc.[sh|bat] export [--dir|--file] <path> --realm my-realm


/opt/bitnami/keycloak/bin/kc.sh import --file /realms/realm.json

# ldapsearch -H ldap://localhost -D "cn=topg,dc=dolphin,dc=lmao" -w supahakka -b "dc=dolphin,dc=lmao" "(objectClass=inetOrgPerson)"