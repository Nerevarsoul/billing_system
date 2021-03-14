from databases import Database

from app.settings import settings

if not settings.TESTING:
    database = Database(settings.DB_URL)
else:
    database = Database(settings.TEST_DB_URL, force_rollback=True)
