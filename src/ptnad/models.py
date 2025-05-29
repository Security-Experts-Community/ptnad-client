from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class TimeRange:
    """Time range for queries."""
    start: int
    end: int


class Flow:
    """Flow data model."""
    
    def __init__(self, obj: Dict[str, Any]):
        """Initialize Flow from dictionary.
        
        Args:
            obj: Dictionary with flow data
        """
        for field_name in self.get_all_fields():
            if field_name in obj:
                setattr(self, field_name, obj[field_name])
            else:
                setattr(self, field_name, None)

    @staticmethod
    def get_all_fields() -> List[str]:
        """Get all possible flow fields."""
        return [
            "_prn.id",
            "_prn.tx_id",
            "_chld.id",
            "_chld.type",
            "proto",
            "src.ip",
            "src.port",
            "src.mac",
            "src.dns",
            "src.geo.region",
            "src.geo.city",
            "src.geo.country",
            "src.geo.asn",
            "src.geo.org",
            "src.groups",
            "src.name",
            "dst.ip",
            "dst.port",
            "dst.mac",
            "dst.dns",
            "dst.geo.region",
            "dst.geo.city",
            "dst.geo.country",
            "dst.geo.asn",
            "dst.geo.org",
            "dst.groups",
            "dst.name",
            "host.ip",
            "host.ip6",
            "host.port",
            "host.dns",
            "host.groups",
            "host.name",
            "bytes.total",
            "bytes.recv",
            "bytes.sent",
            "pkts.total",
            "pkts.recv",
            "pkts.sent",
            "state",
            "flags",
            "errors",
            "_reason",
            "_state",
            "tcp.flags",
            "tcp.flags_tc",
            "tcp.flags_ts",
            "tcp._state",
            "start",
            "end",
            "app_proto",
            "app_service",
            "pcaps",
            "tunnels.level",
            "tunnels.type",
            "tunnels.vlan_id",
            "tunnels.ip",
            "tunnels.ip6",
            "tunnels.endpoints.ip",
            "tunnels.endpoints.ip6",
            "tunnels.endpoints.port",
            "banner.client",
            "banner.server",
            "os.client",
            "os.server",
            "os_fp.client",
            "os_fp.server",
            "os_pt.client",
            "os_pt.server",
            "credentials.login",
            "credentials.password",
            "credentials.valid",
            "rpt.where",
            "rpt.id",
            "rpt.type",
            "rpt.cat",
            "rpt.color",
            "rpt.verdict",
            "rpt.rtime",
            "_ltime",
            "stag",
            "_ndx",
            "id",
            "_type",
            "_index",
            "_sort",
            "criticality",
            "false_positive",
            "has_files"
        ]

    @classmethod
    def from_dict(cls, dictionary: Dict[str, Any]) -> 'Flow':
        """Create Flow instance from dictionary.
        
        Args:
            dictionary: Dictionary with flow data
            
        Returns:
            Flow instance
        """
        return cls(dictionary) 