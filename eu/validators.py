class SchemaValidationError(Exception):
    pass


def validate_item(item):
    """
    Accepts either:
    - dict (single item)
    - list of dicts (bulk items)
    """

    # CASE 1: list input
    if isinstance(item, list):
        return [validate_item(i) for i in item]

    # CASE 2: must be dict
    if not isinstance(item, dict):
        raise SchemaValidationError(f"Invalid item type: {type(item)}")

    name = item.get("name")

    if not name or not isinstance(name, str):
        raise SchemaValidationError("Missing or invalid name")

    item["name"] = name.strip()

    # normalize optional fields
    item["sanctions"] = item.get("sanctions") or []
    item["aliases"] = item.get("aliases") or []

    return item