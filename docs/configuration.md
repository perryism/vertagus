[index](./index.md)

Configuration
=============

Vertagus uses `toml` for its configuration format. You can see the `vertagus.toml` file at the root of this repository
for an example. Here's another one:

```toml
[scm]
type = "git"
tag_prefix = "v"

[project.rules]
current = ["not_empty"]
increment = ["any"]
manifest_comparisons = []

[project.stages.dev.rules]
current = ["regex_dev_mmp"]

[project.stages.beta]
aliases = ["string:latest"]

[project.stages.beta.rules]
current = ["regex_beta_mmp"]

[project.stages.prod]
aliases = ["string:stable", "string:latest", "major.minor"]

[project.stages.prod.rules]
current = ["regex_prod"]

[[project.manifests]]
type = "setuptools_pyproject"
path = "./pyproject.toml"
name = "pyproject"
```