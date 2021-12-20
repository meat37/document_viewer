from ldap3 import Server, Connection, SIMPLE, SYNC, ALL, SUBTREE
import config

server = Server(config.LDAP_SERVER, get_info=ALL)
# conn = Connection(server, "CN=XXXXX,OU=XXX;OU=XXXX,OU=Users,XX=People,XX=corp,XX=amdocs,XX=XXX", password=config.LDAP_PASS, auto_bind=False)
con = Connection(server, user=config.LDAP_USER, password=config.LDAP_PASS, auto_bind=True)
print(con.extend.standard.who_am_i())
con.search('DC=domain,DC=local', '(objectClass=person)')
print(con.entries)
