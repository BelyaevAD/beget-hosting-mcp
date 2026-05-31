---
title: "Управление FTP по API"
source_url: https://beget.com/ru/kb/api/funkczii-upravleniya-ftp
payload_url: https://assets-site.beget.com/ru/kb/api/funkczii-upravleniya-ftp/_payload.json?1d2409a7-6569-40d6-898b-d89ff365e937
published_at: 2020-07-09T18:12:56+03:00
modified_at: 2025-09-02T12:01:55+03:00
section: ftp
---

# Управление FTP по API

Source: [https://beget.com/ru/kb/api/funkczii-upravleniya-ftp](https://beget.com/ru/kb/api/funkczii-upravleniya-ftp)
## getList

Метод возвращает список дополнительных FTP-аккаунтов с их домашними директориями.

### Пример вызова

```text
https://api.beget.com/api/ftp/getList?login=userlogin&passwd=password&output_format=json
```

### Пример ответа

```text
[
 {
 "login":"user_acc1",
 "homedir":"\/public_html"
 },
 {
 "login":"user_siteru",
 "homedir":"\/site.ru\/public_html"
 }
]
```

## add

Метод добавляет новый FTP аккаунт.

### Дополнительные параметры

- **suffix** – суффиксная часть логина. При передаче этого параметра нужно учитывать, что итоговый логин вида "login_suffix" должен быть не длиннее 17 символов.;

- **homedir** – путь до домашней директории создаваемого аккаунта. Он начинается со слеша. (например, /site.ru/public_html);

- **password** – пароль для нового ftp-аккаунта.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/ftp/add?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"suffix":"ftp1","homedir":"/site.ru/public_html","password":"password"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/ftp/add?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22suffix%22%3A%22ftp1%22%2C%22homedir%22%3A%22%2Fsite.ru%2Fpublic_html%22%2C%22password%22%3A%22password%22%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.

## changePassword

Метод производит смену пароля для дополнительного FTP-аккаунта.

### Дополнительные параметры

- **suffix** – суффиксная часть логина. При передаче этого параметра нужно учитывать, что итоговый логин вида "login_suffix" должен быть не длиннее 17 символов.;

- **password** – новый пароль для ftp-аккаунта.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/ftp/changePassword?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"suffix":"ftp1","password":"newpassword"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/ftp/changePassword?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22suffix%22%3A%22ftp1%22%2C%22password%22%3A%22newpassword%22%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.

## delete

Метод удаляет дополнительный FTP-аккаунт с заданным суффиксом.

### Дополнительные параметры

- **suffix** – суффиксная часть логина. При передаче этого параметра нужно учитывать, что итоговый логин вида "login_suffix" должен быть не длиннее 17 символов.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/ftp/delete?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"suffix":"ftp1"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/ftp/delete?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22suffix%22%3A%22ftp1%22%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.
