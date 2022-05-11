import requests
result = requests.get("http://example.com/index.html")
print(result.status_code)
print(result.content)

import httpx
result = httpx.get("http://example.com/index.html")
print(result.status_code)
print(result.content)
