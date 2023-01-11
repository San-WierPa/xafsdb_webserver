"""
@author: Sebastian Paripsa
"""

import scicat_py
import environ
env = environ.Env()
environ.Env.read_env()

USERNAME = env("USERNAME")
PASSWORD = env("PASSWORD")

CONFIGURATION = scicat_py.Configuration(
    host="http://scicat:3000",
)
