---
title: "Управление почтой по API"
source_url: https://beget.com/ru/kb/api/funkczii-dlya-raboty-s-pochtoj
payload_url: https://assets-site.beget.com/ru/kb/api/funkczii-dlya-raboty-s-pochtoj/_payload.json?1d2409a7-6569-40d6-898b-d89ff365e937
published_at: 2020-07-10T14:12:17+03:00
modified_at: 2025-09-02T12:14:14+03:00
section: mail
---

# Управление почтой по API

Source: [https://beget.com/ru/kb/api/funkczii-dlya-raboty-s-pochtoj](https://beget.com/ru/kb/api/funkczii-dlya-raboty-s-pochtoj)
## getMailboxList

### Описание

Метод возвращает все почтовые ящики на заданном домене.

### Дополнительные параметры

- **domain** – домен, почтовые ящики которого будут отображены (например, site.ru).

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/mail/getMailboxList?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"domain":"site.ru"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/mail/getMailboxList?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22domain%22%3A%22site.ru%22%7D
```

### Пример ответа

```text
[
 {
 "mailbox":"mailbox1",
 "domain":"site.ru",
 "spam_filter_status":1,
 "forward_mail_status":"no_forward"
 },
 {
 "mailbox":"test.mail",
 "domain":"site.ru",
 "spam_filter_status": 0,
 "forward_mail_status": "forward"
 },
 {
 "mailbox":"admin",
 "domain":"site.ru",
 "spam_filter_status":1,
 "forward_mail_status":"forward_and_delete"
 }
]
```

## changeMailboxPassword

### Описание

Метод изменяет пароль к заданному почтовому ящику.

### Дополнительные параметры

- **domain** – домен, на котором находится почтовый ящик (например, site.ru);

- **mailbox** – имя почтового ящика (например, info);

- **mailbox_password** – пароль для почтового ящика.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/mail/changeMailboxPassword?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"domain":"site.ru","mailbox":"info","mailbox_password":"password"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/mail/changeMailboxPassword?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22domain%22%3A%22site.ru%22%2C%22mailbox%22%3A%22info%22%2C%22mailbox_password%22%3A%22password%22%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.

## createMailbox

### Описание

Метод создает почтовый ящик на заданном домене.

### Дополнительные параметры

- **domain** – домен, на котором будет создан почтовый ящик (например, site.ru);

- **mailbox** – имя почтового ящика (например, info);

- **mailbox_password** – пароль для почтового ящика.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/mail/createMailbox?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"domain":"site.ru","mailbox":"info","mailbox_password":"password"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/mail/createMailbox?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22domain%22%3A%22site.ru%22%2C%22mailbox%22%3A%22info%22%2C%22mailbox_password%22%3A%22password%22%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.

## dropMailbox

### Описание

Метод удаляет почтовый ящик на заданном домене.

### Дополнительные параметры

- **domain** – домен, на котором находится почтовый ящик (например, site.ru);

- **mailbox** – имя почтового ящика (например, info).

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/mail/dropMailbox?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"domain":"site.ru","mailbox":"info"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/mail/dropMailbox?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22domain%22%3A%22site.ru%22%2C%22mailbox%22%3A%22info%22%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.

## changeMailboxSettings

### Описание

Метод устанавливает опции для почтового ящика.

### Дополнительные параметры

- **domain** – домен, на котором находится почтовый ящик (например, site.ru);

- **mailbox** – имя почтового ящика (например, info);

- **spam_filter_status** - статус работы спам-фильтра (0/1);

- **spam_filter** – уровень фильтрации спама (20 – по умолчанию, в данный момент параметр не актуален, оставлен для совместимости API);

- **forward_mail_status** – режим работы перенаправления для почтового ящика. Возможные значения:

- _no_forward_ – письма не перенаправляются;

- _forward_ – письма также перенаправляются на заданные почтовые ящики;

- _forward_and_delete_ – письма перенаправляются и удаляются из почтового ящика.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/mail/changeMailboxSettings?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"domain":"site.ru","mailbox":"info","spam_filter_status":1,"spam_filter":50,"forward_mail_status":"no_forward"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/mail/changeMailboxSettings?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22domain%22%3A%22site.ru%22%2C%22mailbox%22%3A%22info%22%2C%22spam_filter_status%22%3A1%2C%22spam_filter%22%3A50%2C%0A%22forward_mail_status%22%3A%22no_forward%22%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.

## forwardListAddMailbox

### Описание

Метод добавит почтовый ящик в список ящиков для пересылки.

### Дополнительные параметры

- **domain** – домен, на котором находится почтовый ящик (например, site.ru);

- **mailbox** – имя почтового ящика (например, info);

- **forward_mailbox** – почтовый ящик, на который будут перенаправляться письма.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/mail/forwardListAddMailbox?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"domain":"site.ru","mailbox":"info","forward_mailbox":"mail@yandex.ru"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/mail/forwardListAddMailbox?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22domain%22%3A%22site.ru%22%2C%22mailbox%22%3A%22info%22%2C%22forward_mailbox%22%3A%22%22mail%40yandex.ru%22%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.

## forwardListDeleteMailbox

### Описание

Метод удаляет почтовый ящик из списка ящиков для пересылки.

### Дополнительные параметры

- **domain** – домен, на котором находится почтовый ящик (например, site.ru);

- **mailbox** – имя почтового ящика (например, info);

- **forward_mailbox** – почтовый ящик, который будет удален из списка пересылки.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/mail/forwardListDeleteMailbox?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"domain":"site.ru","mailbox":"info","forward_mailbox":"mail@yandex.ru"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/mail/forwardListDeleteMailbox?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22domain%22%3A%22site.ru%22%2C%22mailbox%22%3A%22info%22%2C%22forward_mailbox%22%3A%22%22mail%40yandex.ru%22%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.

## forwardListShow

### Описание

Метод возвращает список пересылки для заданного почтового ящика.

### Дополнительные параметры

- **domain** – домен, на котором находится почтовый ящик (например, site.ru);

- **mailbox** – имя почтового ящика (например, info).

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/mail/forwardListShow?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"domain":"site.ru","mailbox":"info"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/mail/forwardListShow?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22domain%22%3A%22site.ru%22%2C%22mailbox%22%3A%22info%22%7D
```

### Пример ответа

```text
[
 {
 "forward_mailbox":"admin@domain.ru"
 },
 {
 "forward_mailbox":"webmaster@site.com"
 }
]
```

## setDomainMail

### Описание

Метод устанавливает почту домена.

### Дополнительные параметры

- **domain** – домен, для которого будет установлена с помощью API почта домена (например, site.ru);

- **domain_mailbox** – почтовый ящик, который будет установлен в качестве почты домена (например, mail@site.ru).

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/mail/setDomainMail?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"domain":"site.ru","domain_mailbox":"mail@site.ru"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/mail/setDomainMail?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22domain%22%3A%22site.ru%22%2C%22domain_mailbox%22%3A%22mail%40site.ru%22%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.

## clearDomainMail

### Описание

Метод сбрасывает почту домена.

### Дополнительные параметры

- **domain** – домен, для которого будет сброшена почта домена (например, site.ru).

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/mail/clearDomainMail?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"domain":"site.ru"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/mail/clearDomainMail?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22domain%22%3A%22site.ru%22%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.
