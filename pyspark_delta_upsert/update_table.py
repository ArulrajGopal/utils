# Databricks notebook source
# MAGIC %md
# MAGIC # `update_table` — Delta Lake Merge Helper
# MAGIC
# MAGIC **Purpose**: Perform a Delta Lake MERGE (upsert + scoped delete) with dynamic SQL generation.
# MAGIC
# MAGIC **Usage**: `%run ./update_table` (also pulled in transitively via `%run ./utils`).

# COMMAND ----------

# DBTITLE 1,Imports
# =============================================================================
# Imports
# =============================================================================
from delta.tables import DeltaTable

# COMMAND ----------

# DBTITLE 1,Delta Lake Merge Helper
# =============================================================================
# Delta Lake Merge Helper
# =============================================================================

def update_table(
    df_source,
    delta_table: str,
    join_cols: list,
    change_cols: list,
    delete_scope_cols: list,
) -> dict:
    """Perform a Delta Lake MERGE (upsert + scoped delete) with dynamic SQL generation.

    Args:
        df_source:          Source DataFrame (aliased as ``src`` internally).
        delta_table:        Fully-qualified Delta table name.
        join_cols:          Columns used to match source ↔ target rows (merge keys).
        change_cols:        Non-key payload columns checked for changes to trigger UPDATE.
        delete_scope_cols:  Columns that scope the ``NOT MATCHED BY SOURCE DELETE``
                            to only this partition / tenant.

    Returns:
        ``operationMetrics`` dict from the most recent Delta history entry.
    """
    merge_condition = " AND ".join([f"src.{c} = tgt.{c}" for c in join_cols])

    update_condition = " OR ".join([f"NOT (src.{c} <=> tgt.{c})" for c in change_cols])

    update_set    = {c: f"src.{c}" for c in change_cols + ["ModifiedDate"]}
    insert_values = {c: f"src.{c}" for c in join_cols + change_cols + ["CreatedDate", "ModifiedDate"]}

    # FIX: store reference once — reused for both merge build and history lookup
    dt = DeltaTable.forName(spark, delta_table)

    merge_builder = (
        dt.alias("tgt")
        .merge(df_source.alias("src"), merge_condition)
        .whenMatchedUpdate(condition=update_condition, set=update_set)
        .whenNotMatchedInsert(values=insert_values)
    )

    if delete_scope_cols:
        scope_row        = df_source.select(delete_scope_cols).first()
        delete_condition = " AND ".join(
            [f"tgt.{c} = '{scope_row[c]}'" for c in delete_scope_cols]
        )
        merge_builder = merge_builder.whenNotMatchedBySourceDelete(condition=delete_condition)

    merge_builder.execute()

    # Reuses stored dt reference — avoids a second DeltaTable.forName() round-trip
    metrics = (
        dt.history(1)
        .select("operationMetrics")
        .collect()[0]["operationMetrics"]
    )

    return metrics
