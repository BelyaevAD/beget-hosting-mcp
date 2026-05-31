---
title: "Управление доменами по API"
source_url: https://beget.com/ru/kb/api/funkczii-dlya-raboty-s-domenami
payload_url: https://assets-site.beget.com/ru/kb/api/funkczii-dlya-raboty-s-domenami/_payload.json?1d2409a7-6569-40d6-898b-d89ff365e937
published_at: 2020-07-10T13:31:09+03:00
modified_at: 2025-09-02T12:10:47+03:00
section: domain
---

# Управление доменами по API

Source: [https://beget.com/ru/kb/api/funkczii-dlya-raboty-s-domenami](https://beget.com/ru/kb/api/funkczii-dlya-raboty-s-domenami)
## getList

### Описание

Метод возвращает список доменов на аккаунте пользователя.

### Пример вызова

```text
https://api.beget.com/api/domain/getList?login=userlogin&passwd=password&output_format=json
```

### Пример ответа

```text
[
 {
 "id":"132456", // идентификатор домена

 "fqdn":"mylogin.bget.ru", // полное имя домена (кириллические
 // домены передаются в кириллице)

 "date_add":"2011-10-24 15:01:40", // дата и время добавления домена

 "auto_renew":"0", // статус опции "автоматическое
 // продление домена"

 "date_register":"2011-10-24", // дата регистрации домена
 // (если на обслуживании в BeGet)

 "date_expire":0, // дата окончания срока делегирования
 // (если на обслуживании в BeGet)

 "can_renew":"0", // статус возможности продления

 "registrar":null, // регистратор доменного имени
 // (если на обслуживании в BeGet)

 "registrar_status":null, // статус домена у регистратора
 // (если на обслуживании в BeGet).
 // Может быть: delegated, not_active,
 // undelegated

 "register_order_status":null, // статус заявки на регистрацию домена
 // (если домен был добавлен в рамках
 // заявки на его регистрацию).
 // Может быть: new, registred, delete

 "register_order_comment":null, // комментарий, к заявке на регистрацию
 // (чаще всего это комментарий
 // о причине аннулирования заявки)

 "renew_order_status":"0", // статус заявки на продление домена.
 // Может быть: pending, delete,
 // canceled, error, success

 "is_under_control":0 // статус показывает, находится ли
 // домен на обслуживании в BeGet.
 // Определяет возможность выполнения
 // таких действий, как:
 // продление домена,
 // заказ доп. услуг у регистратора,
 // смена серверов DNS
 }
]
```

## getZoneList

### Описание

Метод возвращает список зон.

### Пример вызова

```text
https://api.beget.com/api/domain/getZoneList?login=userlogin&passwd=password&output_format=json
```

### Пример ответа

```text
{
 "ru":{
 "id":"1", // идентификатор зоны
 "zone":"ru", // наименование зоны
 "price":"120", // стоимость регистрации домена в зоне
 "price_renew":"120", // стоимость продления домена в зоне
 "price_idn":null, // стоимость регистрации IDN-домена в зоне
 "price_idn_renew":null, // стоимость продления IDN-домена в зоне
 "is_idn":"false", // поддерживает ли зона IDN-домены
 "is_national":"true", // является ли зона национальной
 "min_period":"1", // минимальный срок регистрации домена (в годах)
 "max_period":"1" // максимальный срок регистрации домена (в годах)
 },
}
```

## addVirtual

### Описание

Метод добавляет домен.

### Дополнительные параметры

- **hostname** – доменное имя, без зоны (например, domain);

- **zone_id** – id зоны, тип int.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/domain/addVirtual?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"hostname":"domain","zone_id": 1}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/domain/addVirtual?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22hostname%22%3A%22domain%22%2C%22zone_id%22%3A+1%7D
```

### Пример ответа

```text
12510
```

Возвращается ID добавленного домена.

## delete

### Описание

Метод удаляет домен. Если домен был прилинкован к сайту, то он будет отлинкован от него. Также будут удалены все поддомены этого домена.

### Дополнительные параметры

- **id** – id домена.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/domain/delete?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"id":12510}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/domain/delete?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22id%22%3A12510%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.

## getSubdomainList

### Описание

Метод возвращает список поддоменов.

### Пример вызова

```text
https://api.beget.com/api/domain/getSubdomainList?login=userlogin&passwd=password&output_format=json
```

### Пример ответа

```text
[
 {
 "id":"132456", // id поддомена
 "fqdn":"subodmain.domain.ru", // полное имя поддомена
 "domain_id":"12345" // id родительского домена
 },
 {
 "id":"123457",
 "fqdn":"user.forum.domain.com",
 "domain_id":"12347"
 }
]
```

## addSubdomainVirtual

### Описание

Метод добавляет заданный поддомен.

### Дополнительные параметры

- **subdomain** – имя поддомена;

- **domain_id** – id родительского домена.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/domain/addSubdomainVirtual?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"subdomain": "subdomain","domain_id": 1000}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/domain/addSubdomainVirtual?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22subdomain%22%3A+%22subdomain%22%2C%22domain_id%22%3A+1000%7D
```

### Пример ответа

```text
12345
```

Возвращается ID добавленного поддомена.

## deleteSubdomain

### Описание

Метод удаляет заданный поддомен.

### Дополнительные параметры

- **id** – id поддомена.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/domain/deleteSubdomain?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"id": 1000}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/domain/deleteSubdomain?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22id%22%3A+1000%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.

## checkDomainToRegister

### Описание

Метод возвращает информацию о возможности регистрации заданного доменного имени.

### Дополнительные параметры

- **hostname** – доменное имя, без зоны;

- **zone_id** – id зоны. Получить список зон можно с помощью метода getZoneList;

- **period** – период регистрации (в годах), тип int.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/domain/checkDomainToRegister?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"hostname": "domain", "zone_id": 3, "period":1}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/domain/checkDomainToRegister?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22hostname%22%3A+%22domain%22%2C+%22zone_id%22%3A+3%2C+%22period%22%3A1%7D
```

### Пример ответа

```text
{
 "may_be_registered":true, // свободен ли домен для регистрации
 // (на основании сервиса WHOIS)

 "bonus_domains":0, // текущее количество бонусных доменов
 // на аккаунте в выбранной зоне

 "balance":289.46, // текущий баланс аккаунта

 "pay_type":false, // способ оплаты регистрации домена. Может быть:
 // null – оплатить домен невозможно;
 // money – оплата будет со счета аккаунта;
 // bonus_domain – оплата будет за счет бонуса.

 "price":350, // итоговая стоимость регистрации домена
 // (с учетом периода)

 "in_system":false // находится ли уже такой домен
 // на обслуживании BeGet
}
```

### Примечание

Для окончательного решения о возможности регистрации домена необходимо проанализировать три поля: _may_be_registered, pay_type и in_system_.

Их значения должны быть:

- may_be_registered – _true_

- pay_type – _money_ или _bonus_domain_

- in_system – _false_

## getPhpVersion

### Описание

Метод возвращает информацию о текущей версии php для домена, о доступных для установки версиях php, и включен ли php как cgi.

### Дополнительные параметры

- **full_fqdn** – полное имя домена, для которого необходимо получить информацию.

### Пример вызова

```text
http://api.beget.com/api/domain/getPhpVersion?login=usrlogin&passwd=usrpasswd&full_fqdn=foobar.com&output_format=json

https://api.beget.com/api/domain/getPhpVersion?login%3Dusrlogin%26passwd%3Dusrpasswd%26full_fqdn%3Dfoobar.com%26output_format%3Djson
```

### Пример ответа

```text
"status": "success",
"answer": {
 "status": "success",
 "result": {
 "full_fqdn": "foobar.com",
 "php_version": "5.6",
 "cgi": "disabled",
 "allowed_versions": [
 "4.4",
 "5.2",
 "5.3",
 "5.4",
 "5.5",
 "5.6"
 ]
 }
}
```

## changePhpVersion

### Описание

Метод изменяет версию php на переданную. Позволяет установить и снять режим cgi.

### Дополнительные параметры

- **full_fqdn** – полное имя домена, для которого необходимо изменить версию php;

- **php_version** – версия php, на которую будет произведено изменение;

- **is_cgi** – установить или снять режим cgi. По умолчанию имеет значение false.

### Пример вызова

```text
https://api.beget.com/api/domain/changePhpVersion?login=userlogin&passwd=password&output_format=json&input_format=json&input_data={"full_fqdn": "example.com", "php_version": "5.4"}

https://api.beget.com/api/domain/changePhpVersion?login=userlogin&passwd=password&full_fqdn=example.com&php_version=5.4&is_cgi=true&output_format=json
```

### Пример ответа

```text
"status": "success",
"answer": {
 "status": "success",
 "result": {
 "full_fqdn": "example.com", // домен, у которого были изменены версия php и режим cgi
 "result": "changes will take effect in some time", // изменения могут занять некоторое время
 "php_version": "5.4", // версия php после выполнения текущего запроса
 "cgi": "enabled" // включен ли режим cgi
 }
}
```

## getDirectives

### Описание

Метод возвращает пользовательские директивы для указанного домена.

### Дополнительные параметры

- **full_fqdn** – полное имя домена.

### Пример вызова

```text
https://api.beget.com/api/domain/getDirectives?login=userlogin&passwd=password&output_format=json&input_format=json&input_data={"full_fqdn": "example.com"}

https://api.beget.com/api/domain/getDirectives?login=userlogin&passwd=password&full_fqdn=example.com&output_format=json
```

### Пример ответа

```text
"status": "success",
"answer": {
 "status": "success",
 "result": [ // массив с директивами
 {
 "name": "php_admin_value", // имя директивы
 "value": "session.save_handler redis" // её значение
 }
 ]
}
```

## addDirectives

### Описание

Метод добавляет пользовательские директивы для указанного домена.

### Дополнительные параметры

- **full_fqdn** – полное имя домена;

- **directives_list** – массив директив в формате:

```text
[
 {
 name: "name of directive",
 value: "value of directive"
 }
]
```

### Пример вызова

```text
https://api.beget.com/api/domain/addDirectives?login=userlogin&passwd=password&output_format=json&full_fqdn=example.com&directives_list[0][name]=php_flag&directives_list[0][value]=log_errors on
```

### Пример ответа

```text
"status":"success",
"answer": {
 "status": "success",
 "result":true
}
```

## removeDirectives

### Описание

Метод удаляет пользовательские директивы для указанного домена.

### Дополнительные параметры

- **full_fqdn** – полное имя домена;

- **directives_list** – массив директив в формате:

```text
[
 {
 name: "name of directive",
 value: "value of directive"
 }
]
```

### Пример вызова

```text
https://api.beget.com/api/domain/removeDirectives?login=userlogin&passwd=password&output_format=json&full_fqdn=example.com&directives_list[0][name]=php_flag&directives_list[0][value]=log_errors on
```

### Пример ответа

```text
"status":"success",
"answer": {
 "status": "success",
 "result":true
}
```
