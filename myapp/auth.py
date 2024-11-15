import webbrowser
import requests
from urllib.parse import urlparse, parse_qs
import time
import secrets
import json
import os

# Your MyAnimeList credentials and settings
client_id = "your-key"  # Replace with your actual Client ID
client_secret = 'your-key'  # Replace with your actual Client Secret
redirect_uri = "http://localhost:5000/callback"

# Token URL and Authorization URL
auth_url = "https://myanimelist.net/v1/oauth2/authorize"
token_url = "https://myanimelist.net/v1/oauth2/token"

# Path to store tokens
TOKEN_FILE = 'tokens.json'

def get_new_code_verifier() -> str:
    """Generate a code verifier for OAuth flow."""
    token = secrets.token_urlsafe(100)
    return token[:128]

def load_tokens() -> dict:
    """Load tokens from the file, if they exist."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_tokens(tokens: dict):
    """Save tokens to a file."""
    with open(TOKEN_FILE, 'w') as file:
        json.dump(tokens, file)

def refresh_access_token(refresh_token: str) -> str:
    """Refresh the access token using the refresh token."""
    data = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("Error refreshing access token:", response.status_code, response.text)
        return None

def authorize():
    """Handle the OAuth 2.0 authorization code flow."""
    code_verifier = get_new_code_verifier()
    code_challenge = code_verifier  # For simplicity, using the same as code verifier (no hashing here)
    
    authorization_url = (
        f"{auth_url}?response_type=code&client_id={client_id}&code_challenge={code_challenge}"
    )
    
    # Open the browser for user login
    webbrowser.open(authorization_url)
    
    # Wait for the user to paste the redirected URL
    time.sleep(5)
    redirected_url = input("After authorization, paste the redirected URL here: ")

    # Extract the authorization code from the URL
    parsed_url = urlparse(redirected_url)
    auth_code = parse_qs(parsed_url.query)['code'][0]
    
    # Exchange the authorization code for an access token
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": auth_code,
        "code_verifier": code_verifier,
        "grant_type": "authorization_code",
    }
    
    response = requests.post(token_url, data=data)
    
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]
        
        # Save the tokens for future use
        save_tokens({
            "access_token": access_token,
            "refresh_token": refresh_token
        })
        print(f"Access Token: {access_token}")
        return access_token
    else:
        print("Error exchanging authorization code for access token:", response.status_code, response.text)
        return None

def get_access_token():
    """Get the access token, refreshing it if necessary."""
    tokens = load_tokens()
    if tokens:
        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")
        
        if access_token:
            # In this example, we assume the token has expired after an hour.
            # Check expiration logic (e.g. timestamp comparison) here for more advanced handling.
            # If expired, refresh the token
            print("Access Token is being refreshed...")
            access_token = refresh_access_token(refresh_token)
            if access_token:
                tokens["access_token"] = access_token  # Update the access token
                save_tokens(tokens)  # Save the updated tokens
                return access_token
        else:
            print("No access token found, authorizing again...")
            return authorize()
    else:
        print("No tokens found, authorizing...")
        return authorize()



