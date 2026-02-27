from app.schema import SCHEMA


def validate_sql(sql):

    sql = sql.lower()

    allowed = SCHEMA.keys()

    for table in allowed:

        if table in sql:
            return True

    return False
