![image](../assets/logo_with_text.svg)

![PyPI](https://img.shields.io/pypi/v/ptnad-client)

# PT NAD Client

**Documentation**: <a href="https://security-experts-community.github.io/ptnad-client">https://security-experts-community.github.io/ptnad-client</a>

**Source Code**: <a href="https://github.com/Security-Experts-Community/ptnad-client">https://github.com/security-experts-community/ptnad-client</a>

---
Python library for interacting with the PT NAD API.

## 🚀 Installation
```python
pip install ptnad-client
```
### 📖 Usage
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

### 📋 Filter Examples

Here are some useful filter examples you can use in your queries:

```python
# HTTP not on port 80 (external)
"app_proto == 'http' && dst.port != 80 && dst.groups != 'HOME_NET'"

# TLS not on port 443 (external)
"app_proto == 'tls' && dst.port != 443 && dst.groups != 'HOME_NET'"

# Port 53 but not DNS
"dst.port == 53 && app_proto != 'dns' && (flags == 'FINISHED' && !(flags == 'MISSED_START' || flags == 'MISSED_END')) && pkts.recv > 0"

# Sessions with files
"files"

# Search file by name
"files.filename ~ '*amd64.deb'"

# Bittorrent from internal network
"app_proto == bittorrent and src.groups == 'HOME_NET'"

# Unencrypted email (external)
"(app_proto == 'smtp' || app_proto == 'pop3' || app_proto == 'imap') && !(smtp.rqs.cmd.name == 'STARTTLS' || pop3.rqs.cmd.name == 'STLS' || imap.rqs.cmd.name == 'STARTTLS') && dst.groups != 'HOME_NET'"

# Non-standard ports
"src.groups != 'HOME_NET' && dst.port != 80 && dst.port != 443 && dst.port != 25 && src.port != 53 && src.port != 443 && src.port != 123 && (flags == 'FINISHED' && !(flags == 'MISSED_START' || flags == 'MISSED_END')) && pkts.recv > 0"

# Digital Ocean and Amazon
"dst.geo.org == 'DigitalOcean, LLC' || dst.geo.org == 'Amazon.com, Inc.'"

# POST requests with 200 response
"http(rqs.method==POST && rsp.code==200)"

# MultiScanner triggered
"rpt.type == 'ms'"

# Miners
"rpt.cat == 'miners'"
```

You can find detailed instructions and examples here - [usage_examples](https://github.com/Security-Experts-Community/ptnad-client/blob/main/docs/en/usage_examples.ipynb)

## ✅ Features

🔐 Authentication
- Local authentication
- IAM (SSO) authentication

📊 BQL Queries
- Execute queries

📡 Monitoring
- Get system status
- Manage triggers

🛡️ Signatures
- Retrieve classes
- Get rules (all/specific)
- Commit/Revert changes

📋 Replists
- Create/Modify basic and dynamic replists
- Retrieve replist info

### 🛠️ Upcoming Features
- Documentation
- Sources management
- Hosts management
- Groups management

## 🧑‍💻 Contributing

Want to contribute? Check out the following:

- [📄 Contributor Guide](CONTRIBUTING.md)

We welcome all ideas, suggestions, and improvements!

![image](../assets/pic_left.svg)

PT NAD Client is part of an open SDK ecosystem designed to simplify integration with our products.
Check out other related projects in the ecosystem:

🔹[py-ptsandbox](https://github.com/Security-Experts-Community/py-ptsandbox) — A python library for asynchronous interactions with the PT Sandbox API

🔹[sandbox-cli](https://github.com/Security-Experts-Community/sandbox-cli) — CLI instrument for easy working with PT Sandbox