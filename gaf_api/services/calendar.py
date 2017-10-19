from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient import discovery
from gaf_api.services import utils
from datetime import datetime, timedelta, timezone

creds = ServiceAccountCredentials.from_json_keyfile_dict(utils.load_config("google_keys.json"),
                                                         scopes=['https://www.googleapis.com/auth/calendar'])
service = discovery.build(
    "calendar", "v3",
    http=creds.authorize(Http()),
    cache_discovery=False
)


calendar_id = utils.load_config("calendar_id.json").get("id")


def get_days_events():
    """
    Returns the next 24 hours of events
    """
    start_time = datetime.now(tz=timezone.utc)
    end_time = start_time + timedelta(days=1)

    res = service.events().list(calendarId=calendar_id, timeMin=start_time.isoformat(), timeMax=end_time.isoformat())\
        .execute()

    events = []

    for e in res.get("items"):
        event = {
            "name": e.get("summary"),
            "id": e.get("id"),
            "channel": e.get("location"),
            "description": e.get("description"),
            "startTime": e.get("start").get("dateTime"),
            "endTime": e.get("end").get("dateTime")
        }

        events.append(event)

    return {"events": events}


def get_event(event_id: str):
    res = service.events().get(calendarId=calendar_id, eventId=event_id).execute()

    event = {
        "name": res.get("summary"),
        "id": res.get("id"),
        "channel": res.get("location"),
        "description": res.get("description"),
        "startTime": res.get("start").get("dateTime"),
        "endTime": res.get("end").get("dateTime")
    }

    return event
