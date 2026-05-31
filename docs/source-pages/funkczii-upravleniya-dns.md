---
title: "Управление DNS по API"
source_url: https://beget.com/ru/kb/api/funkczii-upravleniya-dns
payload_url: https://assets-site.beget.com/ru/kb/api/funkczii-upravleniya-dns/_payload.json?1d2409a7-6569-40d6-898b-d89ff365e937
published_at: 2020-07-09T17:57:15+03:00
modified_at: 2025-09-02T12:00:34+03:00
section: dns
---

# Управление DNS по API

Source: [https://beget.com/ru/kb/api/funkczii-upravleniya-dns](https://beget.com/ru/kb/api/funkczii-upravleniya-dns)
## getData

Метод возвращает информацию с DNS-сервера о домене.

### Дополнительные параметры

- **fqdn** - полное имя домена (домены на национальных языках следует передавать в punycode).

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/dns/getData?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"fqdn":"beget.ru"}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/dns/getData?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22fqdn%22%3A%22beget.ru%22%7D+
```

### Пример ответа

```text
[
"is_under_control": 1, // домен на обслуживании BeGet (0 - нет / 1 - да)
"is_beget_dns": 1, // домен на DNS-серверах BeGet (0 - нет / 1 - да)
"is_subdomain": 0, // является ли домен поддоменом (0 - нет / 1 - да)
"fqdn": "beget.ru", // переданное доменное имя
"records": { // текущие используемые DNS-записи
	"DNS": [
		{
			"value": "ns1.beget.ru",
			"priority": 10
		},
		{
			"value": "ns2.beget.ru",
			"priority": 20
		}
	],
	"DNS_IP": [
		{
			"value": null,
			"priority": 10
		},
		{
			"value": null,
			"priority": 20
		}
	],
	"A": [
		{
			"value": "91.106.201.65",
			"priority": "0"
		}
	],
	"MX": [
		{
			"value": "mx1.beget.ru",
			"priority": "10"
		},
		{
			"value": "mx2.beget.ru",
			"priority": "20"
		}
	],
	"TXT": [
		{
			"value": "",
			"priority": 0
		}
	]
},
 // тип текущих используемых настроек:
 // 1 - используются A, MX, TXT-записи;
 // 2 - используются NS-записи (для поддоменов);
 // 3 - используются CNAME-записи (для поддоменов).
"set_type": 1
]
```

## changeRecords

Этот метод управления DNS по API производит изменение DNS-записей для заданного домена.

### Дополнительные параметры

- **fqdn** – полное имя домена (домены на национальных языках следует передавать в punycode);

- **records** – массив, содержащий DNS записи.

В параметр **records** необходимо передать одну из групп параметров (в примере используется передача параметров с помощью JSON):

### 1. A-**, MX**-**, TXT**-**записи**

```text
	{
	 "A":[
	 {
	 "priority":10,
	 "value":"127.0.0.1"
	 }
	 ],
	 "MX":[
	 {
	 "priority":10,
	 "value":"mx1.beget.ru"
	 },
	 {
	 "priority":20,
	 "value":"mx2.beget.ru"
	 }
	 ],
	 "TXT":[
	 {
	 "priority":10,
	 "value":"TXT record"
	 }
	 ]
	}
```

Можно передавать до 10 записей каждого типа. Обязательно нужно верно указывать приоритет записей.

### 2. NS-записи (для поддоменов)

```text
	{
	 "NS":[
	 {
	 "priority":10,
	 "value":"ns1.beget.ru"
	 },
	 {
	 "priority":20,
	 "value":"ns2.beget.ru"
	 }
	 ]
	}
```

Можно передавать до 10 записей. Обязательно нужно верно указывать приоритет записей.

### 3. CNAME-запись (для поддоменов)

```text
 {
	 "CNAME":[
	 {
	 "priority":10,
	 "value":"domain.ru"
	 }
	 ]
	}
```

Можно передать только одну CNAME-запись.

### 4. DNS-записи (для доменов, находящихся на обслуживании BeGet)

```text
 {
	 "DNS":[
	 {
	 "priority":10,
	 "value":"ns1.domain.ru"
	 },
	 {
	 "priority":20,
	 "value":"ns2.domain.ru"
	 }
	 ],
	 "DNS_IP":[
	 {
	 "priority":10,
	 "value":"127.0.0.1"
	 },
	 {
	 "priority":20,
	 "value":"192.168.1.2"
	 }
	 ]
	}
```

Можно передать до 4 записей. Если DNS-серверы не являются собственными (т. е. не находятся на одном из поддоменов основного домена), то секцию DNS_IP можно опустить.

### Пример вызова

```text
// input_data приведена в не закодированном виде для наглядности
https://api.beget.com/api/dns/changeRecords?login=userlogin&passwd=password&input_format=json&output_format=json&input_data={"fqdn":"beget.ru","records":{"A":[{"priority":10,"value":"127.0.0.1"}],"MX":[{"priority":10,"value":"mx1.beget.ru"},{"priority":20,"value":"mx2.beget.ru"}],"TXT":[{"priority":10,"value":"TXT record"}]}}

// корректный пример вызова, input_data закодирован с помощью urlencode
https://api.beget.com/api/dns/changeRecords?login=userlogin&passwd=password&input_format=json&output_format=json&input_data=%7B%22fqdn%22%3A%22beget.ru%22%2C%22records%22%3A%7B%22A%22%3A%5B%7B%22priority%22%3A10%2C%22value%22%3A%22127.0.0.1%22%7D%5D%2C%22MX%22%3A%5B%7B%22priority%22%3A10%2Cvalue%22%3A%22mx1.beget.ru%22%7D%2C%7B%22priority%22%3A20%2C%22value%22%3A%22mx2.beget.ru%22%7D%5D%2C%22TXT%22%3A%5B%7B%22priority%22%3A10%2C%22value%22%3A%22TXT+record%22%7D%5D%7D%7D
```

### Пример ответа

```text
true
```

Возвращается признак удачного или нет выполнения.
