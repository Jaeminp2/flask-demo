import os
from flask import Flask

# Set the secret key for our app
# Use an environment variable if available, otherwise use the development default.
SECRET_KEY = os.environ.get('SECRET_KEY', 'development-secret-key')

app = Flask(__name__)
app.secret_key = SECRET_KEY

if __name__ == '__main__':
    # NOTE: Set debug to True for development mode
    app.run(debug=True)
