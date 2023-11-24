import secrets

def generate_api_key():
    return secrets.token_urlsafe(64)

print(generate_api_key())
