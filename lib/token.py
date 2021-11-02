from datetime import datetime, timedelta

import jwt

from reader.arg import ArgReader


def create_token():
    now = datetime.now()
    exp = now + timedelta(minutes=10)
    payload = {
        'iat': now.timestamp(),
        'exp': exp.timestamp(),
        'nbf': now.timestamp()
    }
    token = jwt.encode(payload, ArgReader.db.auth_secret_key)
    return f'{ArgReader.db.auth_header_prefix} {token}'
