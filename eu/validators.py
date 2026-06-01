class SchemaValidationError(Exception):
    pass


def validate_item(item):
    if not isinstance(item, dict):
        raise SchemaValidationError(f"Invalid item type: {type(item)}")

    name = item.get("name")

    if not name or not isinstance(name, str):
        raise SchemaValidationError("Missing or invalid name")

    item["name"] = name.strip()

    item["sanctions"] = item.get("sanctions") or []
    item["aliases"] = item.get("aliases") or []

    return item


def validate_dataset(data):
    if not isinstance(data, dict):
        raise SchemaValidationError("Root must be dict")

    items = data.get("items")

    if not isinstance(items, list):
        raise SchemaValidationError("items must be list")

    validated = [validate_item(i) for i in items]

    return {
        "generated_at": data.get("generated_at"),
        "items": validated
    }