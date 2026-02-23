def select_chart(columns, results):
    if not results or len(columns) < 2:
        return None

    first_value = results[0][0]
    second_value = results[0][1]

    # Date + numeric → Line chart
    if isinstance(second_value, (int, float)) and "date" in columns[0].lower():
        return "line"

    # Categorical + numeric → Bar chart
    if isinstance(second_value, (int, float)) and not isinstance(first_value, (int, float)):
        return "bar"

    # Two numeric → Scatter
    if isinstance(first_value, (int, float)) and isinstance(second_value, (int, float)):
        return "scatter"

    return None