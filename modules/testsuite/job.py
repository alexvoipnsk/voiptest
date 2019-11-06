# -*- coding: utf-8 -*-

import os
import subprocess
import codecs
from time import sleep
import config
from error import TestsuiteError
import terminal


def check(id_):
    return


def get_name(id_):
    number, name = id_.split('-', 1)
    return name


def set_name(id_, name):
    basename, filename = os.path.split(id_)
    number = get_number(id_)
    new_path = os.path.join(basename, number + u'-' + name)
    try:
        os.rename(id_, new_path)
    except OSError as e:
        raise TestsuiteError(u'Не могу переименовать файл: ' + e.strerror)
    return new_path


def get_number(id_):
    basename, filename = os.path.split(id_)
    number, name = filename.split('-', 1)
    return number


def set_number(id_, number):
    basename, filename = os.path.split(id_)
    name = get_name(id_)
    new_path = os.path.join(basename, number + u'-' + name)
    try:
        os.rename(id_, new_path)
    except OSError as e:
        raise TestsuiteError(u'Не могу переименовать файл: ' + e.strerror)
    return new_path


def get_data(id_, k=None):
    data = None
    try:
        data = config.get_data(os.path.join(id_, config.OPTIONS_FILE))
        if k != None:
            data = data.get(k)
    except TestsuiteError as e:
        message = u'Не удалось прочитать данные'
    return data


def set_data(id_, data):
    config.set_data(os.path.join(id_, config.OPTIONS_FILE), data)


def get_arrays(id_):
    arrays = []
    for variable in get_data(id_).get('options'):
        if variable.get('type') == u'array':
            if isinstance(variable.get('value'), list):
                var_id = variable.get('id')
                var_desc = variable.get('description') or variable.get('id')
                var_value = variable.get('value')
                arrays.append((var_id, var_desc, var_value))
    return arrays


def set_array(id_, name, value):
    code = False
    data = get_data(id_)
    for index, variable in enumerate(data.get('options')):
        if variable.get('type') == u'array':
            if variable.get('id') == name:
                [data['options'][index]['value']] = value
    set_data(id_, data)
    return code


def get_strings(id_):
    strings = []
    for variable in get_data(id_, 'options'):
        if variable.get('type') == u'string' or not 'type' in variable.keys():
            if isinstance(variable.get('value'), basestring):
                var_id = variable.get('id')
                var_desc = variable.get('description') or variable.get('id')
                var_value = variable.get('value')
                strings.append((var_id, var_desc, var_value))
    return strings


def set_string(id_, name, value):
    code = False
    data = get_data(id_)
    for index, variable in enumerate(data.get('options')):
        if variable.get('type') == u'string' or not 'type' in variable.keys():
            if variable.get('id') == name:
                data['options'][index]['value'] = value
    set_data(id_, data)
    return code


def delete(id):
    code = True
    message = u''
    try:
        config.rm_rf(id)
    except TestsuiteError as e:
        code = False
        message = u'Не могу удалить задачу ' + id + u': ' + e.message
    return code, message


class Runnable:
    def __init__(self):
        pass

    def on_progress(self, pct):
        pass


    def on_stdout(self, msg):
        pass


    def on_stderr(self, err):
        pass


    def on_exit(self, code):
        pass


    def make_env(self, id):
        try:
            os.makedirs(os.path.join(id, u'input'))
            os.makedirs(os.path.join(id, u'output'))
            os.makedirs(os.path.join(id, u'tmp'))
        except OSError as e:
            print u'Не могу создать каталог: ' + e.strerror
            return

        env_fd = codecs.open(os.path.join(id, u'conf'), 'w', encoding='utf-8')

        for name, description, value in get_strings(id):
            env_fd.write(name + u'="' + value + u'"\n')

        for name, description, value in get_arrays(id):
            with open(os.path.join(id, u'input', name), 'w') as arr_fd:
                for str in value:
                    arr_fd.write(str + u'\n')

        src = os.path.relpath(get_data(id, 'src'), id)
        root = os.path.relpath(os.getcwd(), id)
        src.encode('utf-8')
        env_fd.write(u'ROOTDIR="' + root + u'"\n')
        env_fd.write(u'SRCDIR="' + src + u'"\n')
        env_fd.write(u'LIBDIR="' + src + u'"\n')
        env_fd.write(u'PATH="' + os.environ['PATH'] + u':' + src + u'"\n')


    def run(self, id):
        code = True
        message = u''
        retval = 0

        src = get_data(id, 'src')
        cmd = os.path.join(src, 'run')
        cwd = id

        config.rm_rf(id, mindepth=1)
        self.make_env(id)
        self.on_stdout(u'')
        self.on_stderr(u'')

        try:
            p = subprocess.Popen([os.path.relpath(cmd, cwd)],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 cwd=cwd)

        except (OSError, ValueError) as e:
            code = False
            message = u'Не могу запустить процесс ' + id + u': ' + e.strerror
            return code, retval, message

        while True:
            sleep(.01)
            ret, out = terminal.myreadstr(p.stdout)
            if ret == 0:
                self.on_stdout(out.decode('utf-8'))
            ret, err = terminal.myreadstr(p.stderr)
            if ret == 0:
                self.on_stderr(err.decode('utf-8'))

            retval = p.poll()
            if retval != None:
                break

        self.on_exit(code)

        return code, retval, message
