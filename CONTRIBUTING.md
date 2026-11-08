# Contributing

Corrections to setup instructions, reproducible problem reports and clearer troubleshooting are welcome.

Keep instructions specific to FOOTISTA 2019 **1.30.01 / 2019 Series 3**. Distinguish tested behavior from a candidate or an untested feature. Do not add client download buttons for unpublished releases or claim two-PC PvP acceptance without evidence.

Use relative links within the repository. Do not commit downloads, native game files, local installations, logs or private account information. A normal source ZIP of this repository should remain small.

Run the repository checks before opening a pull request:

```powershell
py -3.13 -B -m unittest discover -s tests -v
py -3.13 -B tools/check_repository.py
```

Client runtime changes and signed package builds are maintained separately from this public download/documentation repository. Release changes follow [the maintainer procedure](docs/releases.md).
