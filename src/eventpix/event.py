import datetime

from icalendar.prop import vDDDTypes, vText  # type: ignore[import-untyped]


class Event:
    def __init__(
        self,
        dtstart: vDDDTypes,
        dtend: vDDDTypes,
        summary: vText,
        description: vText,
        location: vText,
    ):
        self.dtstart_str: str = self._vddd2str(dtstart)
        self.dtend_str: str = self._vddd2str(dtend)
        self.summary: str = self._vtext2str(summary)
        self.description: str = self._vtext2str(description)
        self.location: str = self._vtext2str(location)

        self.dtstart_datetime = self._vddd2datetime(dtstart)
        self.dtend_datetime = self._vddd2datetime(dtend)

    @staticmethod
    def _vddd2str(src: vDDDTypes) -> str:
        if src is None:
            return ""
        return str(src.dt)

    @staticmethod
    def _vtext2str(src: vText) -> str:
        if src is None:
            return ""
        return str(src)

    @staticmethod
    def _vddd2datetime(src: vDDDTypes) -> datetime.datetime | datetime.date | None:
        if src is None:
            return None
        elif isinstance(src.dt, datetime.datetime):
            return src.dt
        elif isinstance(src.dt, datetime.date):
            return src.dt
        else:
            raise ValueError(f"src.dt is not datetime.datetime. It is {type(src.dt)}")

    @staticmethod
    def formatDatetime(dt: datetime.datetime | datetime.date | None) -> str:
        if dt is None:
            return ""
        elif isinstance(dt, datetime.datetime):
            return dt.strftime('%Y/%m/%d %H:%M:%S')
        elif isinstance(dt, datetime.date):
            return dt.strftime('%Y/%m/%d')
        else:
            raise ValueError(f"dt is not datetime.datetime. It is {type(dt)}")