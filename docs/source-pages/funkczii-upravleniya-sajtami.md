---
title: "Управление сайтами по API"
source_url: https://beget.com/ru/kb/api/funkczii-upravleniya-sajtami
payload_url: https://assets-site.beget.com/ru/kb/api/funkczii-upravleniya-sajtami/_payload.json?1d2409a7-6569-40d6-898b-d89ff365e937
published_at: 2020-07-09T19:18:08+03:00
modified_at: 2025-09-02T12:07:06+03:00
section: site
---

# Управление сайтами по API

Source: [https://beget.com/ru/kb/api/funkczii-upravleniya-sajtami](https://beget.com/ru/kb/api/funkczii-upravleniya-sajtami)
## getList

### Описание

Метод возвращает список сайтов. Если к сайту прилинкованы домены, то они также будут возвращены.

### Пример вызова

```text
https://api.beget.com/api/site/getList?login=userlogin&passwd=password&output_format=json
```

### Пример ответа

```text
[
 {
 "id":"125",
 "path":"site.ru\/public_html",
 "domains":[
 {
 "id":"12345",
 "fqdn":"site.ru"
 "php_version":"8.2",
 "http_version":2,
 "ssl":true,
 "ssl_status":"wle_set",
 "nginx_template":"default",
 "redis_session":false

 }
 ]
 },
 {
 "id":"124",
 "path":"vk.com\/public_html",
 "domains":[

 ]
 },
 {
 "id":"123",
 "path":"mysite\/public_html",
 "domains":[

 ]
 }
]
```

ID сайта уникален в рамках одного пользователя.

## add

### Описание

Метод создает новый сайт с заданным именем.

### Дополнительные параметры

- **name** – имя директории с сайтом (например, site.ru).

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/site/add?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"name":"site.ru"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/site/add?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22name%22%3A%22site.ru%22%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения. В случае успешного ответа полный путь к директории с сайтом будет _name/public_html_.

## delete

### Описание

Метод удаляет сайт. Если к сайту были прилинкованы домены, то они будут отлинкованы от него.

### Дополнительные параметры

- **id** – id сайта, тип int.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/site/delete?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"id":10}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/site/delete?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22id%22%3A10%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.

## linkDomain

### Описание

Метод прилинковывает домен к сайту.

### Дополнительные параметры

- **domain_id** – id домена. Получить уникальный id домена можно функцией domain/getList;

- **site_id** – id сайта.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/site/linkDomain?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"domain_id":100,"site_id":10}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/site/linkDomain?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22domain_id%22%3A100%2C%22site_id%22%3A10%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения. После выполнения операции сайт начнет открываться по доменному имени в течение 5–10 минут.

## unlinkDomain

### Описание

Метод отлинковывает домен от сайта.

### Дополнительные параметры

- **domain_id** – id домена. Получить уникальный id домена можно функцией domain/getList.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/site/unlinkDomain?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"domain_id":100}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/site/unlinkDomain?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22domain_id%22%3A100%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.

## freeze

### Описание

Метод запрещает изменение файлов сайта.

### Дополнительные параметры

- **id** – id сайта. Получить уникальный id сайта можно функцией site/getList;

- **excludedPaths** – список путей, в которых будет разрешено изменение файлов.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/site/freeze?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"id": 100, "excludedPaths": ["tmp", "cache"]}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/site/freeze?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22id%22%3A+100%2C+%22excludedPaths%22%3A+%5B%22tmp%22%2C+%22cache%22%5D%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения. Задание помещается в очередь и выполняется в течение 5–10 минут в зависимости от размера сайта.

## unfreeze

### Описание

Метод разрешает изменение файлов сайта.

### Дополнительные параметры

- **id** – id сайта. Получить уникальный id сайта можно функцией site/getList.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/site/unfreeze?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"id": 100}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/site/unfreeze?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7b%22id%22%3a+100%7d
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения. Задание помещается в очередь и выполняется в течение 5–10 минут в зависимости от размера сайта.

## isSiteFrozen

### Описание

Метод возвращает текущий статус сайта – доступно ли редактирование файлов.

### Дополнительные параметры

- **site_id** – id сайта. Получить уникальный id сайта можно функцией site/getList.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/site/isSiteFrozen?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"site_id": 100}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/site/isSiteFrozen?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22site_id%22%3A+100%7D
```

### Пример ответа

```text
"status": "success",
"answer": {
		"status": "success",
		"result": true
}
```
