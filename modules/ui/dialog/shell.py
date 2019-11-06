# -*- coding: utf-8 -*-

from . import windows
import os
import testsuite
import terminal

ui = windows.UI()


def stub():
    ui.draw_msgbox(u'Это меню еще не готово')
    return


def load():
    code, value = testsuite.get_saves()
    if code:
        menu_items = [(save, u'') for save in value]
        if menu_items:
            header = u'Меню загрузки'
            hint = u'Выберите сохраненный тестовый набор:'
            code, tags = ui.draw_menu(header, hint, menu_items)
            if code == ui.OK:
                code, message = testsuite.load(tags)
                if code:
                    ui.draw_msgbox(u'Тестовый набор загружен')
                else:
                    ui.draw_msgbox(message)
        else:
            ui.draw_msgbox(u'Нет сохраненных тестовых наборов')
    else:
        strerror = value
        ui.draw_msgbox(strerror)
    return


def edit_number(job_id):
    h, w = ui.maxsize
    current_number = testsuite.job.get_number(job_id)
    header = u'Введите номер задачи'
    hint = header
    items = [(u'', u'Номер:', current_number)]
    code, tags = ui.draw_form(header, hint, items, (0, w))
    if code == ui.OK:
        testsuite.job.set_number(job_id, tags[0][2])
    return


def edit_name(job_id):
    h, w = ui.maxsize
    current_name = testsuite.job.get_name(job_id)
    header = u'Введите название задачи'
    hint = header
    items = [(u'', u'Название:', current_name)]
    code, tags = ui.draw_form(header, hint, items, (0, w))
    if code == ui.OK:
        testsuite.job.set_name(job_id, tags[0][2])
    return


def edit_strings(job_id):
    h, w = ui.maxsize
    items = testsuite.job.get_strings(job_id)
    header = u'Список строковых переменных'
    hint = header
    if items:
        code, tags = ui.draw_form(header, hint, items, (0, w))
        if code == ui.OK:
            for name, description, value in tags:
                testsuite.job.set_string(job_id, name, value)
    else:
        ui.draw_msgbox(u'В этой задаче нет строковых переменных')
    return


def edit_array(job_id, (id, descr, value)):
    header = u'Задача "' + testsuite.job.get_name(job_id) + u'", массив "' + descr + u'"'
    code, array = ui.draw_array_editor(header, value, (0, 0))
    if code == ui.OK:
        testsuite.job.set_array(job_id, id, array)
    return


def edit_file(job_id, file):
    header = u'Задача "' + testsuite.job.get_name(job_id) + u'", файл "' + file + u'"'
    hint = u' '
    items = ''
    code, array = ui.draw_form(header, hint, items)
    if code == ui.OK:
        testsuite.job.set_file(job_id, file)
    return


def choose_array(job_id):
    h, w = ui.maxsize
    arrays = testsuite.job.get_arrays(job_id)
    if arrays:
        header = u'Список массивов'
        hint = header
        items = [(descr, id) for (id, descr, value) in arrays]
        code, tags = ui.draw_menu(header, hint, items)
        if code == ui.OK:
            for id, descr, value in arrays:
                if descr == tags:
                    chosen_array = id
            header = u'Задача "' + testsuite.job.get_name(job_id) + u'", массив "' + chosen_array + u'"'
            edit_array(job_id, (id, descr, value))
    else:
        ui.draw_msgbox(u'В этой задаче нет массивов')
    return


def jobs_browser(root):
    choice = None
    code, jobs, message = testsuite.get_jobs(testsuite.config.JOBS_ROOT)
    if not code:
        ui.draw_msgbox(message)
        return
    if jobs:
        items = []
        for i in jobs:
            items.append((testsuite.job.get_number(i), testsuite.job.get_name(i)))
        header = u'Текущий тестовый набор'
        hint = u'Левая колонка - приоритет задачи,\nправая колонка - название задачи'
        code, tags = ui.draw_menu(header, hint, items)
        if code == ui.OK:
            for i in jobs:
                if testsuite.job.get_number(i) == tags:
                    choice = i
    else:
        ui.draw_msgbox(u'Список задач пуст')
    return choice


def job_editor(job_id):
    items = [(u'Номер', u''),
             (u'Название', u''),
             (u'Переменные', u''),
             (u'Массивы', u'')]
    header = u'Редактирование задачи "' + testsuite.job.get_name(job_id) + u'"'
    hint = u'Выберите пункт для редактирования'
    code, tags = ui.draw_menu(header, hint, items)
    if code == ui.OK:
        if tags == u'Номер':
            edit_number(job_id)
        elif tags == u'Название':
            edit_name(job_id)
        elif tags == u'Переменные':
            edit_strings(job_id)
        elif tags == u'Массивы':
            choose_array(job_id)
    return


def add_job(path, name):
    items = [(u'', u'номер:', u'10'),
             (u'', u'название:', name)]
    header = u'Введите название для новой задачи:'
    hint = header
    code, tags = ui.draw_form(header, hint, items)
    if code == ui.OK:
        job_number = int(tags[0][2])
        job_name = tags[1][2]
        code, message = testsuite.make_job(os.path.join(path, name), job_number, job_name)
        if code:
            ui.draw_msgbox(u'Задача успешно добавлена')
        else:
            ui.draw_msgbox(message)
    return


def tests_browser(root):
    header = u'Выбор теста'
    stack = [root]
    chosen = False
    while stack:
        path = os.path.join(*stack)
        name = u''
        hint = os.path.relpath(path, root)
        items = testsuite.get_templates(path)
        if items:
            code, tag = ui.draw_menu(header, hint, items)
            if code == ui.OK:
                for name, type in items:
                    if name == tag:
                        if type == testsuite.template.TESTSUITE_DIRECTORY:
                            stack.append(tag)
                        elif type == testsuite.template.TESTSUITE_TEMPLATE:
                            add_job(path, name)
                            break
            else:
                path = stack.pop()
        else:
            ui.draw_msgbox(u'В каталоге пусто')
            stack.pop()
        if chosen:
            break
    return chosen, path, name


def edit():
    while True:
        items = [(u'Добавить задачу', u'добавить в набор'),
                 (u'Удалить задачу', u'удалить из набора'),
                 (u'Изменить параметры задачи', u'список задач')]
        header = u'Меню редактирования тестовых наборов'
        hint = u' '
        code, tags = ui.draw_menu(header, hint, items)
        if code == ui.OK:
            if tags == u'Добавить задачу':
                tests_browser(testsuite.config.TEMPLATES_ROOT)
            elif tags == u'Удалить задачу':
                chosen_job = jobs_browser(testsuite.config.JOBS_ROOT)
                if chosen_job:
                    code, message = testsuite.job.delete(chosen_job)
                    if code:
                        ui.draw_msgbox(u'Задача успешно удалена')
                    else:
                        ui.draw_msgbox(message)
            elif tags == u'Изменить параметры задачи':
                chosen_job = jobs_browser(testsuite.config.JOBS_ROOT)
                if chosen_job:
                    job_editor(chosen_job)
        else:
            break
    return


def save():
    items = [(u'', u'название', u'')]
    header = u'Введите название для тестового набора:'
    hint = header
    h, w = ui.maxsize
    code, tags = ui.draw_form(header, hint, items, (0, w))
    if code == ui.OK:
        code, message = testsuite.save(tags[0][2])
        if code:
            ui.draw_msgbox(u'Сохранено успешно')
        else:
            ui.draw_msgbox(message)
    return


def log_to(msg, fd=None, func=None):
    if fd:
        fd.write(msg.encode('utf-8'))
        fd.flush()
    if func:
        func()


def run():
    code, jobs, message = testsuite.get_jobs()
    if not code:
        ui.draw_msgbox(message)
        return

    header = u'Выполнение тестового набора'
    height, width = ui.maxwindowsize
    elements = []
    total_number = len(jobs)
    for number, id in enumerate(jobs):

        stdout = open(os.path.join(id, u'stdout.log'), 'w')
        stderr = open(os.path.join(id, u'stderr.log'), 'w')

        pct = int(float(number) / total_number * 100)
        name = testsuite.job.get_name(id)
        elements.append((name, '7'))
        ui.draw_mixedgauge(header, elements, pct, height, width)

        runnable = testsuite.job.Runnable()
        runnable.on_stdout = lambda msg: log_to(msg, stdout)
        runnable.on_stderr = lambda msg: log_to(msg, stderr)

        code, retval, message = runnable.run(id)

        if not code:
            ui.draw_msgbox(u'Не удалось запустить задачу')
            break

        elements[number] = (name, retval)

    ui.draw_mixedgauge(header, elements, 100, height, width)
    terminal.getch()
    return


def clean():
    return testsuite.clean()


def exit():

    return


def main():
    while True:
        menu_items = [(u'Загрузить', u'восстановление из архива'),
                      (u'Редактировать', u'настройка тестового набора'),
                      (u'Сохранить', u'сохранение текущего состояния'),
                      (u'Запустить', u'выполнить тестовый набор'),
                      (u'Очистить', u'удалить тестовый набор'),
                      (u'Выйти', u'выход из оболочки')]
        code, tags = ui.draw_menu(u'Главное меню', u'Выберите пункт меню:', menu_items)
        if code == ui.OK:
            if tags == u'Загрузить':
                load()
            elif tags == u'Редактировать':
                edit()
            elif tags == u'Сохранить':
                save()
            elif tags == u'Запустить':
                run()
            elif tags == u'Очистить':
                clean()
            elif tags == u'Выйти':
                exit()
        else:
            break
