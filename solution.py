import datetime


# Часть A. Функции

# Нормализация email адресов
def normalize_addresses(value: str) -> str:
    """
    Возвращает значение, в котором адрес приведен к нижнему регистру и очищен от пробелов по краям.
    """
    return value.strip().lower()


# Сокращенная версия тела письма
def add_short_body(email: dict) -> dict:
    """
    Возвращает email с новым ключом email["short_body"] —
    первые 10 символов тела письма + "...".
    """
    email["short_body"] = email["body"][0:10] + "..."
    return email


# Очистка текста письма
def clean_body_text(body: str) -> str:
    """
    Заменяет табы и переводы строк на пробелы.
    """
    return body.replace("\t", " ").replace("\n", " ")


# Формирование итогового текста письма
def build_sent_text(email: dict) -> str:
    """
    Формирует текст письма в формате:

    Кому: {to}, от {from}
    Тема: {subject}, дата {date}
    {clean_body}
    """
    return f"""Кому: {email["recipient"]}, от {email["sender"]}
    Тема: {email["subject"]}, дата {email["date"]} 
    {email["body"]}"""


# Проверка пустоты темы и тела
def check_empty_fields(subject: str, body: str) -> tuple[bool, bool]:
    """
    Возвращает кортеж (is_subject_empty, is_body_empty).
    True, если поле пустое.
    """
    is_subject_empty = not bool(subject.strip())
    is_body_empty = not bool(body.strip())
    return is_subject_empty, is_body_empty


# Маска email отправителя
def mask_sender_email(login: str, domain: str) -> str:
    """
    Возвращает маску email: первые 2 символа логина + "***@" + домен.
    """
    return login[:2] + "***@" + domain


# Создать функцию, которая проверит корректности email адресов. Адрес считается корректным, если:
# 1. содержит символ @;
# 2. оканчивается на один из доменов: .com, .ru, .net.

test_emails = [
    # Корректные адреса
    "default@study.com",
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
    "",
    "   ",
]


def get_correct_email(email_list: list[str]) -> list[str]:
    """
    Возвращает список корректных email.
    """
    correct_emails = []
    for email in email_list:
        if '@' in email and email.endswith(('.com', '.ru', '.net')):
            correct_emails.append(email)
    return correct_emails


# Создание словаря письма
def create_email(sender: str, recipient: str, subject: str, body: str) -> dict:
    """
    Создает словарь email с базовыми полями:
    'sender', 'recipient', 'subject', 'body'
    """
    return {"sender": sender, "recipient": recipient, "subject": subject, "body": body}


# Добавление даты отправки
def add_send_date(email: dict) -> dict:
    """
    Возвращает email с добавленным ключом email["date"] — текущая дата в формате YYYY-MM-DD.
    """
    email["date"] = datetime.datetime.now().strftime("%Y-%m-%d")
    return email


# Получение логина и домена
def extract_login_domain(address: str) -> tuple[str, str]:
    """
    Возвращает логин и домен отправителя.
    Пример: "user@mail.ru" -> ("user", "mail.ru")
    """
    login, domain = address.split("@")
    return login, domain


def sender_email(recipient_list: list[str], subject: str, message: str, *, sender="default@study.com") -> list[dict]:
    emails_list = []

    # Проверить, что recipient_list не пустой
    if not recipient_list:
        return emails_list

    # Проверить корректность email отправителя и получателей через get_correct_email()
    correct_recipients_emails = get_correct_email(recipient_list)
    if not get_correct_email([sender]) or not correct_recipients_emails:
        return emails_list

    # Проверить пустоту темы и тела письма через check_empty_fields(). Если одно из них пустое — вернуть пустой список
    is_empty_subject, is_empty_body = check_empty_fields(subject, message)
    if is_empty_subject or is_empty_body:
        return emails_list

    # Исключить отправку самому себе: пройти по каждому элементу recipient_list в цикле for, если адрес совпадает с sender, удалить его из списка
    cleaned_recipients_list = [recipient for recipient in correct_recipients_emails if recipient != sender]

    # Нормализовать: subject и body → с помощью clean_body_text() recipient_list и sender → с помощью normalize_addresses()
    cleaned_subject_text = clean_body_text(subject)
    cleaned_message_text = clean_body_text(message)
    normalized_recipients = []
    for recipient in cleaned_recipients_list:
        normalized_recipients.append(normalize_addresses(recipient))
    normalized_sender = normalize_addresses(sender)

    # Создать письмо для каждого получателя функцией create_email()
    for recipient in normalized_recipients:
        email = create_email(normalized_sender, recipient, cleaned_subject_text, cleaned_message_text)
        # Добавить дату отправки с помощью add_send_date()
        add_send_date(email)
        # Замаскировать email отправителя с помощью extract_login_domain() и mask_sender_email()
        login, domain = extract_login_domain(normalized_sender)
        email["masked_sender"] = mask_sender_email(login, domain)
        # Сохранить короткую версию в email["short_body"]
        add_short_body(email)
        # Сформировать итоговый текст письма функцией build_sent_text()
        email["sent_text"] = build_sent_text(email)
        emails_list.append(email)

    return emails_list
