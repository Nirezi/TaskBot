# What's this?
discord上で課題やタスクの管理を行うためのBot

## テーブル構造
| Field       | Type    | Null | Key | Default | Extra | Comment           |
|-------------|---------|------|-----|---------|-------|-------------------|
| id          | INTEGER | NO   | PRI | NULL    |       | 課題ID              |
| title       | TEXT    | NO   |     | NULL    |       | 課題タイトル            |
| description | TEXT    | NO   |     | NULL    |       | 課題の詳細             |
| deadline    | INTEGER | NO   |     | NULL    |       | 締め切り日時(Unix time) |