from pyramid.view import view_config
from pyramid.request import Request
from gaf_api.services import calendar
from gaf_api.resources import Root


@view_config(route_name="v1:calendar/events", request_method="GET", context=Root)
def get_events(request: Request):
    """
    Returns the days events
    """
    return calendar.get_days_events()


@view_config(route_name="v1:calendar/event", request_method="GET", context=Root)
def get_event(request: Request):
    """
    Get's an event from an event ID
    """
    event_id = request.matchdict["event"]
    return calendar.get_event(event_id)


@view_config(route_name="v1:live", request_method="GET", context=Root)
def live_check(request: Request):
    """
    Checks if things are working fine
    """
    return {"API Live": True}
