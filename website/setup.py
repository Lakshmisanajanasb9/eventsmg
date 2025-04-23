import os
import secrets
import shutil

def setup_environment():
    """Set up development environment."""
    if not os.path.exists('.env'):
        # Copy the example file
        shutil.copy('.env.example', '.env')
        
        # Generate a random secret key
        secret_key = secrets.token_hex(16)
        
        # Read and update the .env file
        with open('.env', 'r') as file:
            env_contents = file.read()
        
        # Replace the placeholder with an actual secret key
        env_contents = env_contents.replace('replace_with_your_secret_key', secret_key)
        
        with open('.env', 'w') as file:
            file.write(env_contents)
        
        print("Created .env file with a random SECRET_KEY")
        print("Please update other variables in .env with your actual credentials")
    else:
        print(".env file already exists")

if __name__ == "__main__":
    setup_environment()
