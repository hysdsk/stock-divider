# stock-divider
[松井証券Web](https://ca.image.jp/matsui/)の株式分割情報を基にDBに適用する。

## 分割手順
作業前に必ずバックアップを取得する。

```
$ mysqldump [--protocol=tcp] -h <host> -u <user> -p <database> > dump.`date "+%Y%m%d"`.txt
```
前回分割を適用した日を確認する。

```
mysql> select updated_at from symbol_divide_info order by updated_at desc limit 1;
```

今回適用する予定の分割情報を確認する。
```
mysql> select * from symbol_divide_info where right_last_date <= {今日} and right_last_date > {前回適用日} order by right_last_date;
```

分割情報を適用する。
```
$ python3 -m stock-divider
```


今回適用した銘柄を確認する。
```
mysql> select distinct symbol_code from symbol_daily_info where updated_at >= {今日};
```
