# -*- coding: utf-8 -*-

import os, sys
import testsuite


def log_to(msg, fd=None, func=None):
    if fd:
        fd.write(msg.encode('utf-8'))
        fd.flush()
    if func:
        func()


def save(*argv):
    pass


def load(*argv):
    pass


def set(*argv):
    if argv[0] == u'job':
        set_job(argv)
    pass


def set_job(*argv):
    if argv[0] == u'name':
        pass
    elif argv[0] == u'number':
        pass
    elif argv[0] == u'variable':
        pass
    pass


def set_job_name(*argv):
    pass


def set_job_number(*argv):
    pass


def set_job_variable(*argv):
    pass


def show(*argv):
    if argv[0] == u'jobs':
        show_jobs(argv)
    elif argv[0] == u'job':
        show_job(argv)
    elif argv[0] == u'templates':
        show_templates(argv)
    elif argv[0] == u'template':
        show_template(argv)
    pass


def show_jobs(*argv):
    pass


def show_job(*argv):
    if argv[0] == u'name':
        pass
    elif argv[0] == u'number':
        pass
    elif argv[0] == u'variables':
        pass
    elif argv[0] == u'variable':
        pass
    pass


def show_job_variables(*argv):
    pass


def show_job_variable(*argv):
    pass


def show_templates(*argv):
    pass


def show_template(*argv):
    pass


def run():
    code, jobs, message = testsuite.get_jobs()
    if not code:
        return

    message = u''
    retval = 0
    for number, id_ in enumerate(jobs):

        stdout = open(os.path.join(id_, u'stdout.log'), 'w')
        stderr = open(os.path.join(id_, u'stderr.log'), 'w')

        name = testsuite.job.get_name(id_)
        sys.stdout.write(name.ljust(80))

        runnable = testsuite.job.Runnable()
        runnable.on_stdout = lambda msg: log_to(msg, stdout)
        runnable.on_stderr = lambda msg: log_to(msg, stderr)

        code, exit_code, message = runnable.run(id_)

        if not code:
            break

        if exit_code != 0:
            retval = exit_code

        sys.stdout.write(str(exit_code) + u'\n')

    return code, retval, message


def main():
    code, exit_code, message =  run()
    if not code:
        sys.stderr.write(message + u'\n')

    if exit_code != 0:
        sys.stderr.write(u'Во время выполнения теста были ошибки\n')

    return exit_code
