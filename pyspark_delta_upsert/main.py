# Databricks notebook source
# MAGIC %run ./update_table

# COMMAND ----------

### to be defined before running this script
### 1.df_source
### 2.SILVER_FULL
### 3.cols_list - join_cols, change_cols, delete_scope_cols


join_cols = ["col1","col2","col3"]

change_cols = [
    "col4","col5","col6","col7","col8","col9","col10","col11","col12"
]

delete_scope_cols = ["col3"]


metrics = update_table(
    df_source         = df_source,
    delta_table       = SILVER_FULL,
    join_cols         = join_cols,
    change_cols       = change_cols,
    delete_scope_cols = delete_scope_cols
)

inserted = int(metrics.get("numTargetRowsInserted",     0))
updated  = int(metrics.get("numTargetRowsUpdated",      0))
deleted  = int(metrics.get("numTargetRowsDeleted",      0))

print(f"  ✅ Merge complete — Inserted: {inserted:,}  Updated: {updated:,}  Deleted: {deleted:,}")

if inserted == 0 and updated == 0 and deleted == 0:
    print(f"  ✅ No changes — silver is already up to date.")

df_source.unpersist()