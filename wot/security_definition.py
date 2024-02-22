# No Security (nosec)
nosec = {
    "name": "no_sec",
    "body": {
        "scheme": "nosec"
    }
}
# Basic Authentication (basic)
basic = {
    "name": "basic_sc",
    "body": {
        "scheme": "basic",
        "in": "header"      # where the security information is provided
    }
}
# Digest Authentication (digest)
digest = {
    "name": "digest_sc",
    "body": {
        "scheme": "digest",
        "qop": "auth",
        "in": "header"
    }
}
# Bearer Token (bearer)
bearer = {
    "name": "bearer_sc",
    "body": {               # you might specify the token format (like JWT) and the algorithm used for signing
        "scheme": "bearer",
        "authorization": "https://example.com/auth",
        "alg": "ES256",
        "format": "jwt",
        "in": "header"
    }
}
# Public Key Infrastructure (psk)
psk = {
    "name": "psk_sc",
    "body": {
        "scheme": "psk"
    }
}
# Client Certificates (cert)
cert = {
    "name": "cert_sc",
    "body": {
        "scheme": "cert",
        "identity": "https://example.com/certificates"
    }
}
# API Key (apikey)
apikey = {
    "name": "apikey_sc",
    "body": {
        "scheme": "apikey",
        "in": "header",
        "name": "X-API-KEY"     # specifies the name of the header or query parameter that carries the API key
    }
}


# # OAuth 2.0 (oauth2)
# # OAuth2 Flows: For OAuth 2.0, different flow types can be used (e.g., code, implicit, password, clientCredentials), each suitable for different scenarios.
# oauth2 = {
#     "name": "oauth2_sc",
#     "body": {
#         "scheme": "oauth2",
#         "flow": "code",
#         "authorization": "https://example.com/authorize",
#         "token": "https://example.com/token",
#         "refresh": "https://example.com/refresh",
#         "scopes": ["read", "write"]
#     }
# }


every_security_option = [
    {
        "name": "no_sec",
        "body": {
            "scheme": "nosec"
            }
    }, 
    {
        "name": "basic_sc",
        "body": {
            "scheme": "basic",
            "in": "header"      # where the security information is provided
            }
    }, 
    {
        "name": "digest_sc",
        "body": {
            "scheme": "digest",
            "qop": "auth",
            "in": "header"
            }
    }, 
    {
        "name": "bearer_sc",
        "body": {               # you might specify the token format (like JWT) and the algorithm used for signing
            "scheme": "bearer",
            "authorization": "https://example.com/auth",
            "alg": "ES256",
            "format": "jwt",
            "in": "header"
            }
    },
    {
        "name": "psk_sc",
        "body": {
            "scheme": "psk"
            }
    }, 
    {
        "name": "cert_sc",
        "body": {
            "scheme": "cert",
            "identity": "https://example.com/certificates"
            }
    }, 
    {
        "name": "apikey_sc",
        "body": {
            "scheme": "apikey",
            "in": "header",
            "name": "X-API-KEY"     # specifies the name of the header or query parameter that carries the API key
            }
    }
]