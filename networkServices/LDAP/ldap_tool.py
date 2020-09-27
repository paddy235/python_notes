"""
需求分析：与LDAP服务器建立连接，并且查询公司所有的员工信息和部门信息
运行环境：python3 + Windows或者Linux
依赖库第三方库： ldap3
GitHub链接：
"""
from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, LEVEL, SUBTREE, ServerPool
import time
import json


AUTH_LDAP_SERVER_URI = ['ldap://bitmain-inc.com:389']
AUTH_LDAP_BIND_DM = '@bitmain-inc.com'
AUTH_LDAP_SEARCH_BASE = "dc=bitmain-inc,dc=com"
username = 'jian'
password = ''


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
            import traceback
            traceback.print_exc()
            return None

    def search_ldap(self, search_user):
        ldap_status = self.auth_ldap()
        search_result_dict = {}
        if ldap_status:
            res = self.ldap_conn.search(
                search_base=self.AUTH_LDAP_SEARCH_BASE,
                search_filter='(sAMAccountName={})'.format(search_user),
                search_scope=SUBTREE,
                attributes=self.attributes,
                paged_size=5
            )
            if res:
                try:
                    entry = self.ldap_conn.response[0]
                    dn = entry['dn'].split(',')
                    search_result_dict = entry['attributes']
                    search_result_dict['company'] = dn[3].lstrip('OU=')
                    search_result_dict['team'] = dn[1].lstrip('OU=')
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    ldap_status = False
        return ldap_status, search_result_dict

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

    def users_get(self):
        '''获取所有的用户'''
        search_filter = '(objectclass=user)'
        self.ldap_conn.search(search_base=AUTH_LDAP_SEARCH_BASE, search_filter=search_filter, attributes=ALL_ATTRIBUTES)
        res = self.ldap_conn.response_to_json()
        res = json.loads(res)['entries']
        return res

    def OU_get(self):
        '''获取所有的OU'''
        ou_search_filter = '(objectclass=organizationalUnit)'#只获取【OU】对象

        self.ldap_conn.search(search_base=self.AUTH_LDAP_SEARCH_BASE, search_filter=ou_search_filter,
                         attributes=ALL_ATTRIBUTES)
        res = self.ldap_conn.response_to_json()
        res = json.loads(res)['entries']
        return res


ldap = Ldap3Util.init_ldap(username, password)
if ldap.auth_ldap():
    users = ldap.users_get()
    with open("users.json", "w", encoding='utf-8') as f:
        f.write(json.dumps(users, indent=4, ensure_ascii=False))
    ous = ldap.OU_get()
    with open("ous.json","w", encoding='utf-8') as f:
        f.write(json.dumps(ous, indent=4, ensure_ascii=False))

    print('done')

