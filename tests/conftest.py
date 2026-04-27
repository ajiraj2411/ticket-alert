import os

def pytest_configure():
    os.environ.setdefault('DATABASE_URL_PUBLIC', 'sqlite:///:memory:')
    os.environ.setdefault('BOT_TOKEN', 'test_token')