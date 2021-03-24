---
title: Rules
description: The dag auditing rules
---

## No disabled models

There are disabled scripts.

If you have disabled a script that you no longer require, you should probably delete it.
Assuming that you have your dbt scripts under version control, you can always retrieve the script if you need it in future.

## No orphaned models

There are model(s) that have become disconnected and have no resolvable dependencies.

```mermaid
graph LR
  A --> B --> C
  Orphan
```

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

## Single source per staging model

There are [staging](#staging) script(s) that have multiple [source](#source) inputs.

```mermaid
graph LR
  src1[Source A] & src2[Source B] --> Staging
```

When a staging script depends on a source, it should be a one-to-one mapping. This allows for any renaming or casting from the source system to be done in one place.

## No rejoin models

These models are taking part in rejoins.

```mermaid
graph LR
  Source --> Staging --> m1[Mart A] --> m2[Mart B]
  Staging --> m2
```

The example above shows that `Staging` is rejoined into `Mart B`. This probably means that something is missing in `Mart A`.

## No references outside of its own staging area

There are [staging](#staging) model(s) referencing a staging model that belongs in a different area

```mermaid
graph LR
  subgraph stg2[Staging 2]
  src_b --> stg_b
  end
  subgraph stg1[Staging 1]
  src_a --> stg_a
  end
  subgraph stg3[Staging 3]
  src_b --This is bad!--> stg_c
  end
  
```

If you want to cross areas, this should be done at mart level.

## No references to marts from staging

There are [staging](#staging) model(s) referencing a [mart](#mart) model.

```mermaid
graph LR
  Source --> Staging --> Marts
  Marts --This is bad!--> Staging
```

Data should be flowing from source centric to business centric areas like so:

```mermaid
graph LR
  Source --> Staging --> Marts
```

## No references to source from marts

There are [mart](#mart) model(s) referencing a [source](#source). 

```mermaid
graph LR
  Source --> Staging --> Marts
  Source --This is bad!--> m2[Mart B]
```

Data should be flowing from source centric to business centric areas like so:

```mermaid
graph LR
  Source --> Staging --> Marts
```

## No owner on physical models

There are physical models without a designated owner. Physical models consist of the following:
- sources
- table materialization
- view materialization
- incremental materialization

To ensure ownership and proper cataloguing of data is preserved, fill in all your physical models with the owner tag as described in the [Dbt reference](https://docs.getdbt.com/reference/resource-properties/meta/#designate-a-model-owner)


## Definitions
### Source

The resource type is "source".
### Mart

The resource type is "model" and the fully qualified name contains "marts"

### Staging

The resource type is "model" and the either the fully qualified name contains "staging" or the model id contains "stg_"
