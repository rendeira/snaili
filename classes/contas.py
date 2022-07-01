import json
import os
import secrets
import string

from azure.identity import UsernamePasswordCredential
from msgraph.core import GraphClient

from classes.linguagem import lang

client: GraphClient
alphabet = string.ascii_letters + string.digits + "-*!@#$%><.,+"


def login():
    pass_credential = UsernamePasswordCredential(os.environ["ms-client-id"], os.environ["ms-admin-email"],
                                                 os.environ["ms-admin-pass"])
    global client
    client = GraphClient(credential=pass_credential)
    print(f"{lang['info-icon']} {lang['logged-as']} {get('/me')['userPrincipalName']}")


def random_password() -> string:
    return ''.join(secrets.choice(alphabet) for i in range(20))


def get_accounts() -> string:
    values = get('/users')
    str = ''
    for item in values['value']:
        str = str + "\n" + "- " + (item['displayName']).lower() + ";"
    return str


def get(cmd) -> json:
    result = client.get(cmd)
    return result.json()
