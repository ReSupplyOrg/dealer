$ENV:SECRET_KEY = "development-secret";

# Postgres
$ENV:POSTGRES_DATABASE = "dealer";
$ENV:POSTGRES_USERNAME = "dealer";
$ENV:POSTGRES_PASSWORD = "dealer";
$ENV:POSTGRES_HOST = "127.0.0.1";
$ENV:POSTGRES_PORT = "5432";

# Redis
$ENV:REDIS_LEADER = "redis://127.0.0.1:6379"

# Start dealer
python backend/manage.py migrate
python backend/manage.py runserver