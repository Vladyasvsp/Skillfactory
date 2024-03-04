import random
HELP = """
help - напечатать справку по программе
add - добавить задачу в список (название задачи запрашиваем у пользователя)
show - напечатать все добавленные задачи
random - добавлять случайную задачу на дату Сегодня"""


random_tasks = ["Записаться на курс в Нетологию", "Написать Гвидо письмо", "Покормить кошку", "Помыть машину"]

tasks = {

}

run = True

def add_todo(date, task):
    if date in tasks:
        # Дата есть в словаре
        # Добавляем в список задачу
        tasks[date].append(task)
    else:
        # Даты в словаре нет
        # Создаем запись с ключом date
        tasks[date] = []
        tasks[date].append(task)
    print('Задача', task, ' добавлена на дату', date)

while run:
    comand = input('Введите команду: ')
    if comand == "help":
        print(HELP)
    elif comand == "show":
        date = input('Введите дату для отображения списка задач: ')
        if date in tasks:
            for task in tasks[date]:
                print('- ', task)
        else:
            print('Такой даты нет')
    elif comand == "add":
        date = input('Введите дату выполнения задачи: ')
        task = input('Введите название задачи: ')
        add_todo(date, task)
    elif comand == "random":
        task = random.choice(random_tasks)
        add_todo("Сегодня", task)
    elif comand == "exit":
        print('Спасибо за использование! До свидания')
        break
    else:
        print('Неизвестная задача')
