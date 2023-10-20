

# модуль генерации случайных чисел
import random

# модуль работы с временем
import datetime


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
def get_password_types(password_length):
    """
        Возможные типы символов (регистр не важен):
            - LOWER_CASE - прописные буквы,
            - UPPER_CASE - заглавные буквы
            - NUMS       - добавлять цифры в пароль
            - SPEC       - добавлять спец символы в пароль
        ----
            - START      - начать генерацию пароля по выбранным типам символов
    """
    # состояние выбранных типов (True - выбран, False - не выбран)
    types = {"LOWER_CASE": False, "UPPER_CASE": False,
             "NUMS": False, "SPEC": False}

    flags_str = get_password_types.__doc__
    # вывод пояснения по возможным флагам
    print(flags_str)

    while True:
        # принимаем типы символов и говорим по счету нужно ввести
        cur_type = input("Введите название типа: ")
        cur_type = cur_type.upper()

        # флаг для начала генерации пароля
        # начинает генерацию, если выбрали хотя бы один тип символа
        types_num = get_types_num(types)
        if cur_type == "START":
            status = is_type_num_correct(types_num, password_length)

            # если пароль изменился
            password_length = status["password_length"]
            # если с типами нет проблем, начинает генерацию пароля
            if status["gen_start"]:
                break
            else:
                print("Уберите не нужные типы символов")
                continue


        # проверяем, есть ли такой тип символа
        if cur_type in types:
            # меняем выбранный тип символа
            # на True, если был False
            # на False, если был True
            types[cur_type] = not types[cur_type]

        else:
            print("Такого типа символа нет." + flags_str)

        # промежуточный вывод состояний типов, чтобы видеть из чего будет генерироваться пароль
        print(f'Пока что выбраны типы: ' + str(types))

    print(f'Выбранные типы: ' + str(types))
    return types


def generate_password(password_length, types):
    """ генерирует пароль по заданным условиям(видам типов символов) """
    password = ""
    spec_list = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "—", "_", "+",
                 "=", ";", ":", ",", ".", "?", "|", "`", "~", "[", "]", "{", "}"]
    nums_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    types_used = get_only_true_types(types)

    while len(password) < password_length:
        # если сгенерировался код символа, который не используется в пароле
        # алгоритм сам перейдет к следующему шагу, ничего не изменив

        # случайная величина, определяет какой символ сейчас генерируется
        rand_sym_code = random.getrandbits(2)

        if types["NUMS"] and rand_sym_code == 0:
            # генерируем случайное число от 0 до 9
            num_sample = random.sample(nums_list, k=3)
            random.shuffle(num_sample)
            password += str(num_sample[0])
            types_used["NUMS"] = True

        if types["SPEC"] and rand_sym_code == 1:
            # выбираем случайные элементы из списка специальных символов
            password += random.choice(spec_list)
            types_used["SPEC"] = True

        # если используем буквы
        if types["UPPER_CASE"] and rand_sym_code == 2:
            # генерируем заглавные буквы
            password += chr(random.randint(65, 90))
            types_used["UPPER_CASE"] = True

        if types["LOWER_CASE"] and rand_sym_code == 3:
            # генерируем заглавные буквы
            password += chr(random.randrange(101, 123))
            types_used["LOWER_CASE"] = True

        # если пароль сгенерирован
        if password_length <= len(password):
            # но сгенерирован неправильно, сгенерируем заново
            # будет проще, чем каждый раз убирать символы из пароля, пока не получим подходящий
            if not check_password(types_used):
                password = ""
                for type in types_used:
                    types_used[type] = False
                continue

    return password


def check_password(types_used):
    """ проверяет, все ли выбранные типы учтены в пароле """
    for type in types_used.items():
        if not type:
            return False
    return True


def get_only_true_types(types):
    """ словарь, в котором будем отмечать какой из типов символов уже есть в пароле """
    true_types = {}
    for type in types:
        if types[type] and type != "NO_LETTERS":
            true_types[type] = False
    return true_types


def get_types_num(types):
    """ возвращает количество выбранных типов, используется для генерации самого пароля """
    types_num = 0
    for type in types:
        if types[type]:
            types_num += 1

    return types_num


def is_type_num_correct(types_length, password_length):
    """ проверяет соответсвие количества выбранных типов символов и длины пароля """
    status = {"password_length": password_length, "gen_start": False}

    # если число выбранных типов превосходит длину пароля, то нельзя его сгенерировать правильно
    if types_length > password_length:
        change_pass_length = input("Количество выбранных типов символов превышает длину пароля, "
                                   "хотите изменить длину пароля? y(да)/n(нет)")
        if change_pass_length == 'y':
            new_length = get_password_length()
            status["password_length"] = new_length
    # если не выбрано ни одного типа символа для генерации пароля
    elif types_length == 0:
        print("Для генерации пароля необходимо выбрать хотя бы один тип символа")
    else:
        status["gen_start"] = True

    return status


def print_advice():
    advice = "Советуется менять пароли каждый месяц. Вам следует сменить пароль "

    next_month = datetime.datetime.today() + datetime.timedelta(days=30)
    print(advice + str(next_month.year) + ":" + str(next_month.month) + ":" + str(next_month.day))


def make_new_password():
    """
        Программа умеет генерировать пароли заданной длины с заданными условиями на использование символов

        - Сначала вводится длина пароля. Она должна быть больше нуля.

        - Выбираются типы символов, из которых будет состоять пароль. Их выбор происходит путем ввода флага,
        означающего конкретную группу символов. Возможные типы символов:

            - LOWER_CASE - прописные буквы,
            - UPPER_CASE - заглавные буквы
            - NUMS       - добавлять цифры в пароль
            - SPEC       - добавлять спец символы в пароль

        - Тип символа может быть написан в любом регистре, даже смешанном, главное сохранить порядок символов, например:
            - LOWER_CASE можно написать следующими способами: lower_case, LoWeR_CaSe, LOWER_case
            - Однако если написать Case_lower, программа не поймет этот флаг и попросит ввести другой.

        - Если количество типов символов превысило длину пароля, пользователю предлагается изменить длину пароля

        -- При выборе одного типа два раза, он не будет использоваться (так можно убирать флаги при ошибке)

        - Для начала генерации пароля необходимо ввести флаг START (также в любом регистре)

        - Далее происходит генерация пароля по выбранным символам. Генерация происходит быстро, но если:
            - пароль имеет большую длину
            - пароль имеет малую длину, но количество выбранных типов символов отличается на несколько единиц
            или вообще совпадает (засчет перегенерации пароля сначала)


        -------
        Обрабатываемые ошибки:
            - неверная длина пароля
            - неверный флаг типа символа
            - количество выбранных типов символов больше длины пароля
            - нулевое количество выбранных типов символов

    """
    print(make_new_password.__doc__)
    password_length = get_password_length()
    types = get_password_types(password_length)
    password = generate_password(password_length, types)
    print("Ваш новые пароль: " + password)
    print_advice()


# MAIN
make_new_password()
