from moz_sql_parser import parse
from typing import List
import json


class SqlMetadata:
    """
        Sql Metadata: parses a sql statement, and extracts metadata on tables, cols, etc. in query.
    """
    def __init__(self, sql: str):
        self.ast = parse(sql)

    """
        Returns the ast (as a dict? don't know the type of ast)
    """
    def raw_ast(self):
        self.ast

    def tables_queried(self) -> List[str]:
        try:
            tables = []
            # this is to check that it's a select query. It should
            # error?
            self.ast["select"]

            extract_tables_from_from(self.ast["from"], tables)

            return tables 
        except KeyError:
            return []

def extract_tables_from_from(query_from, tables: List[str]) -> List[str]:
    # extract from body: from
    try:
        # check if from is a string, then append, otherwise if it's another query
        # then get the `from` from that and call recursive
        tables.append(query_from)
    except KeyError:
        return

# easy testing for now
if __name__ == "__main__":

# this already doesn't work because mozilla parser expects 'select' for query
#    statement = """ WITH customer_total_return 
#        AS (SELECT sr_customer_sk     AS ctr_customer_sk, 
#                    sr_store_sk        AS ctr_store_sk, 
#                    Sum(sr_return_amt) AS ctr_total_return 
#            FROM   store_returns, 
#                    date_dim 
#            WHERE  sr_returned_date_sk = d_date_sk 
#                    AND d_year = 2001 
#            GROUP  BY sr_customer_sk, 
#                    sr_store_sk),
#    high_return AS (
#        SELECT ctr_store_sk, Avg(ctr_total_return) * 1.2 AS return_limit
#        FROM   customer_total_return ctr2 
#        GROUP BY ctr_store_sk
#    )
#    SELECT c_customer_id 
#    FROM   customer_total_return ctr1, 
#        store, 
#        customer,
#        high_return 
#    WHERE  ctr1.ctr_total_return > high_return.return_limit
#        AND s_store_sk = ctr1.ctr_store_sk 
#        AND s_state = 'TN' 
#        AND ctr1.ctr_customer_sk = c_customer_sk 
#        AND ctr1.ctr_store_sk = high_return.ctr_store_sk
#    ORDER  BY c_customer_id
#    LIMIT 100;
#    """

    sql_metadata = SqlMetadata(statement)
    print(sql_metadata.tables_queried())
