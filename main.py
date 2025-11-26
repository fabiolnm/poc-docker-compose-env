import os

hello = os.environ.get("HELLO", "NOT SET")
print(f"HELLO={hello}")
