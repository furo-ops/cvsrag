import logging
from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


class AvailabilityAdapter(ABC):
    @abstractmethod
    def get_availability(self) -> dict[str, dict]:
        """Return dict mapping lowercase person name to their availability data."""
        pass


class CSVAvailabilityAdapter(AvailabilityAdapter):
    """Reads availability from a CSV or Excel file."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_availability(self) -> dict[str, dict]:
        path = Path(self.file_path)
        if not path.exists():
            logger.warning(f"Availability file not found: {self.file_path}")
            return {}

        try:
            if path.suffix.lower() in (".xlsx", ".xls"):
                df = pd.read_excel(path)
            else:
                df = pd.read_csv(path)

            result: dict[str, dict] = {}
            for _, row in df.iterrows():
                name = str(row.get("name", "")).strip().lower()
                if not name:
                    continue

                avail_pct = row.get("availability_percentage")
                avail_date = row.get("availability_date")
                location = row.get("location")
                grade = row.get("grade")
                current_project = row.get("current_project")
                result[name] = {
                    "current_project": (
                        str(current_project).strip()
                        if pd.notna(current_project) and str(current_project).strip()
                        else None
                    ),
                    "availability_date": (
                        str(avail_date).strip()
                        if pd.notna(avail_date) and str(avail_date).strip()
                        else None
                    ),
                    "availability_percentage": int(avail_pct) if pd.notna(avail_pct) else None,
                    "location": (
                        str(location).strip()
                        if pd.notna(location) and str(location).strip()
                        else None
                    ),
                    "grade": (
                        str(grade).strip()
                        if pd.notna(grade) and str(grade).strip()
                        else None
                    ),
                }

            return result

        except Exception as e:
            logger.error(f"Error reading availability file '{self.file_path}': {e}")
            return {}


class SharePointAvailabilityAdapter(AvailabilityAdapter):
    """Future: reads availability from SharePoint/internal tool API."""

    def get_availability(self) -> dict[str, dict]:
        raise NotImplementedError("SharePoint availability adapter not yet implemented")


def get_availability_adapter(file_path: str) -> AvailabilityAdapter:
    return CSVAvailabilityAdapter(file_path)
