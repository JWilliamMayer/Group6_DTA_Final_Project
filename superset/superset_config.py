# Superset Configuration

# Database connection settings
SQLALCHEMY_DATABASE_URI = "postgresql://airflow:airflow@postgres:5432/airflow"

# Flask-AppBuilder settings
SECRET_KEY = "thisISaSECRET_1234"

# Superset specific settings
ROW_LIMIT = 5000  # Maximum number of rows returned from SQL queries
SUPERSET_WEBSERVER_TIMEOUT = 300  # Webserver timeout in seconds
SUPERSET_WEBSERVER_PORT = 8088  # Port for the web server

# Email configuration
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_STARTTLS = True
SMTP_SSL = False
SMTP_USER = "youremail@gmail.com"
SMTP_PASSWORD = "yourpassword"
SMTP_MAIL_FROM = "youremail@gmail.com"

# Feature flags
FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
    "DASHBOARD_CACHE": True,
    "DASHBOARD_NATIVE_FILTERS": True,
    "ALERT_REPORTS": True,
    "DASHBOARD_CROSS_FILTERS": True,
    "DASHBOARD_NATIVE_FILTERS_SET": True,
    "ENABLE_JAVASCRIPT_CONTROLS": True,
}

# Cache configuration
CACHE_CONFIG = {
    "CACHE_TYPE": "redis",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": "redis",
    "CACHE_REDIS_PORT": 6379,
    "CACHE_REDIS_DB": 1,
    "CACHE_REDIS_URL": "redis://redis:6379/1",
}

# Additional database connections
ADDITIONAL_DATABASES = {
    "postgres_dta": {
        "sqlalchemy_uri": "postgresql://airflow:airflow@postgres:5432/airflow",
        "connect_args": {},
    }
}

# Default database connections to display in the UI
DATA_SOURCES = ["postgres_dta"]

# Dashboard settings
DASHBOARD_POSITIONS_AUTO_SAVE = True  # Auto-save dashboard layout changes
ENABLE_DASHBOARD_EMBEDS = True  # Allow dashboards to be embedded in other sites

# Query settings
QUERY_SEARCH_LIMIT = 1000  # Maximum number of queries to display on the search page
SQL_MAX_ROW = 100000  # Maximum number of rows returned from SQL Lab queries
SQL_QUERY_COST_ESTIMATE_TIMEOUT = 10  # Timeout for cost estimation (in seconds)

# Security settings
AUTH_TYPE = "db"  # Type of authentication
AUTH_USER_REGISTRATION = True  # Allow users to register
AUTH_USER_REGISTRATION_ROLE = "Public"  # Default role for new users
PREVENT_UNSAFE_DB_CONNECTIONS = True  # Prevent unsafe database connections

# Visualization settings
VIZ_TYPE_BLACKLIST = []  # Visualization types to disable
DEFAULT_VIZ_TYPE = "table"  # Default visualization type

# Internationalization
BABEL_DEFAULT_LOCALE = "en"  # Default locale
LANGUAGES = {
    "en": {"flag": "us", "name": "English"},
    "es": {"flag": "es", "name": "Spanish"},
    "fr": {"flag": "fr", "name": "French"},
}

# Theming options
THEME_OVERRIDES = {
    "borderRadius": 4,
    "colors": {
        "primary": {
            "base": "#4A57A9",
        },
        "secondary": {
            "base": "#E04355",
        },
        "grayscale": {
            "base": "#666666",
        },
    },
    "typography": {
        "families": {
            "sansSerif": "'Roboto', 'Helvetica Neue', Helvetica, Arial, sans-serif",
            "monospace": "'Roboto Mono', 'Courier New', monospace",
        },
        "weights": {
            "normal": 400,
            "bold": 700,
        },
    },
}

# Custom visualization plugins
CUSTOM_PLUGINS = {}

# Dashboard template processor
DASHBOARD_TEMPLATE_PARAMS = {}

# Extension loading
ADDITIONAL_MODULE_DS_MAP = {}