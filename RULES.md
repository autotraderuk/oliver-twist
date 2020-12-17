# Staging scripts referencing multiple sources

There are staging script(s) that have multiple source inputs.

When a staging script depends on a source, it should be a one-to-one mapping. This allows for any renaming or casting from the source system to be done in one place.

# Rejoin models

These models are taking part in rejoins.

# Disabled models

There are disabled scripts.

If you have disabled a script that you no longer require, you should probably delete it.
Assuming that you have your dbt scripts under version control, you can always retrieve the script if you need it in future.


# Orphaned models

There are model(s) that have become disconnected and have no resolvable dependencies.

This can be caused by:

- Hard-coded references to scripts
- The use of `target_project()` to reference a script
- A script that compiles to no content (e.g. an empty file or a macro)

When referencing dependencies, you should use:

- `source()` for sources (https://docs.getdbt.com/docs/using-sources)
- `ref()` for models (https://docs.getdbt.com/docs/ref)

e.g.:

```sql
SELECT *
FROM {{ source('source_name', 'table_name') }}

SELECT *
FROM {{ ref('script_name') }}
```
