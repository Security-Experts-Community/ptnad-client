from enum import Enum
from typing import Any, Dict, List

from ptnad.exceptions import PTNADAPIError


class Status(str, Enum):
    UNKNOWN = "unknown"
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"

    def __str__(self) -> str:
        return self.value

class TriggerType(str, Enum):
    AUDIT = "audit"
    UPDATES = "updates"
    STATS = "stats"
    LICENSE = "license"

    def __str__(self) -> str:
        return self.value

class Problem:
    def __init__(self, status: str, template: str, vars: Dict[str, Any]) -> None:
        self.status = Status(status)
        self.template = template
        self.vars = vars
        self.message = self.template.format(**self.vars)

    def __str__(self) -> str:
        return self.message

class MonitoringStatus:
    def __init__(self, status: str, problems: List[Dict[str, Any]]) -> None:
        self._status = Status(status)
        self.problems_raw = problems
        self.problems = [Problem(**prob) for prob in problems]

    @property
    def status(self) -> str:
        return str(self._status)

class Trigger:
    def __init__(self, id: str, type: str, status: str, template: str, vars: Dict[str, Any], updated: str) -> None:
        self.id = id
        self.type = TriggerType(type)
        self.status = Status(status)
        self.template = template
        self.vars = vars
        self.updated = updated

class MonitoringAPI:
    def __init__(self, client) -> None:
        self.client = client

    def get_status(self) -> MonitoringStatus:
        """
        Get the current status.

        Returns:
            MonitoringStatus: An object containing the current status and any problems.

        Raises:
            PTNADAPIError: If there's an error retrieving the status.

        """
        try:
            response = self.client.get("/monitoring/status").json()
            return MonitoringStatus(**response)
        except PTNADAPIError as e:
            e.operation = "get monitoring status"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to get monitoring status: {str(e)}")

    def get_triggers(self) -> List[Trigger]:
        """
        Get the list of triggers.

        Returns:
            List[Trigger]: A list of Trigger objects.

        Raises:
            PTNADAPIError: If there's an error retrieving the triggers.

        """
        try:
            response = self.client.get("/monitoring/triggers").json()
            return [Trigger(**trigger) for trigger in response.get("results", [])]
        except PTNADAPIError as e:
            e.operation = "get triggers"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to get triggers: {str(e)}")

    def get_trigger_by_id(self, trigger_id: str) -> Trigger | None:
        """
        Get a specific trigger by its ID.

        Args:
            trigger_id (str): The ID of the trigger to retrieve.

        Returns:
            Optional[Trigger]: The Trigger object if found, None otherwise.

        Raises:
            PTNADAPIError: If there's an error retrieving the trigger.

        """
        triggers = self.get_triggers()
        return next((trigger for trigger in triggers if trigger.id == trigger_id), None)

    def get_active_triggers(self) -> List[Trigger]:
        """
        Get all active triggers (triggers with status other than 'green').

        Returns:
            List[Trigger]: A list of active Trigger objects.

        Raises:
            PTNADAPIError: If there's an error retrieving the triggers.

        """
        triggers = self.get_triggers()
        return [trigger for trigger in triggers if trigger.status != "green"]

    def get_triggers_by_type(self, trigger_type: str) -> List[Trigger]:
        """
        Get all triggers of a specific type.

        Args:
            trigger_type (str): The type of triggers to retrieve.

        Returns:
            List[Trigger]: A list of Trigger objects of the specified type.

        Raises:
            PTNADAPIError: If there's an error retrieving the triggers.

        """
        triggers = self.get_triggers()
        return [trigger for trigger in triggers if trigger.type == trigger_type]
