import os
from dotenv import load_dotenv

load_dotenv()

"""Валидные данные"""
valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')
driver_path = os.getenv('driver_path')
