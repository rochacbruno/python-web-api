from urllib.request import urlopen

result = urlopen("http://example.com/index.html")
print(result.read().decode("utf-8"))
