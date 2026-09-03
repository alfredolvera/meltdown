# Per-function provenance

Every JSON file under `functions/` describes one routine from one exact game
revision. The recommended name is `<revision>_<address>.json`, for example
`ki15d_80001234.json`.

Create a record:

```sh
python3 tools/ki_project.py new-function \
  --id ki15d_80001234 \
  --address 0x80001234 \
  --name provisional_name
```

Validate all records:

```sh
python3 tools/ki_project.py provenance-check provenance/functions
```

`TEMPLATE.json` is documentation and is skipped by the validator. Assembly,
source, and evidence paths must be relative to the repository root.
