import logging
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from .config import SCOPES, SERVICE_ACCOUNT_FILE

logger = logging.getLogger(__name__)


def get_authenticated_service(service_name='sheets', version='v4'):
    """Get authenticated Google API service using a GCP service account."""
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build(service_name, version, credentials=creds)
    logger.info(f"Authenticated service account: {service_name} v{version}")
    return service
