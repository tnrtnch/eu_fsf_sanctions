import json

with open("eu_fsf_sanctions.json") as f:
    data = json.load(f)

assert "items" in data
assert isinstance(data["items"], list)

print(len(data["items"]))