import os

from secrets.secrets import *

os.system(f'docker run --name discord-postgres -e POSTGRES_PASSWORD={db_password} -e POSTGRES_USER={db_username} -p 5432:5432 -d postgres')
