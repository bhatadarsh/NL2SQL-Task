def choose_chart(columns):

    if not columns:
        return None

    if len(columns) < 2:
        return None

    first = columns[0].lower()

    if "date" in first or "time" in first:
        return "line"

    return "bar"
