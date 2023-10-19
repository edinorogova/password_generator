# модуль генерации случайных чисел
import random


def get_password_length():
    """ обработчик длины пароля """

    # получение длины пароля, где password_length - длина пароля
    while True:
        password_length = int(input("Введите длину пароля: "))
        # если длина пароля не натуральное число, даем возможность ввести еще раз
        if password_length <= 0:
            print("Длина пароля должна быть представлена натуральным числом")
        # если длина пароля натуральное число, идем дальше по алгоритму
        else:
            break
    print(f'Длина пароля: {password_length}')
    return password_length


# принимает от пользователя флаги определяющие виды символов, котрый должны содержаться в пароле
# :return словарь, где ключи - названия флагов, значения - True/False (используется или нет)
def get_password_types():
    """
        Возможные типы символов (регистр не важен):
            - LOWER_CASE - прописные буквы,
            - UPPER_CASE - заглавные буквы
            - NO_LETTERS - не использовать буквы в пароле,
            - NUMS       - добавлять цифры в пароль
            - SPEC       - добавлять спец символы в пароль
        ----
            - START      - начать генерацию пароля по выбранным типам символов
    """
    # состояние выбранных типов (True - выбран, False - не выбран)
    types = {"LOWER_CASE": False, "UPPER_CASE": False, "NO_LETTERS": False,
             "NUMS": False, "SPEC": False}

    flags_str = get_password_types.__doc__
    print(flags_str)

    while True:
        # принимаем типы символов и говорим по счету нужно ввести
        cur_type = input("Введите название типа: ")
        cur_type = cur_type.upper()

        # флаг для начала генерации пароля
        if cur_type == "START":
            break

        # проверяем, есть ли такой тип символа
        if cur_type in types:
            # меняем выбранный тип символа
            # на True, если был False
            # на Falsw, если был True
            types[cur_type] = not types[cur_type]

            if cur_type == "LOWER_CASE":
                types["NO_LETTERS"] = False
            elif cur_type == "UPPER_CASE":
                types["NO_LETTERS"] = False
            # если буквы не используются, то они не заглавные и не прописные
            elif cur_type == "NO_LETTERS":
                types["LOWER_CASE"] = False
                types["UPPER_CASE"] = False
        else:
            print("Такого типа символа нет." + flags_str)

        # промежуточный вывод состояний типов, чтобы видеть из чего будет генерироваться пароль
        print(f'Пока что выбраны типы: ' + str(types))

    print(f'Выбранные типы: ' + str(types))
    return types

def generate_password(password_length, types):
    password = []
    spec_list = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "—", "_", "+",
                 "=", ";", ":", ",", ".", "?", "|", "`", "~", "[", "]", "{", "}"]

    cur_password_len = 0
    while cur_password_len < password_length:
        if types["NUMS"]:
            # генерируем случайное число от 0 до 9
            password.append(random.randrange(10))
        if types["SPEC"]:
            # выбираем случайные элементы из списка специальных символов
            password.append(random.choice(spec_list))
        if not types["NO_LETTERS"]:
            # если используем буквы
            if types["UPPER_CASE"]:
                # генерируем заглавные буквы
                password.append(random.randint(65, 90))
            if types["LOWER_CASE"]:
                # генерируем заглавные буквы
                password.append(int(random.random(101, 122)))


    # random.shuffle(x)

    return password

# MAIN
password_length = get_password_length()
types = get_password_types()

