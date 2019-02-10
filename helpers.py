import datetime

# Make date readable by all
date_handler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, (datetime.datetime, datetime.date))
    else None
)

default_json_response = {
    'success': False, 
    'payload': []
}