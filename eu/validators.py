class SchemaValidationError(Exception):
    pass


def validate_item(item):
    if not isinstance(item, dict):
        raise SchemaValidationError(
            f"Invalid item type: {type(item)}"
        )

    name = item.get("name")

    if not name or not isinstance(name, str):
        raise SchemaValidationError(
            "Missing or invalid name"
        )

    item["name"] = name.strip()

    item["schema"] = item.get("schema") or ""
    item["sanctions"] = item.get("sanctions") or ""
    item["aliases"] = item.get("aliases") or ""

    return item  