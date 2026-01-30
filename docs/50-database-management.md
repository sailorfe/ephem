# Database Management

Besides the `--save` option to `now` and `cast`, the `data` command lets you interact with your saved chart database. It has the following subcommands:

- `data view`: View database.
- `data load N`: Re-generate a chart from saved input data.
- `data delete N`: Delete chart.
- `data sync`: Sync YAML charts with database; see [Advanced Usage](./60-advanced-usage.md).

Each chart in your database has a unique integer ID that you will need to know to interact with your charts. The first command you should run is `data view`.

```
$ ephem data view

[1] Jean Cremers
   UTC:     1957-03-14T18:55:00+00:00
   Local:   1957-03-14T19:55:00+01:00
   Lat:     52.0, Lng: 6.0

[2] Kevin DeCapite
   UTC:     1976-11-29T17:32:00+00:00
   Local:   1976-11-29T12:32:00-05:00
   Lat:     41.3919, Lng: -81.7286

[3] Walter Pullen
   UTC:     1971-11-19T19:01:00+00:00
   Local:   1971-11-19T11:01:00-08:00
   Lat:     47.6, Lng: -122.33

[4] Jeon Soyeon
   UTC:     1998-08-26T08:20:00+00:00
   Local:   1998-08-26T17:20:00+09:00
   Lat:     37.488167, Lng: 127.085472

[5] Nick Cave
   UTC:     1957-09-22T02:20:00+00:00
   Local:   1957-09-22T12:20:00+10:00
   Lat:     -36.25, Lng: 142.416667
```

- You can store as many charts as your local storage allows, but scrolling through the output can get tedious.
- The ID #'s are permanent. If you delete charts 2-4, the sequence will look like `1, 5`. This is fine!
