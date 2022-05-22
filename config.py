import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://vjfdxyrk:sEJAp9eqEXryY-IhhWF9Ncmfl5XJVf8_@tyke.db.elephantsql.com/vjfdxyrk'
