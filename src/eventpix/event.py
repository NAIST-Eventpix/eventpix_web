import datetime
from typing import TypeAlias

from icalendar.prop import vDDDTypes, vText  # type: ignore[import-untyped]

Datetime: TypeAlias = datetime.datetime | datetime.date | None


class Event:
    def __init__(
        self,
        dtstart: vDDDTypes,
        dtend: vDDDTypes,
        summary: vText,
        description: vText,
        location: vText,
    ):
        self._dtstart = self._vddd2datetime(dtstart)
        self._dtend = self._vddd2datetime(dtend)
        self._summary: str = self._vtext2str(summary)
        self._description: str = self._vtext2str(description)
        self._location: str = self._vtext2str(location)
        self.google_calendar_url = self.generate_google_calendar_url()

    @property
    def dtstart(self) -> Datetime:
        return self._dtstart

    @property
    def dtend(self) -> Datetime:
        return self._dtend

    @property
    def summary(self) -> str:
        return self._summary

    @property
    def description(self) -> str:
        return self._description

    @property
    def location(self) -> str:
        return self._location

    @property
    def formatted_dtstart(self) -> str:
        return self._format_datetime(self._dtstart)

    @property
    def formatted_dtend(self) -> str:
        return self._format_datetime(self._dtend)

    def generate_google_calendar_url(self) -> str:
        base_url = "https://www.google.com/calendar/render?action=TEMPLATE"
        params = {"text": self._summary, "hl": "ja"}
        if self._dtstart and self._dtend:
            params["dates"] = (
                f"{self._dtstart.strftime('%Y%m%dT%H%M%S')}/{self._dtend.strftime('%Y%m%dT%H%M%S')}"
            )
        elif self._dtstart:
            params["dates"] = (
                f"{self._dtstart.strftime('%Y%m%dT%H%M%S')}/{self._dtstart.strftime('%Y%m%dT%H%M%S')}"
            )
        if self._location:
            params["location"] = self._location
        if self._description:
            params["details"] = self._description

        url_params = "&".join(f"{key}={value}" for key, value in params.items())
        return f"{base_url}&{url_params}"

    @staticmethod
    def _vtext2str(src: vText) -> str:
        if src is None:
            return ""
        return str(src)

    @staticmethod
    def _vddd2datetime(src: vDDDTypes) -> Datetime:
        if src is None:
            return None
        elif isinstance(src.dt, datetime.datetime):
            return src.dt
        elif isinstance(src.dt, datetime.date):
            return src.dt
        else:
            raise ValueError(f"src.dt is not datetime.datetime. It is {type(src.dt)}")

    @staticmethod
    def _format_datetime(dt: Datetime) -> str:
        if isinstance(dt, datetime.datetime):
            return dt.strftime("%Y/%m/%d %H:%M:%S")
        elif isinstance(dt, datetime.date):
            return dt.strftime("%Y/%m/%d")
        else:
            return ""
