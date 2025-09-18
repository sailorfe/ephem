## Advanced Usage: YAML database

`ephem`'s database is designed to be usable with only the `data view/load/delete` commands, but you may want to edit an existing chart—e.g., rename a chart created with `now --save`—or create new ones without running any commands. This is where the `data sync` comes in.

The database you just interacted with is stored at `~/.local/share/ephem/ephem.db`:

```
.local/share/ephem
|-- charts/
|   |-- jean-cremers.yaml
|   |-- jeon-soyeon.yaml
|   |-- kevin-decapite.yaml
|   |-- nick-cave.yaml
|   `-- walter-pullen.yaml
`-- ephem.db
```

Each time you run `--save`, it creates a new chart under `charts/`. You can ignore this entirely, but if you open one in a text editor like `n/vim` or `nano`, you'll see something like this:

```yaml
name: Nick Cave
timestamp_utc: '1957-09-22T02:20:00+00:00'
timestamp_input: '1957-09-22T12:20:00+10:00'
latitude: -36.25
longitude: 142.416667
_metadata:
  created: '2025-09-10T12:55:37.004823'
  source: ephem_cli
  tags: [famous, musician, adb, rodden-c]
```

### Creating new charts with YAML

```sh
cd ~/.local/share/ephem/charts
cp some-chart.yaml new-chart.yaml
$EDITOR new-chart.yaml
ephem data sync
```

This workflow can be faster than running `ephem cast --save`, but the one tradeoff I can think of is **you'll need to perform a local time -> UTC conversion yourself**. You can also remove or add as many `_metadata` fields as you want.

### Editing existing YAML charts

```sh
cd ~/.local/share/ephem/charts
$EDITOR some-chart.yaml
ephem data sync
```

Charts created with `ephem now --save` get timestamped names like "Chart 2025-09-17 14:30:25 UTC". To give them meaningful names, edit both the filename and the `name:` field inside:

```sh
cd ~/.local/share/ephem/charts
mv chart-2025-09-17-14-30-25-utc.yaml mercury-retrograde.yaml
$EDITOR mercury-retrograde.yaml                                 # Change name: field
ephem data sync                                                 # Creates backup of original timestamped version
```

Note: `ephem data sync` will recreate the original timestamped .yaml file because the chart still exists in ephem.db. This functions as a backup! It's generally poor science to discard data. But if you *really* want to go nuclear...

#### Deleting charts permanently ⚠️

Combine these commands:

```sh
ephem data delete N && rm ~/.local/share/ephem/charts/some-chart.yaml
```
