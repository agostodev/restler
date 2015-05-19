import os.path

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = ("test",)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "TEST_NAME": "test_db",
    },
}
