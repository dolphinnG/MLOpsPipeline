from ldap3 import Server, Connection, ALL, MODIFY_ADD, MODIFY_REPLACE, MODIFY_DELETE
from services.interfaces.IUserService import IUserService
from models.userModel import UserCreate, UserUpdate
from utils import constants, utils


class LDAPService(IUserService):

    def __init__(self, ldap_server, admin_dn, admin_password):
        self.ldap_server = ldap_server
        self.admin_dn = admin_dn
        self.admin_password = admin_password
        self.server = Server(self.ldap_server, get_info=ALL)

    def create_conn(self):
        return LDAPService.LDAPConn(self.server, self.admin_dn, self.admin_password)

    # async def __aenter__(self):
    #     self.conn = Connection(
    #         self.server, self.admin_dn, self.admin_password, auto_bind=True
    #     )
    #     return self

    # async def __aexit__(self, exc_type, exc_value, traceback):
    #     self.conn.unbind()

    class LDAPConn:
        def __init__(self, server, admin_dn, admin_password):
            self.conn = Connection(server, admin_dn, admin_password, auto_bind=True)

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_value, traceback):
            self.conn.unbind()

        async def add_user(self, user: UserCreate):
            user_dn = f"uid={user.uid},{constants.LDAP_USERS_BASE_DN}"
            user_attributes = user.model_dump()
            self.conn.add(user_dn, attributes=user_attributes)
            return self.conn.result

        async def update_user(self, user_dn: str, user: UserUpdate):
            user_dn = f"uid={user_dn},{constants.LDAP_USERS_BASE_DN}"
            changes = {
                key: (MODIFY_REPLACE, [value])
                for key, value in user.model_dump().items()
                if value is not None
            }
            self.conn.modify(user_dn, changes)
            return self.conn.result

        async def delete_user(self, user_dn: str):
            user_dn = f"uid={user_dn},{constants.LDAP_USERS_BASE_DN}"
            self.conn.delete(user_dn)
            return self.conn.result

        async def add_user_to_group(self, user_dn: str, group_dn: str):
            user_dn = f"uid={user_dn},{constants.LDAP_USERS_BASE_DN}"
            group_dn = f"cn={group_dn},{constants.LDAP_USERS_BASE_DN}"
            self.conn.modify(group_dn, {"member": [(MODIFY_ADD, [user_dn])]})
            return self.conn.result

        async def remove_user_from_group(self, user_dn: str, group_dn: str):
            self.conn.modify(group_dn, {"member": [(MODIFY_DELETE, [user_dn])]})
            return self.conn.result

        async def get_users(self, user_dn: str = constants.LDAP_USERS_BASE_DN):
            if user_dn != constants.LDAP_USERS_BASE_DN:
                user_dn = f"uid={user_dn},{constants.LDAP_USERS_BASE_DN}"
            self.conn.search(user_dn, "(objectClass=inetOrgPerson)", attributes=["*"])
            # res = [utils.ldap_entry_to_dict(entry) for entry in self.conn.entries]
            user_entries_with_group = [(entry, []) for entry in self.conn.entries]
            group_entries = await self._get_all_groups()

            for user_entry in user_entries_with_group:
                entry = user_entry[0]
                related_groups = user_entry[1]
                for group_entry in group_entries:
                    if entry.entry_dn in group_entry.member.values:
                        related_groups.append(group_entry.cn.value)

            res = [
                utils.ldap_entry_to_dict(entry_with_group)
                for entry_with_group in user_entries_with_group
            ]

            return res

        async def _get_all_groups(self):
            self.conn.search(
                constants.LDAP_GROUPS_BASE_DN,
                "(objectClass=groupOfNames)",
                attributes=["*"],
            )
            return self.conn.entries

        async def get_all_groups(self):
            group_entries = await self._get_all_groups()
            res = [entry.cn.value for entry in group_entries]
            return res
