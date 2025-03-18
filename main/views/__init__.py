from .medical_record_views import index, upload_report, get_report_analysis
from .chat_views import process_chat
from .emergency_views import (
    trigger_emergency,
    get_emergency_contacts,
    add_emergency_contact,
    delete_emergency_contact
) 