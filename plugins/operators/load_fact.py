from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class LoadFactOperator(BaseOperator):

    ui_color = "#F98866"
    insert_sql = """
        INSERT INTO {}
        {}
    """

    @apply_defaults
    def __init__(
        self, redshift_conn_id="", fact_table="", select_sql="", *args, **kwargs
    ):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.fact_table = fact_table
        self.select_sql = select_sql

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info(f"Loading data into {self.fact_table} fact table")
        formatted_sql = LoadFactOperator.insert_sql.format(
            self.fact_table, self.select_sql
        )
        redshift.run(formatted_sql)
