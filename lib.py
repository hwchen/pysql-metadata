from typing import List
import json
import sql_metadata


class SqlMetadata:
    """
        Sql Metadata: parses a sql statement, and extracts metadata on tables, cols, etc. in query.
    """
    def __init__(self, sql: str):
        self.sql = sql

    """
        Returns the ast (as a dict? don't know the type of ast)
        Using sql_metadata, it's not a real ast, just a stream of tokens
    """
    def raw_ast(self):
        sql_metadata.get_query_tokens(self.sql)

    def tables_queried(self) -> List[str]:
        return sql_metadata.get_query_tables(self.sql)

    def columns_queried(self) -> List[str]:
        return sql_metadata.get_query_columns(self.sql)


# easy testing for now
if __name__ == "__main__":

    statement = """ WITH customer_total_return 
        AS (SELECT sr_customer_sk     AS ctr_customer_sk, 
                    sr_store_sk        AS ctr_store_sk, 
                    Sum(sr_return_amt) AS ctr_total_return 
            FROM   store_returns, 
                    date_dim 
            WHERE  sr_returned_date_sk = d_date_sk 
                    AND d_year = 2001 
            GROUP  BY sr_customer_sk, 
                    sr_store_sk),
    high_return AS (
        SELECT ctr_store_sk, Avg(ctr_total_return) * 1.2 AS return_limit
        FROM   customer_total_return ctr2 
        GROUP BY ctr_store_sk
    )
    SELECT c_customer_id 
    FROM   customer_total_return ctr1, 
        store, 
        customer,
        high_return 
    WHERE  ctr1.ctr_total_return > high_return.return_limit
        AND s_store_sk = ctr1.ctr_store_sk 
        AND s_state = 'TN' 
        AND ctr1.ctr_customer_sk = c_customer_sk 
        AND ctr1.ctr_store_sk = high_return.ctr_store_sk
    ORDER  BY c_customer_id
    LIMIT 100;
    """

    metadata = SqlMetadata(statement)
    # this looks right
    print(metadata.tables_queried())

    # This one has bugs, it returns functions like Sum as well as columns,
    # and returns columns used in comparisons, not just projected columns.
    # Also returns raw string, with qualifiers that may be aliases (not tied to table)
    # ['sr_customer_sk', 'sr_store_sk', 'Sum', 'sr_return_amt', 'sr_returned_date_sk', 'd_date_sk', 'd_year', 'ctr_store_sk', 'Avg', 'ctr_total_return', 'c_customer_id', 'ctr1.ctr_total_return', 'high_return.return_limit', 's_store_sk', 'ctr1.ctr_store_sk', 's_state', 'ctr1.ctr_customer_sk', 'c_customer_sk', 'high_return.ctr_store_sk']
    print(metadata.columns_queried())
