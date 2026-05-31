---
title: "Управление Cron по API"
source_url: https://beget.com/ru/kb/api/funkczii-upravleniya-cron
payload_url: https://assets-site.beget.com/ru/kb/api/funkczii-upravleniya-cron/_payload.json?1d2409a7-6569-40d6-898b-d89ff365e937
published_at: 2020-07-09T17:39:02+03:00
modified_at: 2025-09-02T11:42:42+03:00
section: cron
---

# Управление Cron по API

Source: [https://beget.com/ru/kb/api/funkczii-upravleniya-cron](https://beget.com/ru/kb/api/funkczii-upravleniya-cron)
## getList

### Описание

Метод возвращает список всех задач CronTab.

### Пример вызова

```text
https://api.beget.com/api/cron/getList?login=userlogin&passwd=password&output_format=json
```

### Пример ответа

```text
 [
 {
 "row_number": "1000", // ID задания
 "minutes": "*", // Минуты
 "hours": "*", // Часы
 "days": "*", // Дни
 "months": "10,11", // Месяцы
 "weekdays": "*", // Дни недели
 "command": "wget -O \/dev\/null http:\/\/wget vk.com", // Команда
 "is_hidden": "1" // статус задания (активно/не активно)
 }
 ]
```

Возвращается двумерный массив, каждая строка которого описывает задание Cron.

## add

### Описание

Метод добавит новое задание. После добавления задание будет активно.

### Дополнительные параметры

- **minutes** – минуты могут быть от 0 до 59;

- **hours** – часы могут быть от 0 до 23;

- **days** – день месяца может быть от 1 до 31;

- **months** – месяц может быть от 1 до 12;

- **weekdays** – день недели может быть от 0 до 7, где 0 и 7 – воскресенье;

- **command** – команда.

Можно конфигурировать CronTab для выполнения задач не только в определенное время, но и ежеминутно, ежечасно, ежедневно, еженедельно или ежемесячно, используя комбинацию */x

- */5 * * * * – запускать команду каждые пять минут;

- */3 * * * – запускать каждые три часа;

- 0 12-16 * * * – запускать команду каждый час с 12 до 16 (в 12, 13, 14, 15 и 16);

- 0 12,16,18 * * * – запускать команду каждый час в 12, 16 и 18 часов.

### Пример запуска php-скрипта test.php каждую минуту

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/cron/add?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"minutes":"*/1","hours":"*","days":"*","months":"*","weekdays":"*","command":"/usr/bin/php ~/site.ru/public_html/test.php"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https%3A%2F%2Fapi.beget.com%2Fapi%2Fcron%2Fadd%3Flogin%3Duserlogin%26passwd%3Dpassword%26input_format%3Djson%26output_format%3Djson%26input_data%3D%7B%22minutes%22%3A%22*%2F1%22%2C%22hours%22%3A%22*%22%2C%22days%22%3A%22*%22%2C%22months%22%3A%22*%22%2C%22weekdays%22%3A%22*%22%2C%22command%22%3A%22%2Fusr%2Fbin%2Fphp%20~%2Fsite.ru%2Fpublic_html%2Ftest.php%22%7D
```

### Пример ответа

```text
{"status":"success","answer":{"status":"success","result":{"row_number":941671}}}
```

### Пример запуска php-скрипта test.pl 13 января в 10 часов 1 минуту, если этот день вторник

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/cron/add?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"minutes":"1","hours":"10","days":"13","months":"1","weekdays":"2","command":"/usr/bin/php%20~/site.ru/public_html/test.php"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https%3A%2F%2Fapi.beget.com%2Fapi%2Fcron%2Fadd%3Flogin%3Duserlogin%26passwd%3Dpassword%26input_format%3Djson%26output_format%3Djson%26input_data%3D%7B%22minutes%22%3A%221%22%2C%22hours%22%3A%2210%22%2C%22days%22%3A%2213%22%2C%22months%22%3A%221%22%2C%22weekdays%22%3A%222%22%2C%22command%22%3A%22%2Fusr%2Fbin%2Fphp%2520~%2Fsite.ru%2Fpublic_html%2Ftest.php%22%7D
```

### Пример ответа

```text
{"status":"success","answer":{"status":"success","result":{"row_number":941471}}}
```

## edit

### Описание

Метод изменит указанное задание.

### Дополнительные параметры

- **id** – идентификатор задания;

- **minutes** – минуты;

- **hours** – часы;

- **days** – дни;

- **months** – месяцы;

- **weekdays** – дни недели;

- **command** – команда.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/cron/edit?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"id":"123456","minutes":"*","hours":"*","days":"*","months":"*","weekdays":"*","command":"wget -O \/dev\/null http:\/\/wget vk.com"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/cron/add?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22minutes%22%3A%22*%22%2C%22hours%22%3A%22*%22%2C%22days%22%3A%22*%22%2C%22months%22%3A%22*%22%2C%22weekdays%22%3A%22*%22%2C%22command%22%3A%22wget%20-O%20%5C%2Fdev%5C%2Fnull%20http%3A%5C%2F%5C%2Fwget%20vk.com%22%7D
```

### Пример ответа

```text
"row_number": 123456
```

Возвращается ID задания (идентификатор задания уникален в рамках одного пользователя).

## delete

### Описание

Метод удалит задание с указанным ID.

### Дополнительные параметры

- **row_number** – ID задания, тип int.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/cron/delete?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"row_number":1000}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/cron/delete?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22row_number%22%3A1000%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.

## changeHiddenState

### Описание

Метод изменит статус задания.

### Дополнительные параметры

- **row_number** – ID задания, тип int;

- **is_hidden** – статус задания (активное / не активное), тип boolean: 0 или 1.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/cron/changeHiddenState?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"row_number":1000,"is_hidden":0}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/cron/changeHiddenState?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22row_number%22%3A1000%2C%22is_hidden%22%3A0%7D
```

### Пример ответа

```text
 "row_number": 4
```

Как видим, этот метод управления Cron по API позволяет поменять статус задания.

## getEmail

### Описание

Метод возвращает email, на который приходит вывод выполненных заданий.

### Пример вызова

```text
https://api.beget.com/api/cron/getEmail?login=userlogin&passwd=password&output_format=json
```

### Пример ответа

```text
 admin@domain.ru
```

Если email не задан, то возвращается NULL.

## setEmail

### Описание

Метод устанавливает email, на который будет приходить вывод выполненных заданий.

### Дополнительные параметры

- **email** – Email или пустая строка.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/cron/setEmail?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"email":"admin@domain.ru"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/cron/setEmail?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22email%22%3A%22admin%40domain.ru%22%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.
