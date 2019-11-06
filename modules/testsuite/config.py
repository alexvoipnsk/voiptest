# -*- coding: utf-8 -*-

TEMPLATES_ROOT = u'tests/scripts'
JOBS_ROOT = u'jobs'
SAVES_PATH = u'saves'
OPTIONS_FILE = u'options.json'


import os
import json
import codecs
import tarfile
from error import TestsuiteError

def ls(root, sorted=False):
    list_ = []
    try:
        for dir in os.listdir(root):
            list_.append(os.path.join(root, dir))
        if sorted:
            list_.sort()
    except OSError as e:
        raise TestsuiteError(u'Не могу получить список файлов в директории ' + root + u': ' + e.strerror)
    return list_


def rm_rf(root, mindepth = 0, depth = 0):
    """Удаляет файл root, а если это каталог - то и его содержимое, оставляя
    нетронутыми объекты, вложенные в root не глубже, чем на уровень mindepth.
    Если mindepth равен 0, то root удаляется полностью

    :param dir:
    :param mindepth:
    :param depth:
    """
    try:
        for path in (os.path.join(root, file) for file in os.listdir(root)):
            if os.path.isdir(path):
                rm_rf(path, mindepth, depth + 1)
            else:
                if depth >= mindepth:
                    os.unlink(path)
        if depth >= mindepth:
            os.rmdir(root)
    except OSError as e:
        raise TestsuiteError(u'Не могу удалить файл ' + root + u': ' + e.strerror)


def mkdir(path):
    try:
        os.mkdir(path)
    except OSError as e:
        raise TestsuiteError(u'Не могу создать каталог ' + path + u': ' + e.strerror)


def read_json(path):
    try:
        with open(path, 'r') as file:
            return json.loads(file.read().decode('utf-8'), encoding='utf-8')
    except IOError as e:
        raise TestsuiteError(u'не могу прочитать файл ' + path + u': ' + e.strerror)
    except ValueError as e:
        raise TestsuiteError(u'ошибка синтаксиса JSON в файле ' + path + u': ' + e.message)


def write_json(path, data):
    try:
        with codecs.open(path, 'w', encoding='utf-8') as file:
            return json.dump(data, file, encoding='utf-8', ensure_ascii=False)
    except ValueError as e:
        raise TestsuiteError(u'ошибка синтаксиса JSON: ' + e.message)
    except (IOError, OSError) as e:
        raise TestsuiteError(u'error writing file ' + path)


def get_data(path):
    return read_json(path)


def set_data(path, data):
    return write_json(path, data)


def get_saves(path=SAVES_PATH):
    try:
        saves = (os.path.splitext(os.path.splitext(os.path.basename(i))[0])[0] for i in ls(path, sorted=True))
    except TestsuiteError as e:
        raise TestsuiteError(u'Не могу получить список сохранений: ' + e.message)
    return saves


def save(name):
    try:
        path = os.path.join(SAVES_PATH, name + u'.tar.gz').encode('utf-8')
        with tarfile.open(path, 'w:gz') as file:
            file.add(JOBS_ROOT)
        file.close()
    except (IOError, OSError) as e:
        raise TestsuiteError(u'Не могу сохранить тестовый набор ' + name + u': ' + e.strerror.decode('utf-8'))
    pass


def load(name):
    try:
        path = os.path.join(SAVES_PATH, name + u'.tar.gz').encode('utf-8')
        file = tarfile.open(path, 'r:gz')
        file.extractall()
        file.close()
    except (IOError, OSError) as e:
        raise TestsuiteError(u'Не могу загрузить тестовый набор ' + name + u': ' + e.strerror.decode('utf-8'))
    pass
