import os

from dotenv import load_dotenv

load_dotenv()

WP_URL = os.getenv("WP_URL")
WP_API_BASE = os.getenv("WP_API_BASE")
WP_FULL_URL = WP_URL + WP_API_BASE
WP_USER = os.getenv("WP_USER")
WP_PASSWORD = os.getenv("WP_PASSWORD")

DB_CONFIG = {
    "host":os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "database":os.getenv("DB_DATABASE"),
    "user":os.getenv("DB_USER"),
    "password":os.getenv("DB_PASSWORD"),
}