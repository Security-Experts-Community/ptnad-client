# PT NAD Client

Python library for interacting with the PT NAD API.

## Installation
```sh
pip install ptnad-client
```

## Usage
```python
from ptnad import PTNADClient

client = PTNADClient("https://1.3.3.7", verify_ssl=False)
client.set_auth(username="user", password="pass")
# client.set_auth(auth_type="sso", username="user", password="pass", client_id="ptnad", client_secret="11111111-abcd-asdf-12334-0123456789ab", sso_url="https://siem.example.local:3334")
client.login()

query = "SELECT src.ip, dst.ip, proto FROM flow WHERE end > 2025.02.25 and end < 2025.02.26 LIMIT 10"
result = client.bql.execute(query)
print(f"Results: {result}")
```

## Available:
- Auth: 
  - Local 
  - IAM (SSO)
- BQL (Execute query)
- Monitoring 
  - Status
  - Triggers
- Signatures
  - Get classes
  - Get rules (All, Specific), 
  - Commit/Revert changes
- Replists
  - Create/Modify replists (basic and dynamic)
  - Get replist info

## Comming soon
- docs
- Sources
- Host 
- Groups
