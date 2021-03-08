---
title: Custom Rules
description: Adding your own rules
---

You can load and run your own custom rules in Oliver Twist. This is achieved using the `--add-rules-from` option, which is repeatable, allowing you to load rules from multiple locations, e.g.

```shell
olivertwist check --add-rules-from=./custom_rules/ --add-rules-from=./more_rules/ manifest.json
```

The value you give should be to a directory containing Python source (`.py`) files that encode the logic for your rules. In order to be discovered and run by Oliver Twist, your rules must be instances of `olivertwist.ruleengine.rule.Rule`. This can be achieved by applying the `@rule` decorator to a plain function with the signature `(manifest: Manifest) -> (passes: List[Node], failures: List[Node])` e.g.:

```python
from olivertwist.ruleengine.rule import rule

@rule(id="my-pointless-rule", name="Everything is allowed!")
def pass_everything(manifest: Manifest) -> Tuple[List[Node], List[Node]]:
    return list(manifest.nodes()), []

```

An important constraint here is that the `id` you specify should be unique and should not clash with any of the [pre-defined rules](./rules.md)
