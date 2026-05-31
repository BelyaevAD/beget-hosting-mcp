---
title: "Управление MySQL по API"
source_url: https://beget.com/ru/kb/api/funkczii-upravleniya-mysql
payload_url: https://assets-site.beget.com/ru/kb/api/funkczii-upravleniya-mysql/_payload.json?1d2409a7-6569-40d6-898b-d89ff365e937
published_at: 2020-07-09T18:57:32+03:00
modified_at: 2025-09-02T12:04:11+03:00
section: mysql
---

# Управление MySQL по API

Source: [https://beget.com/ru/kb/api/funkczii-upravleniya-mysql](https://beget.com/ru/kb/api/funkczii-upravleniya-mysql)
## getList

### Описание

Метод возвращает список баз данных MySQL с их доступами.

### Пример вызова

```text
https://api.beget.com/api/mysql/getList?login=userlogin&passwd=password&output_format=json
```

### Пример ответа

```text
[
 {
 "name":"user_mydb",
 "size":"1",
 "accesses":[
 {
 "name":"localhost"
 }
 ]
 },
 {
 "name":"user_wp",
 "size":"44",
 "accesses":[
 {
 "name":"localhost"
 },
 {
 "name":"192.168.1.5"
 }
 ]
 }
]
```

## addDb

### Описание

Метод добавляет задание в очередь на создание новой базы данных MySql с заданным суффиксом и создает доступ для localhost с заданным паролем. Процесс создания базы данных может занимать несколько минут.

### Дополнительные параметры

- **suffix** – суффиксная часть имени базы данных. При передаче этого параметра нужно учитывать, что итоговый логин вида "login_suffix" должен быть не длиннее 16 символов;

- **password** – пароль для новой базы данных. Должен содержать не менее 6 символов.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/mysql/addDb?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"suffix":"newdb","password":"password"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/mysql/addDb?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22suffix%22%3A%22newdb%22%2C%22password%22%3A%22password%22%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.

## addAccess

### Описание

Метод добавляет заданный доступ к заданной базе данных MySql.

### Дополнительные параметры

- **suffix** – суффиксная часть логина. При передаче этого параметра нужно учитывать, что итоговый логин вида "login_suffix" должен быть не длиннее 16 символов;

- **access** – имя доступа - это может быть: _домен, IP, * или localhost_;

- **password** – пароль для нового доступа к базе данных. Должен содержать не менее 6 символов.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/mysql/addAccess?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"suffix":"newdb","access":"192.168.100.100","password":"newpassword"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/mysql/addAccess?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22suffix%22%3A%22newdb%22%2C%22access%22%3A%22192.168.100.100%22%2C%22password%22%3A%22newpassword%22%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.

## dropDb

### Описание

Этот метод управления MySQL по API удаляет заданную базу данных и все доступы к ней.

### Дополнительные параметры

- **suffix** – суффиксная часть имени базы данных.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/mysql/dropDb?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"suffix":"newdb"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/mysql/dropDb?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22suffix%22%3A%22newdb%22%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.

## dropAccess

### Описание

Метод удаляет заданный доступ у базы данных.

### Дополнительные параметры

- **suffix** – суффиксная часть имени базы данных;

- **access** – имя доступа - это может быть: _домен, IP, * или localhost_.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/mysql/dropAccess?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"suffix":"newdb","access":"localhost"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/mysql/dropAccess?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22suffix%22%3A%22newdb%22%2C%22access%22%3A%22localhost%22%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.

## changeAccessPassword

### Описание

Метод изменяет пароль на указанном доступе.

### Дополнительные параметры

- **suffix** – суффиксная часть имени базы данных;

- **access** – имя доступа - это может быть: _домен, IP, * или localhost_;

- **password** – пароль для нового доступа к базе данных. Должен содержать не менее 6 символов.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/mysql/changeAccessPassword?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"suffix":"newdb","access":"localhost","password":"newpassword"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/mysql/changeAccessPassword?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22suffix%22%3A%22newdb%22%2C%22access%22%3A%22localhost%22%2C%22password%22%3A%22newpassword%22%7D%0A
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.
