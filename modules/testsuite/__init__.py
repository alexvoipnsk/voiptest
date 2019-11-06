# -*- coding: utf-8 -*-

import os
import template
import job
import config
from error import TestsuiteError


def make_job(template_id, number, name):
    code = True
    message = u''

    job_id = os.path.join(config.JOBS_ROOT, ("%04d-%s" % (number, name)))

    try:
        config.mkdir(job_id)
        data = template.get_data(template_id)
        data.update({'src': template_id})
        job.set_data(job_id, data)
    except TestsuiteError as e:
        code = False
        message = e.message

    return code, message


def clean(path=config.JOBS_ROOT):
    config.rm_rf(path, mindepth=1)


def get_saves(path=config.SAVES_PATH):
    code = True
    data = u''
    try:
        data = config.get_saves(path)
    except TestsuiteError as e:
        code = False
        data = e.message
    return code, data


def save(name):
    code = True
    strerror = u''
    try:
        config.save(name)
    except TestsuiteError as e:
        code = False
        strerror = e.message
    return code, strerror


def load(name):
    code = True
    message = u''
    try:
        clean()
        config.load(name)
    except TestsuiteError as e:
        code = False
        message = e.message
    return code, message


def get_templates(path):
    return template.get_list(path)


def get_jobs(path=config.JOBS_ROOT):
    code = True
    jobs = []
    message = u''
    try:
        jobs = config.ls(path, sorted=True)
    except TestsuiteError as e:
        code = False
        message = e.message
    return code, jobs, message


class Testsuite:
    prio = 0


    def __init__(self):
        pass

    def get_next_step(self):
        jobs = []
        for id_ in get_jobs():
            prio = job.get_number(id_)
            if prio == self.prio:
                jobs.append(id_)
        return jobs

    def run_next_step(self):
        code = 0
        jobs = self.get_next_step()
        for id_ in jobs:
            runnable = job.Runnable()
        return code

    def run(self):
        code = 0
        exit_code = True
        message = u''
        while True:
            try:
                exit_code = self.run_next_step()
                if exit_code != 0:
                    break
            except TestsuiteError as e:
                code = False
                break

        return code, exit_code, message


class Runnable:
    def __init__(self):
        pass
