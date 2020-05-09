from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class LoadDimensionOperator(BaseOperator):

    ui_color = "#80BD9E"
    insert_sql = """
        INSERT INTO {}
        {}
    """

    @apply_defaults
    def __init__(
        self,
        redshift_conn_id="",
        dimension_table="",
        select_sql="",
        truncate=True,
        *args,
        **kwargs,
    ):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.dimension_table = dimension_table
        self.select_sql = select_sql
        self.truncate = truncate

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        if self.truncate is True:
            self.log.info(f"Deleting data from {self.dimension_table} dimension table")
            redshift.run(f"DELETE FROM {self.dimension_table}")

        self.log.info(f"Loading data into {self.dimension_table} dimension table")
        formatted_sql = LoadDimensionOperator.insert_sql.format(
            self.dimension_table, self.select_sql
        )
        redshift.run(formatted_sql)
