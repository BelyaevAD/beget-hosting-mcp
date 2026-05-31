---
title: "Сбор статистики по API"
source_url: https://beget.com/ru/kb/api/funkczii-dlya-sbora-statistiki
payload_url: https://assets-site.beget.com/ru/kb/api/funkczii-dlya-sbora-statistiki/_payload.json?1d2409a7-6569-40d6-898b-d89ff365e937
published_at: 2020-07-10T16:11:54+03:00
modified_at: 2026-05-03T19:05:58+03:00
section: stat
---

# Сбор статистики по API

Source: [https://beget.com/ru/kb/api/funkczii-dlya-sbora-statistiki](https://beget.com/ru/kb/api/funkczii-dlya-sbora-statistiki)
## getSiteListLoad

### Описание

Метод возвращает информацию о средней нагрузке на сайтах пользователя за последний месяц.

### Пример вызова

```text
// корректный пример вызова
https://api.beget.com/api/stat/getSitesListLoad?login=user&passwd=password&output_format=json
```

### Пример ответа

```text
[
 {
 "name": "sitename.ru",
 "id": "299163",
 "cp": "195.257188"
 },
 {
 "name": "sitename2.ru",
 "id": "299176",
 "cp": "97.168125"
 },
 {
 "name": "sitename3.ru",
 "id": "307286",
 "cp": "93.905937"
 }
]
```

Возвращается список сайтов и средняя нагрузка по ним (по убыванию).
ID сайта уникален в рамках одного пользователя.

## getDbListLoad

### Описание

Метод возвращает информацию о средней нагрузке на базах данных пользователя за последний месяц.

### Пример вызова

```text
// корректный пример вызова
https://api.beget.com/api/stat/getDbListLoad?login=user&passwd=password&output_format=json
```

### Пример ответа

```text
[
 {
 "name": "base_name",
 "cp": "2895.257188"
 },
 {
 "name": "base_name2",
 "cp": "1500.168125"
 },
 {
 "name": "base_name3",
 "cp": "856.905937"
 }
]
```

Возвращается список имен баз данных и средняя нагрузка по ним (по убыванию).
name – имя базы уникально в рамках одного пользователя.

## getSiteLoad

### Описание

Метод возвращает детальную информацию о нагрузке на указанном сайте (нагрузка по дням и часам).

### Дополнительные параметры

- **site_id** – идентификатор сайта.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/stat/getSiteLoad?login=user&passwd=password&output_format=json&input_format=json&input_data={"site_id":296164}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/stat/getSiteLoad?login=user&passwd=password&output_format=json&input_format=json&input_data={%22site_id%22:296164}
```

### Пример ответа

```text
{
 "days": [
 {
 "value": "0.35",
 "date": "2014-05-04"
 },
 {
 "value": "0.47",
 "date": "2014-05-05"
 },
 {
 "value": "0.14",
 "date": "2014-05-06"
 },
 {
 "value": "0.09",
 "date": "2014-05-07"
 }
 ...
 ],
 "hours": [
 {
 "value": "0.02",
 "date": "2014-06-02 18:00:00"
 },
 {
 "value": "0.00",
 "date": "2014-06-02 19:00:00"
 },
 {
 "value": "0.00",
 "date": "2014-06-02 20:00:00"
 },
 {
 "value": "0.00",
 "date": "2014-06-02 21:00:00"
 }
 ...
 ]
}
```

Возвращается список с нагрузкой за последние 30 дней (по датам).
А также доступна статистика API в виде списка (по часам).

## getDbLoad

### Описание

Метод возвращает детальную информацию о нагрузке на указанной базе данных MySQL.

### Дополнительные параметры

- **db_name** – имя базы данных.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/stat/getDbLoad?login=user&passwd=password&output_format=json&input_format=json&input_data={"db_name":"login_dbname"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/stat/getDbLoad?login=user&passwd=password&output_format=json&input_format=json&input_data=%7B%22db_name%22%3A%22login_dbname%22%7D
```

### Пример ответа

```text
{
 "hours": [
 {
 "cpu_time": "0",
 "date": "2014-06-02 20:00:00"
 },
 {
 "cpu_time": "0",
 "date": "2014-06-02 21:00:00"
 },
 {
 "cpu_time": "0",
 "date": "2014-06-02 22:00:00"
 },
 {
 "cpu_time": "0",
 "date": "2014-06-03 15:00:00"
 },
 {
 "cpu_time": "0",
 "date": "2014-06-03 16:00:00"
 },
 {
 "cpu_time": "0",
 "date": "2014-06-03 17:00:00"
 },
 {
 "cpu_time": "0",
 "date": "2014-06-03 18:00:00"
 },
 {
 "cpu_time": "0",
 "date": "2014-06-03 19:00:00"
 }
 ...
 ],
 "days": [
 {
 "cpu_time": "0",
 "date": "2014-05-04"
 },
 {
 "cpu_time": "0",
 "date": "2014-05-13"
 },
 {
 "cpu_time": "0",
 "date": "2014-05-20"
 },
 {
 "cpu_time": "0",
 "date": "2014-05-21"
 },
 {
 "cpu_time": "31",
 "date": "2014-05-22"
 },
 {
 "cpu_time": "1",
 "date": "2014-05-23"
 },
 {
 "cpu_time": "0",
 "date": "2014-05-24"
 },
 {
 "cpu_time": "0",
 "date": "2014-05-25"
 },
 {
 "cpu_time": "0",
 "date": "2014-06-03"
 }
 ...
 ],
 "size_days": [
 {
 "date": "2014-05-04",
 "size": "229512"
 },
 {
 "date": "2014-05-05",
 "size": "229512"
 },
 {
 "date": "2014-05-06",
 "size": "229512"
 },
 {
 "date": "2014-05-07",
 "size": "229512"
 },
 {
 "date": "2014-05-08",
 "size": "229512"
 },
 {
 "date": "2014-05-09",
 "size": "229512"
 },
 {
 "date": "2014-05-10",
 "size": "229512"
 },
 {
 "date": "2014-05-11",
 "size": "229512"
 },
 {
 "date": "2014-05-23",
 "size": "229512"
 },
 {
 "date": "2014-05-24",
 "size": "229512"
 },
 {
 "date": "2014-05-25",
 "size": "229512"
 },
 {
 "date": "2014-05-26",
 "size": "229512"
 }
 ...
 ]
}
```

Возвращается список с нагрузкой за последние 30 дней (по датам).
Список с нагрузкой за последние сутки (по часам).
Список с размером базы (в байтах) за последние 30 дней (по датам).
