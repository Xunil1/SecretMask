import re


class EmailMasker:
    def __init__(self, email, mask_char="x"):
        self.email = email
        self.mask_char = mask_char

    def mask(self):
        name, domain = self.email.split("@")
        masked_name = self.mask_char * len(name)
        return f"{masked_name}@{domain}"


class PhoneMasker:
    def __init__(self, phone_number, mask_char="x", mask_length=3):
        self.phone_number = phone_number
        self.mask_char = mask_char
        self.mask_length = mask_length

    def mask(self):
        # Убираем лишние пробелы
        normalized_phone = re.sub(r'\s+', ' ', self.phone_number)

        # Находим символы для маскирования
        digits = re.findall(r'\d', normalized_phone)
        if self.mask_length > len(digits):
            masked_digits = len(digits)
        else:
            masked_digits = self.mask_length

        visible_digits = digits[:-masked_digits]

        masked_phone = ""
        digit_index = 0
        for char in normalized_phone:
            if char.isdigit():
                if digit_index < len(visible_digits):
                    masked_phone += visible_digits[digit_index]
                else:
                    masked_phone += self.mask_char
                digit_index += 1
            else:
                masked_phone += char

        return masked_phone


class SkypeMasker:
    def __init__(self, skype, mask_char="x"):
        self.skype = skype
        self.mask_char = mask_char

    def mask(self):
        if self.skype.startswith("skype:"):
            return f"skype:{self.mask_char * 3}"
        else:
            # Замена идентификатора пользователя в ссылке
            return re.sub(r"(skype:)([^\"?]*)", f"\\1{self.mask_char * 3}", self.skype)


# Пример с Email
email = "example@domain.com"
email_masker = EmailMasker(email)
print(email_masker.mask())  # Вывод: xxxxxx@domain.com

# Пример с номером телефона
phone = "+7 666 777       888"
phone_masker = PhoneMasker(phone, mask_length=5)
print(phone_masker.mask())  # Вывод: +7 666 7xx xxx

# Пример со Skype
skype = "skype:alex.max"
skype_masker = SkypeMasker(skype)
print(skype_masker.mask())  # Вывод: skype:xxx

skype_link = '<a href="skype:alex.max?call">skype</a>'
skype_masker_link = SkypeMasker(skype_link)
print(skype_masker_link.mask())  # Вывод: <a href="skype:xxx?call">skype</a>
