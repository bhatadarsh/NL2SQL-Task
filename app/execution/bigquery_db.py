from google.cloud import bigquery

client = bigquery.Client()


def execute_query(sql_query):

    try:
        query_job = client.query(sql_query)

        result = query_job.result()

        df = result.to_dataframe()

        columns = list(df.columns)

        rows = df.values.tolist()

        return columns, rows

    except Exception as e:

        return None, str(e)
