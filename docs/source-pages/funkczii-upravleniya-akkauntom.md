---
title: "Управление аккаунтом по API"
source_url: https://beget.com/ru/kb/api/funkczii-upravleniya-akkauntom
payload_url: https://assets-site.beget.com/ru/kb/api/funkczii-upravleniya-akkauntom/_payload.json?1d2409a7-6569-40d6-898b-d89ff365e937
published_at: 2020-07-09T12:59:15+03:00
modified_at: 2025-09-02T11:05:44+03:00
section: user
---

# Управление аккаунтом по API

Source: [https://beget.com/ru/kb/api/funkczii-upravleniya-akkauntom](https://beget.com/ru/kb/api/funkczii-upravleniya-akkauntom)
## getAccountInfo

### Описание

Метод возвращает информацию о тарифном плане пользователя, о некоторых параметрах сервера, на котором пользователь размещается в данный момент, и используемых лимитах на нем.

### Пример вызова

```text
https://api.beget.com/api/user/getAccountInfo?login=userlogin&passwd=password&output_format=json
```

### Пример ответа

```text
 "plan_name": "Great", // Имя тарифа
 "user_sites": 7, // Фактическое кол-во сайтов
 "plan_site": 25, // Максимальное кол-во сайтов
 "user_domains": 4, // Фактическое кол-во доменов
 "plan_domain": 2147483647, // Максимальное кол-во доменов
 "user_mysqlsize": 153, // Фактический объем БД MySQL
 "plan_mysql": 2147483647, // Максимальное кол-во БД MySQL
 "user_quota": 1283, // Размер использованной дисковой квоты
 "plan_quota": 10000, // Максимальный размер дисковой квоты
 "user_ftp": 6, // Фактическое кол-во FTP-аккаунтов
 "plan_ftp": 25, // Максимальное кол-во FTP-аккаунтов
 "user_mail": 18, // Фактическое кол-во почтовых ящиков
 "plan_mail": 2147483647, // Максимальное кол-во почтовых ящиков
 "user_bash": "\/bin\/bash", // Используемая командная оболочка
 "plan_cp": 400, // Максимальная допустимая нагрузка по аккаунту
 "user_rate_current": "12.66", // Текущая стоимость тарифного плана в сутки
 "user_is_year_plan": "0", // Используется ли годовая скидка
 "user_rate_year": 4620, // Текущая стоимость тарифа в год
 "user_rate_month": 385, // Текущая стоимость тарифа в месяц
 "user_balance": 1339.57, // Текущий баланс пользователя
 "user_days_to_block": 4865, // Количество дней до блокировки
 "server_apache_version": " Apache\/2.2.23 (Unix)", // Версия Apache
 "server_mysql_version": "5.1.68", // Версия MySQL
 "server_nginx_version": "nginx\/1.1.0", // Версия Nginx
 "server_perl_version": "v5.10.1", // Версия Perl
 "server_php_version": "5.2.17", // Версия PHP
 "server_python_version": "Python 2.6.6", // Версия Python
 "server_name": "germes", // Имя сервера
 "server_cpu_name": "24 * Intel(R) Xeon(R) CPU X5660 @ 2.80GHz", // Процессора
 "server_memory": "96747", // Кол-во оперативной памяти (Мб)
 "server_memorycurrent": 4944, // Кол-во используемой оперативной памяти
 "server_loadaverage": "4.05", // Текущая нагрузка Load Average
 "server_uptime": "18" // Аптайм
```

В некоторых полях (например, plan_domain) может стоять значение **2147483647** – это означает, что лимита на этот параметр не существует.

## toggleSsh

### Описание

Метод включает или выключает SSH, если нет дополнительного параметра ftplogin - для основного аккаунта, с ftplogin - для указанного ftp аккаунта.

### Дополнительные параметры

- **status** 1 – включить, 0 - выключить;

- **ftplogin** – login ftp аккаунта, если передан, включает\отключает доступ к ftp аккаунту по SSH, если не передан, включает\отключает доступ по SSH к основному аккаунту пользователя.

### Пример вызова

```text
https://api.beget.com/api/user/toggleSsh?login=userlogin&passwd=password&status=0&output_format=json

https://api.beget.com/api/user/toggleSsh?login=userlogin&passwd=password&status=1&ftplogin=ftploginname&output_format=json
```

### Пример ответа

```text
"status": "success",
"answer": {
		"status": "success",
		"result": [
		]
	}
```
