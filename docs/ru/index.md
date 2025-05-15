![image](../assets/logo_with_text.svg)

![PyPI](https://img.shields.io/pypi/v/ptnad-client)

# PT NAD Client

**Документация**: <a href="https://security-experts-community.github.io/ptnad-client">https://security-experts-community.github.io/ptnad-client/</a>

**Исходный код**: <a href="https://github.com/Security-Experts-Community/ptnad-client">https://github.com/Security-Experts-Community/ptnad-client</a>

---

Библиотека на Python для взаимодействия с API PT NAD.

## 🚀 Установка
```python
pip install ptnad-client
```

### 📖 Пример использования
```python
from ptnad import PTNADClient

client = PTNADClient("https://1.3.3.7", verify_ssl=False)
client.set_auth(username="user", password="pass")
# client.set_auth(auth_type="sso", username="user", password="pass", client_id="ptnad", client_secret="11111111-abcd-asdf-12334-0123456789ab", sso_url="https://siem.example.local:3334")
client.login()

query = "SELECT src.ip, dst.ip, proto FROM flow WHERE end > 2025.02.25 and end < 2025.02.26 LIMIT 10"
result = client.bql.execute(query)
print(f"Результаты: {result}")
```

### 📋 Примеры фильтров

Вот несколько полезных примеров фильтров, которые вы можете использовать в своих запросах:

```python
# HTTP не на порту 80 (внешний)
"app_proto == 'http' && dst.port != 80 && dst.groups != 'HOME_NET'"

# TLS не на порту 443 (внешний)
"app_proto == 'tls' && dst.port != 443 && dst.groups != 'HOME_NET'"

# Порт 53 не по DNS
"dst.port == 53 && app_proto != 'dns' && (flags == 'FINISHED' && !(flags == 'MISSED_START' || flags == 'MISSED_END')) && pkts.recv > 0"

# Сессии с файлами
"files"

# Поиск по названию файла
"files.filename ~ '*amd64.deb'"

# Bittorrent из внутренней сети
"app_proto == bittorrent and src.groups == 'HOME_NET'"

# Почта в открытую (внешняя)
"(app_proto == 'smtp' || app_proto == 'pop3' || app_proto == 'imap') && !(smtp.rqs.cmd.name == 'STARTTLS' || pop3.rqs.cmd.name == 'STLS' || imap.rqs.cmd.name == 'STARTTLS') && dst.groups != 'HOME_NET'"

# Нестандартные порты
"src.groups != 'HOME_NET' && dst.port != 80 && dst.port != 443 && dst.port != 25 && src.port != 53 && src.port != 443 && src.port != 123 && (flags == 'FINISHED' && !(flags == 'MISSED_START' || flags == 'MISSED_END')) && pkts.recv > 0"

# Digital Ocean и Amazon
"dst.geo.org == 'DigitalOcean, LLC' || dst.geo.org == 'Amazon.com, Inc.'"

# POST запросы с ответом 200
"http(rqs.method==POST && rsp.code==200)"

# Сработки MultiScanner
"rpt.type == 'ms'"

# Майнеры
"rpt.cat == 'miners'"
```

С подробными инструкциями и примерами можете ознакомиться тут - [usage_examples](https://github.com/Security-Experts-Community/ptnad-client/blob/main/docs/ru/usage_examples.ipynb)

## ✅ Возможности

🔐 Аутентификация  
- Локальная аутентификация  
- IAM (SSO) аутентификация  

📊 BQL-запросы  
- Выполнение запросов  

📡 Мониторинг  
- Получение статуса системы  
- Управление триггерами  

🛡️ Сигнатуры  
- Получение классов  
- Получение правил (всех/конкретных)  
- Применение/откат изменений  

📋 Реплисты  
- Создание/редактирование базовых и динамических реплистов  
- Получение информации о реплистах  

### 🛠️ Планируемые функции  
- Документация с примерами 
- Управление источниками  
- Управление хостами  
- Управление группами  

## 🧑‍💻 Вклад в проект

Хотите внести свой вклад? Ознакомьтесь с гайдом:

- [📄 Гайд для участников](CONTRIBUTING.md)

Мы открыты для любых идей, предложений и улучшений!

![image](../assets/pic_left.svg)

PT NAD Client — часть экосистемы открытых SDK, созданной для упрощения интеграции с продуктами компании.
Вы также можете ознакомиться с другими проектами:

🔹[py-ptsandbox](https://github.com/Security-Experts-Community/py-ptsandbox) — Python-библиотека для асинхронной работы с API PT Sandbox

🔹[sandbox-cli](https://github.com/Security-Experts-Community/sandbox-cli) — CLI-инструмент для удобной работы с PT Sandbox