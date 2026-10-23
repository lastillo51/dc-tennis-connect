from urllib.parse import urlencode

from app.api.schemas.court import CourtLocation


def build_google_maps_url(location: CourtLocation) -> str:
    if location.latitude is not None and location.longitude is not None:
        destination = f"{location.latitude},{location.longitude}"
    else:
        destination = location.address

    query = urlencode(
        {
            "api": "1",
            "destination": destination,
        }
    )

    return f"https://www.google.com/maps/dir/?{query}"