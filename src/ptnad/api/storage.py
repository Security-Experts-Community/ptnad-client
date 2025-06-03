from typing import List, Optional
import sqlite3
from datetime import datetime, timedelta
import logging
from logging.handlers import TimedRotatingFileHandler
from time import sleep
import os

from ..exceptions import PTNADAPIError
from ..models import Flow, TimeRange

class StorageAPI:
    """API for working with PT NAD storage."""
    
    FORMATTER = logging.Formatter(
        "%(asctime)s - %(process)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    def __init__(
        self,
        client,
        db_file: str = "ptnad.db",
        log_file: str = "ptnad.log",
        log_level: str = "DEBUG"
    ):
        """Initialize Storage API.
        
        Args:
            client: PTNADClient instance
            db_file: SQLite database file path
            log_file: Log file path
            log_level: Logging level
        """
        self.client = client
        self.db_file = db_file
        self.log_file = log_file
        self.log_level = log_level

    def _setup_logger(self, log_level: str, log_file: str) -> logging.Logger:
        """Setup logger with file handler."""
        logger = logging.getLogger(__name__)
        
        logger.handlers = []
        
        logger.setLevel(log_level)
        
        file_handler = TimedRotatingFileHandler(log_file, when='midnight')
        file_handler.setFormatter(self.FORMATTER)
        file_handler.suffix = "%Y%m%d"
        
        logger.addHandler(file_handler)
        logger.propagate = False
        return logger

    def _create_db(self):
        """Create SQLite database."""
        self.logger.info(f"Connect to SQLite DB in file {self.db_file}")
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS saved_flows(
                flow_id TEXT PRIMARY KEY,
                start TEXT,
                end TEXT,
                src_idx TEXT,
                dst_idx TEXT
            )
        """)
        conn.commit()

    def get_flows(
        self,
        time_range: TimeRange,
        storage_idx: str,
        nad_filter: Optional[str] = None
    ) -> List[Flow]:
        """Get flows from storage using BQL query.
        
        Args:
            time_range: Time range for query
            storage_idx: Source storage index
            nad_filter: Optional filter to apply
            
        Returns:
            List of Flow objects
        """
        query = f"""
            SELECT id, start, end 
            FROM flow 
            WHERE (end >= {time_range.start} AND end <= {time_range.end})
            {f"and ({nad_filter})" if nad_filter else ""}
            LIMIT 1
        """
        
        self.logger.debug(f"BQL Query: {query}")
        result = self.client.bql.execute(query, source=storage_idx)
        
        flows = []
        for row in result:
            flow_dict = {
                "id": row[0],
                "start": row[1],
                "end": row[2]
            }
            flows.append(Flow.from_dict(flow_dict))
            
        return flows

    def _filter_old_flows(
        self,
        flows: List[Flow],
        src_idx: str,
        dst_idx: str
    ) -> List[Flow]:
        """Filter out flows that are already in database."""
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        new_flows = []
        
        for flow in flows:
            cur.execute(
                "SELECT * FROM saved_flows WHERE flow_id = ? AND src_idx = ? AND dst_idx = ?",
                (flow.id, src_idx, dst_idx)
            )
            if cur.fetchall():
                continue
                
            cur.execute(
                "INSERT INTO saved_flows VALUES(?, ?, ?, ?, ?)",
                [flow.id, flow.start, flow.end, src_idx, dst_idx]
            )
            conn.commit()
            new_flows.append(flow)
            
        return new_flows

    def save_flows(
        self,
        nad_filter: str,
        persist_idx: str,
        storage_idx: str = "2",
        delta_hours: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        storage_dir: Optional[str] = None
    ) -> None:
        """Save flows to persistent storage.
        
        Args:
            nad_filter: Filter to apply to flows
            persist_idx: Target storage index
            storage_idx: Source storage index
            delta_hours: Hours to look back from current time
            start_time: Start timestamp in milliseconds
            end_time: End timestamp in milliseconds
            storage_dir: Directory for storing database and logs. If None, uses current directory
        """
        if storage_dir is None:
            self.storage_dir = os.path.join(os.getcwd(), "storage_output")
        else:
            self.storage_dir = storage_dir
            
        os.makedirs(self.storage_dir, exist_ok=True)

        self.db_file = os.path.join(self.storage_dir, self.db_file)
        self.log_file = os.path.join(self.storage_dir, self.log_file)
        
        self.logger = self._setup_logger(self.log_level, self.log_file)
        self._create_db()
        
        if not (delta_hours or (start_time and end_time)):
            raise ValueError(
                "Please specify either delta_hours or both start_time and end_time"
            )
            
        if delta_hours and (start_time or end_time):
            raise ValueError(
                "Can't use both delta_hours and start_time/end_time"
            )

        current_time = datetime.now()
        if delta_hours:
            time_range = TimeRange(
                int((current_time - timedelta(hours=delta_hours)).timestamp() * 1000),
                int(current_time.timestamp() * 1000)
            )
        else:
            time_range = TimeRange(start_time, end_time)

        self.logger.info(
            f"Query flows with params "
            f"start={time_range.start}, "
            f"end={time_range.end}, "
            f"filter='{nad_filter}'"
        )

        flows = self.get_flows(time_range, storage_idx, nad_filter)
        self.logger.info(f"Received {len(flows)} flows")
        
        if not flows:
            self.logger.warning("No flows found matching the criteria")
            return

        self.logger.info("Filtering old flows")
        new_flows = self._filter_old_flows(
            flows,
            storage_idx,
            persist_idx
        )

        self.logger.info(f"New flows to save: {len(new_flows)}")
        
        if not new_flows:
            self.logger.info("No new flows to save")
            return

        flow_ids = [flow.id for flow in new_flows]
        self.logger.info(f"Flow IDs to save: {flow_ids}")
        
        post_data = {
            "id": flow_ids,
            "source": [storage_idx],
            "start": time_range.start,
            "end": time_range.end,
            "target": persist_idx
        }
        
        self.logger.info(f"Preparing to save flows to target storage {persist_idx}")
        self.logger.info(f"POST data: {post_data}")
        
        try:
            endpoint = "sources/save"
            self.logger.info(f"Sending POST request to {endpoint}")
            self.logger.info(f"Full URL: {self.client.base_url}{endpoint}")
            
            response = self.client.post(
                endpoint,
                json=post_data
            )
            
            self.logger.info(f"Response status: {response.status_code}")
            self.logger.info(f"Response headers: {dict(response.headers)}")
            self.logger.info(f"Response body: {response.text}")
            
            if not response.ok:
                self.logger.error(
                    f"Server error: {response.status_code}\n{response.text}"
                )
                raise PTNADAPIError(
                    f"Failed to save flows: {response.status_code} {response.text}"
                )
                
            self.logger.info(f"Successfully sent request to save {len(new_flows)} flows")

            result = response.json()
            self.logger.info(f"Task ID: {result.get('id')}, State: {result.get('state')}")
            
            while result['state'] in ["PENDING", "STARTED", "PROGRESS"]:
                self.logger.info(f"Checking task status: {result['state']}")
                task_endpoint = f"tasks/{result['id']}"
                self.logger.info(f"Sending GET request to {task_endpoint}")
                
                response = self.client.get(task_endpoint)
                self.logger.debug(f"Task status response: {response.status_code}")
                self.logger.debug(f"Task status body: {response.text}")
                
                if not response.ok:
                    self.logger.error(
                        f"Server error: {response.status_code}\n{response.text}"
                    )
                    raise PTNADAPIError(
                        f"Failed to check task status: {response.status_code} {response.text}"
                    )
                result = response.json()
                self.logger.debug(f"Task state: {result.get('state')}")
                sleep(10)

            self.logger.info(f"Task completed with state: {result.get('state')}")
            
        except Exception as e:
            self.logger.error(f"Error during flow saving: {str(e)}")
            raise 