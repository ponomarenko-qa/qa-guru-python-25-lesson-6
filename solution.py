import datetime


def normalize_addresses(value: str) -> str:
    """
    Возвращает значение, в котором адрес приведен к нижнему регистру и очищен от пробелов по краям.
    """
    return value.strip().lower()


def add_short_body(email: dict) -> dict:
    """
    Возвращает email с новым ключом email["short_body"] —
    первые 10 символов тела письма + "...".
    """
    email["short_body"] = email["body"][0:10] + "..."
    return email


def clean_body_text(body: str) -> str:
    """
    Заменяет табы и переводы строк на пробелы.
    """
    return body.replace("\t", " ").replace("\n", " ")


def build_sent_text(email: dict) -> str:
    """
    Формирует текст письма в формате:

    Кому: {to}, от {from}
    Тема: {subject}, дата {date}
    {clean_body}
    """
    return f"""Кому: {email["recipient"]}, от {email["masked_sender"]}
    Тема: {email["subject"]}, дата {email["date"]} 
    {email["short_body"]}"""


def check_empty_fields(subject: str, body: str) -> tuple[bool, bool]:
    """
    Возвращает кортеж (is_subject_empty, is_body_empty).
    True, если поле пустое.
    """
    is_subject_empty = not bool(subject.strip())
    is_body_empty = not bool(body.strip())
    return is_subject_empty, is_body_empty


def mask_sender_email(login: str, domain: str) -> str:
    """
    Возвращает маску email: первые 2 символа логина + "***@" + домен.
    """
    return login[:2] + "***@" + domain


test_emails = [
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
        if '@' in email and email.strip().lower().endswith(('.com', '.ru', '.net')):
            correct_emails.append(email)
    return correct_emails


def create_email(sender: str, recipient: str, subject: str, body: str) -> dict:
    """
    Создает словарь email с базовыми полями:
    'sender', 'recipient', 'subject', 'body'
    """
    return {"sender": sender, "recipient": recipient, "subject": subject, "body": body}


def add_send_date(email: dict) -> dict:
    """
    Возвращает email с добавленным ключом email["date"] — текущая дата в формате YYYY-MM-DD.
    """
    email["date"] = datetime.datetime.now().strftime("%Y-%m-%d")
    return email


def extract_login_domain(address: str) -> tuple[str, str]:
    """
    Возвращает логин и домен отправителя.
    Пример: "user@mail.ru" -> ("user", "mail.ru")
    """
    login, domain = address.split("@")
    return login, domain


def sender_email(recipient_list: list[str], subject: str, message: str, *, sender="default@study.com") -> list[dict]:
    emails_list = []

    if not recipient_list:
        return emails_list

    correct_recipients_emails = get_correct_email(recipient_list)
    if not get_correct_email([sender]) or not correct_recipients_emails:
        return emails_list

    is_empty_subject, is_empty_body = check_empty_fields(subject, message)
    if is_empty_subject or is_empty_body:
        return emails_list

    cleaned_recipients_list = [recipient for recipient in correct_recipients_emails if recipient != sender]

    cleaned_subject_text = clean_body_text(subject)
    cleaned_message_text = clean_body_text(message)
    normalized_recipients = []
    for recipient in cleaned_recipients_list:
        normalized_recipients.append(normalize_addresses(recipient))
    normalized_sender = normalize_addresses(sender)

    for recipient in normalized_recipients:
        email = create_email(normalized_sender, recipient, cleaned_subject_text, cleaned_message_text)
        add_send_date(email)
        login, domain = extract_login_domain(normalized_sender)
        email["masked_sender"] = mask_sender_email(login, domain)
        add_short_body(email)
        email["sent_text"] = build_sent_text(email)
        emails_list.append(email)

    return emails_list
