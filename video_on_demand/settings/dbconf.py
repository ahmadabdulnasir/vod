"""
This file contains different types of Database configuration that the project support and uses
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = os.path.dirname(BASE_DIR)

DEVELOPMENTDB = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(PROJECT_ROOT, "dev.db"),
    }
}


POSTGRESDB = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "voddb",
        "USER": "vod",
        "PASSWORD": "Pass@1234",
        "HOST": "localhost",
        "PORT": "",
    }
}

MSSQL = {
    "default": {
        "ENGINE": "sql_server.pyodbc",
        "NAME": "vodDB",
        "USER": "sa",
        "PASSWORD": "Pass@1234",
        "HOST": "127.0.0.1",
        "PORT": "1433",
        "OPTIONS": {"driver": "ODBC Driver 17 for SQL Server", "unicode_results": True},
    }
}

MANGODB = {
    "default": {
        "ENGINE": "djongo",
        "NAME": "voddb",
        "ENFORCE_SCHEMA": False,
        "CLIENT": {
            "host": "localhost",
            "port": 5984,
            "username": "vod",
            "password": "Pass@1234",
            # 'authSource': 'db-name',
            "authMechanism": "SCRAM-SHA-1",
        },
        "LOGGING": {
            "version": 1,
            "loggers": {"djongo": {"level": "DEBUG", "propagate": False}},
        },
    }
}

MYSQL = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "OPTIONS": {"read_default_file": "/path/to/my.cnf"},
    }
}
