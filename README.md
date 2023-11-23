# stock-divider
[松井証券Web](https://ca.image.jp/matsui/)の株式分割情報を基にDBに適用する。

作業前に必ずバックアップを取得する。

```
$ mysqldump [--protocol=tcp] -h <host> -u <user> -p <database> > dump.`date "+%Y%m%d"`.txt
```

分割情報を適用する。
```
$ python3 -m stock-divider
```

以降はMySQLにログインして確認する。

前回適用した日から今日までの分割情報を確認する。
```
mysql> select * from symbol_divide_info where right_last_date <= {今日} and right_last_date > {前回適用日} order by right_last_date;
```

今回の作業で更新された銘柄を確認する。
```
mysql> select distinct symbol_code from symbol_daily_info where updated_at >= {今日};
```
