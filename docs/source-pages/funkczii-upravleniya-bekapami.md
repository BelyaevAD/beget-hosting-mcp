---
title: "Управление бэкапами по API"
source_url: https://beget.com/ru/kb/api/funkczii-upravleniya-bekapami
payload_url: https://assets-site.beget.com/ru/kb/api/funkczii-upravleniya-bekapami/_payload.json?1d2409a7-6569-40d6-898b-d89ff365e937
published_at: 2020-07-09T15:57:51+03:00
modified_at: 2025-09-02T11:31:55+03:00
section: backup
---

# Управление бэкапами по API

Source: [https://beget.com/ru/kb/api/funkczii-upravleniya-bekapami](https://beget.com/ru/kb/api/funkczii-upravleniya-bekapami)
## getFileBackupList

Метод возвращает доступный список резервных файловых копий.

### Пример вызова

```text
https://api.beget.com/api/backup/getFileBackupList?login=userlogin&passwd=password&output_format=json
```

### Пример ответа

```text
[
 {
 "backup_id": 14508595,
 "date": "2014-11-05 01:05:09"
 },
 {
 "backup_id": 14216570,
 "date": "2014-10-31 03:13:49"
 },
 {
 "backup_id": 14132477,
 "date": "2014-10-30 00:56:25"
 },
 {
 "backup_id": 14077266,
 "date": "2014-10-28 01:33:42"
 },
 {
 "backup_id": 14009305,
 "date": "2014-10-26 01:38:26"
 },
 {
 "backup_id": 13574406,
 "date": "2014-10-16 06:13:29"
 }
 ]
```

## getMysqlBackupList

Метод возвращает доступный список резервных копий баз mysql.

### Пример вызова

```text
https://api.beget.com/api/backup/getMysqlBackupList?login=userlogin&passwd=password&output_format=json
```

### Пример ответа

```text
[
 {
 "backup_id": 14508571,
 "date": "2014-11-05 01:04:16"
 },
 {
 "backup_id": 14216543,
 "date": "2014-10-31 03:12:44"
 },
 {
 "backup_id": 14132466,
 "date": "2014-10-30 00:55:43"
 },
 {
 "backup_id": 14077252,
 "date": "2014-10-28 01:31:53"
 },
 {
 "backup_id": 14009290,
 "date": "2014-10-26 01:28:59"
 },
 {
 "backup_id": 13713103,
 "date": "2014-10-19 05:11:13"
 },
 {
 "backup_id": 13574391,
 "date": "2014-10-16 05:59:31"
 }
 ]
```

## getFileList

Метод возвращает список файлов и директорий из резервной копии по заданному пути и идентификатору.

### Дополнительные параметры

- **backup_id** – идентификатор резервной копии backup_id, если не задан – значит листинг идет по текущей копии;

- **path** – путь от корня домашней директории (например "/site.ru/public_html").

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/backup/getFileList?login=userlogin&passwd=password&output_format=json&input_format=json&input_data={"path":"/site.ru/public_html","backup_id":14508595}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/backup/getFileList?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22path%22%3A%22%2Fsite.ru%2Fpublic_html%22%2C%22backup_id%22%3A14508595%7D
```

### Пример ответа

```text
[
 {
 "name": ".cache",
 "is_dir": 1,
 "mtime": "2012-12-25 18:35:05",
 "size": 4096
 },
 {
 "name": ".ssh",
 "is_dir": 1,
 "mtime": "2014-08-06 13:59:14",
 "size": 4096
 },
 {
 "name": "ftputil",
 "is_dir": 1,
 "mtime": "2014-08-07 13:06:09",
 "size": 4096
 {
 "name": "testlogo.png",
 "is_dir": 0,
 "mtime": "2013-02-13 11:02:13",
 "size": 18623
 },
 {
 "name": "textarea.js",
 "is_dir": 0,
 "mtime": "2013-04-05 18:14:18",
 "size": 1321
 },
 {
 "name": "tree-bottom.png",
 "is_dir": 0,
 "mtime": "2013-04-05 18:14:18",
 "size": 976
 },
 {
 "name": "update.php",
 "is_dir": 0,
 "mtime": "2014-01-16 15:56:36",
 "size": 25457
 }
 ]
```

Возвращается массив объектов, каждый объект состоит из следующих элементов:

- **name** – имя файла или папки;

- **is_dir** – признак файл это (0) или папка (1);

- **mtime** – время создания файла в формате "Y-m-d H:i:s";

- **size** – размер в байтах.

## getMysqlList

Метод возвращает список баз данных из резервной копии по заданному идентификатору.

### Дополнительные параметры

- **backup_id** – идентификатор резервной копии backup_id, если не задан – значит листинг идет по текущей копии.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/backup/getMysqlList?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"backup_id":14216543}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/backup/getMysqlList?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22backup_id%22%3A14216543%7D
```

### Пример ответа

```text
[
 "db_test111",
 "db_test",
 "db_opca2",
 "db_btrx"
 ]
```

Возвращается список имен баз данных.

## restoreFile

Метод создает заявку на восстановление данных из резервной копии по заданному пути и резервной копии.

### Дополнительные параметры

- **backup_id** – идентификатор резервной копии backup_id;

- **paths** – массив (одно или несколько значений) путей для восстановления от корня домашней директории (например "/site.ru/public_html").

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/backup/restoreFile?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"backup_id":14508595,"paths":["/site.ru/public_html/","/site2.ru/public_html/"]}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/backup/restoreFile?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22backup_id%22%3A14508595%2C%22paths%22%3A%5B%22%2Fsite.ru%2Fpublic_html%2F%22%2C%22%2Fsite2.ru%2Fpublic_html%2F%22%5D%7D
```

### Пример ответа

```text
true
```

Как видим, этот метод управления бэкапами по API позволяет создать заявку на восстановление данных из резервной копии по нужному пути.

## restoreMysql

Метод создает заявку на восстановление БД из резервной копии по заданному имени БД и идентификатору резервной копии.

### Дополнительные параметры

- **backup_id** – идентификатор резервной копии backup_id;

- **bases** – массив (одно или несколько значений) имен баз данных MySQL для восстановления.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/backup/restoreMysql?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"backup_id":"14132466","bases":["db_test","db_test2"]}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/backup/restoreMysql?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22backup_id%22%3A%2214132466%22%2C%22bases%22%3A%5B%22db_test%22%2C%22db_test2%22%5D%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.

## downloadFile

Метод создает заявку на загрузку и выкладывание данных из резервной копии в корень аккаунта.

### Дополнительные параметры

- **backup_id** – идентификатор резервной копии backup_id (необязательный), если не указан то используется текущая копия;

- **paths** – массив (одно или несколько значений) путей для восстановления от корня домашней директории (например "/site.ru/public_html").

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/backup/downloadFile?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"backup_id":14508595,"paths":["/site.ru/public_html/","/site2.ru/public_html/"]}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/backup/downloadFile?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22backup_id%22%3A14508595%2C%22paths%22%3A%5B%22%2Fsite.ru%2Fpublic_html%2F%22%2C%22%2Fsite2.ru%2Fpublic_html%2F%22%5D%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.

## downloadMysql

Метод создает заявку на загрузку и выкладывание данных из резервной копии в корень аккаунта.

### Дополнительные параметры

- **backup_id** – идентификатор резервной копии backup_id (необязательный), если не указан то используется текущая копия;

- **bases** – массив (одно или несколько значений) имен баз данных MySQL для восстановления.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/backup/downloadMysql?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"backup_id":14216543,"bases":["db_test", "db_test2"]}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/backup/downloadMysql?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22backup_id%22%3A14216543%2C%22bases%22%3A%5B%22db_test%22%2C+%22db_test2%22%5D%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.

## getLog

Метод возвращает список и статусы заданий по восстановлению и загрузке.

### Пример вызова

```text
https://api.beget.com/api/backup/getLog?login=userlogin&passwd=password&output_format=json
```

### Пример ответа

```text
[
 {
 "id": 80240,
 "operation": "download",
 "type": "download_mysql",
 "date_create": "2014-11-05 14:22:13",
 "target_list": [
 "db_opca2"
 ],
 "status": "success"
 },
 {
 "id": 80239,
 "operation": "download",
 "type": "download_file",
 "date_create": "2014-11-05 14:17:11",
 "target_list": [
 "/site.ru/public_html",
 "/site2.ru/public_html"
 ],
 "status": "success"
 },
 {
 "id": 32904,
 "operation": "restore",
 "type": "restore_mysql",
 "date_create": "2014-11-05 14:00:44",
 "target_list": [
 "db_test",
 "db_opca2"
 ],
 "status": "success"
 },
 {
 "id": 32901,
 "operation": "restore",
 "type": "restore_file",
 "date_create": "2014-11-05 13:55:20",
 "target_list": [
 "/site.ru/public_html",
 "/site2.ru/public_html"
 ],
 "status": "success"
 },
 {
 "id": 13457,
 "operation": "restore",
 "type": "restore_file",
 "date_create": "2014-06-23 17:18:21",
 "target_list": [
 "/site.ru/public_html",
 "/site2.ru/public_html"
 ],
 "status": "success"
 }
 ]
```

Возвращается массив объектов, каждый объект состоит из следующих элементов:

- **id** – идентификатор заявки восстановления / скачивания;

- **operation** – действие восстановление (restore), скачивание (download);

- **type** – подробное действие и тип данных restore / download и file / mysql;

- **date_create** – время создания заявки в формате "Y-m-d H:i:s";

- **target_list** – массив элементов в заявке (файлов или баз данных);

- **status** – статус выполнения.
