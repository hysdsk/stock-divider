# stock-divider
[松井証券Web](https://ca.image.jp/matsui/)の株式分割情報を基にDBに適用する。
作業前に必ずバックアップを取得すること。

```
# バックアップ取得
$ mysqldump [--protocol=tcp] -h <host> -u <user> -p <database> > dump.`date "+%Y%m%d"`.txt

# 分割適用
$ python3 -m stock-divider
```
