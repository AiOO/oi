import os

path = os.path.dirname(os.path.abspath(__file__))
# Set this string for your database.
db_string = 'sqlite:///%s/secret.db' % path

