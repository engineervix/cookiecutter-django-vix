# -*- coding: utf-8 -*-

"""
Largely based on https://github.com/pydanny/cookiecutter-django/blob/master/hooks/post_gen_project.py

Does the following:

1. Generates and saves random secret key

    TODO: this might have to be moved to a pre_gen_hook

A portion of this code was adopted from Django's standard crypto functions and
utilities, specifically:
    https://github.com/django/django/blob/master/django/utils/crypto.py
"""

import os
import random
import shutil
import string

# Get the root project directory
PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

# Use the system PRNG if possible
try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False


def get_random_string(length=50):
    """
    Returns a securely generated random string.
    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    punctuation = string.punctuation.replace('"', '').replace("'", '')
    punctuation = punctuation.replace('\\', '')
    if using_sysrandom:
        return ''.join(random.choice(
            string.digits + string.ascii_letters + punctuation
        ) for i in range(length))

    print(
        "Cookiecutter-Django-Vix couldn't find a secure pseudo-random number generator on your system."
        " Please change your SECRET_KEY variables in the .env file"
        " manually."
    )
    return "CHANGEME!!"


def set_secret_key(config_file_location):
    # Open file
    with open(config_file_location) as f:
        file_ = f.read()

    # Generate a SECRET_KEY that matches the Django standard
    SECRET_KEY = get_random_string()

    # Replace "CHANGEME!!!" with SECRET_KEY
    file_ = file_.replace('CHANGEME!!!', SECRET_KEY, 1)

    # Write the results to file
    with open(config_file_location, 'w') as f:
        f.write(file_)


def make_secret_key(project_directory):
    """Generates and saves random secret key"""

    example_env_file = os.path.join(
        project_directory,
        'conf/env/env.example'
    )

    env_file = os.path.join(
        project_directory,
        'conf/env/.env'
    )

    shutil.copyfile(example_env_file, env_file)

    # .env file
    set_secret_key(env_file)

# Generates and saves random secret key
make_secret_key(PROJECT_DIRECTORY)

db_choice = '{{ cookiecutter.database }}'


def setup_db(config_file_location):
    # Open file
    with open(config_file_location) as f:
        file_ = f.read()

    if db_choice == "sqlite":
        DB_URL = "sqlite:///" + os.path.join(PROJECT_DIRECTORY, "conf/db/db.sqlite3")
        print("You have decided to use an SQLite Database, which may not be the best for production")
        print("Please change to Postgres before deployment")
    elif db_choice == "postgres":
        DB_URL = "postgres://user:password@host:port/database"
        print("Please manually setup your Postgres Database and add the connection details to the env file.")
    elif db_choice == "postgis":
        DB_URL = "postgis://user:password@host:port/database"
        print("Please manually setup your Postgis Database and add the connection details to the env file.")
    else:
        # default fallback: SQLite
        DB_URL = "sqlite:///" + os.path.join(PROJECT_DIRECTORY, "conf/db/db.sqlite3")

    # Replace "CHANGEME!!!" with SECRET_KEY
    file_ = file_.replace('CONFIGUREDB!!!', DB_URL, 1)

    # Write the results to file
    with open(config_file_location, 'w') as f:
        f.write(file_)


def make_db_config(project_directory):
    """Generates and saves random secret key"""

    env_file = os.path.join(
        project_directory,
        'conf/env/.env'
    )

    # env.example file
    setup_db(env_file)

make_db_config(PROJECT_DIRECTORY)

# make a copy of the local.example.py
shutil.copyfile(
    os.path.join(PROJECT_DIRECTORY, 'src/{{ cookiecutter.project_slug }}/settings/local.example.py'),
    os.path.join(PROJECT_DIRECTORY, 'src/{{ cookiecutter.project_slug }}/settings/local.py')
)
