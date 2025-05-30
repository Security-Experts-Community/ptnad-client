from typing import Any, Dict, List, Optional

from ptnad.exceptions import PTNADAPIError


class SensorsAPI:
    def __init__(self, client) -> None:
        self.client = client

    def get_sensors(self) -> List[Dict[str, Any]]:
        """
        Get detailed information about ptdpi modules: their properties, state,
        information about applied filters and rules.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing ptdpi module information.

        Raises:
            PTNADAPIError: If there's an error retrieving the sensors information.

        """
        try:
            response = self.client.get("/sensors").json()
            return response["results"]
        except PTNADAPIError as e:
            e.operation = "get sensors"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to get sensors: {str(e)}")

    def get_sensor(self, sensor_id: int) -> Dict[str, Any]:
        """
        Get information about a specific ptdpi module by its id.

        Args:
            sensor_id (int): ID of the ptdpi module.

        Returns:
            Dict[str, Any]: Information about the ptdpi module.

        Raises:
            PTNADAPIError: If there's an error retrieving the ptdpi module information.

        """
        try:
            response = self.client.get(f"/sensors/{sensor_id}").json()
            return response
        except PTNADAPIError as e:
            e.operation = f"get sensor {sensor_id}"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to get sensor {sensor_id}: {str(e)}")
