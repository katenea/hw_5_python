## Часть А


from datetime import date


# 1. Нормализация email адресов (Возвращает значение, в котором адрес приведен к нижнему регистру
# и очищен от пробелов по краям)
def normalize_addresses(value: str) -> str:
    return value.strip().lower()


#2. Сокращенная версия тела письма (Возвращает email с новым ключом email["short_body"] —
#первые 10 символов тела письма + "...".)
def add_short_body(email: dict) -> dict:
    email["short_body"] = email["body"][0:10] + "... "
    return email


#3. Очистка текста письма (Заменяет табы и переводы строк на пробелы)
def clean_body_text(body: str) -> str:
    return body.replace("\n", " ").replace("\t", " ")


#4.Формирование итогового текста письма (Формирует текст письма)
def build_sent_text(email: dict) -> str:
    send_text = (f"Кому: {email['recipient']}, от {email['sender']}\n"
    f"Тема: {email['subject']}, дата {email['date']}\n"
    f"{email['short_body']}")
    return send_text


#5. Проверка пустоты темы и тела
def check_empty_fields(subject: str, body:str) -> tuple[bool, bool]:
    is_subject_empty = subject == ''
    is_body_empty = body ==''
    return is_subject_empty, is_body_empty


#6. Маска email отправителя (Возвращает маску email: первые 2 символа логина + "***@" + домен)
def mask_sender_email(login: str, domain: str) -> str:
    mask_from = login[0:2] + "***@" + domain
    return mask_from


#7. Создать функцию которая проверит корректности email адресов. Адрес считается корректным, если:
#содержит символ @;
#оканчивается на один из доменов: .com, .ru, .net.
# Возвращает список корректных email
def get_correct_email(email_list: list[str]) -> list[str]:
    correct_domain = ('.com', '.ru','.net')
    correct_email = []
    for email in email_list:
        if '@' in email and email.endswith(correct_domain):
            correct_email.append(email)
    return correct_email

#8. Создание словаря письма (Создает словарь email с базовыми полями:
#'sender', 'recipient', 'subject', 'body')
def create_email(sender: str, recipient: str, subject: str, body: str) -> dict:
    return {
        "sender": sender,
        "recipient": recipient,
        "subject": subject,
        "body": body
    }


#9. Добавление даты отправки (Возвращает email с добавленным ключом email["date"] — текущая дата в формате YYYY-MM-DD.)
def add_send_date(email: dict) -> dict:
    email["date"] = date.today().isoformat()
    return email

#10. Получение логина и домена (Возвращает логин и домен отправителя.)
def extract_login_domain(address: str) -> tuple[str, str]:
    login = address.split("@")[0]
    domain = address.split("@")[1]
    return login, domain


##Часть B. Отправка письма


def sender_email(recipient_list: list[str], subject: str, message: str, *, sender="default@study.com") -> list[dict]:
    # Проверить, что список получателей не пустой
    if not recipient_list:
        return []
    # Проверить корректность email отправителя и получателей через get_correct_email()
    sender_list = get_correct_email([sender])
    if not sender_list:
        return []

    recipient_list = get_correct_email(recipient_list)
    if not recipient_list:
        return []

    # Проверить пустоту темы и тела письма через check_empty_fields(). Если одно из них пустое — вернуть пустой список.
    subject_empty, massage_empty = check_empty_fields(subject, message)
    if subject_empty or massage_empty:
        return []

    # Исключить отправку самому себе: пройти по каждому элементу recipient_list в цикле for,
    # если адрес совпадает с sender, удалить его из списка.
    new_recipient_list = []
    for email in recipient_list:
        if email != sender:
            new_recipient_list.append(email)


    # Нормализовать: subject и body → с помощью clean_body_text() recipient_list и sender → с помощью normalize_addresses()
    subject = clean_body_text(subject)
    message = clean_body_text(message)
    sender = normalize_addresses(sender)
    norm_recipients_list = []
    for email in new_recipient_list:
        norm_recipients_list.append(normalize_addresses(email))

    # Создать письмо для каждого получателя функцией create_email()
    result_list = []
    for email in norm_recipients_list:
        result = create_email(sender,email,subject,message)
        result = add_send_date(result)   #Добавить дату отправки с помощью add_send_date()
        #Замаскировать email отправителя с помощью extract_login_domain() и mask_sender_email().
        login, domain = extract_login_domain(sender)
        result["sender"] = mask_sender_email(login, domain)
        #Сохранить короткую версию в email["short_body"]
        result = add_short_body(result)
        #Сформировать итоговый текст письма функцией build_sent_text().
        result_text = build_sent_text(result)
        result_list.append(result_text)

    # Вернуть итоговый список писем
    return result_list


test_emails = [
    # Корректные адреса
    "user@gmail.com",
    "admin@company.ru",
    "test_123@service.net",
    "Example.User@domain.com",
    "default@study.com",
    " hello@corp.ru  ",
    "user@site.NET",
    "user@domain.coM",
    "user.name@domain.ru",
    "usergmail.com",
    "user@domain",
    "user@domain.org",
    "@mail.ru",
    "name@.com",
    "name@domain.comm",
    "idadekin@gmail.com",
    "",
    "   ",
]

print(test_emails)
result_mails = sender_email(test_emails, "Проверка темы", "Привет! Я Марсик, хочу кушать!", sender="idadekin@gmail.com")
for asd in result_mails:
    print(asd)