"""
@author: s52748
@contact: s52748@beuth-hochschule.de
@version: 12.06.2016
@summary: Module, which contains the main script for starting the application
"""

# !/usr/bin/env python

from src.controller.app_controller import AppController
from src.model.dao import DAO

if __name__ == "__main__":
    DAO()  # Create database tables, if db does not exists
    AppController()  # Start program
