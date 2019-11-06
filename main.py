#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, signal

code = 127

try:
    cwd = os.path.dirname(os.path.realpath(__file__))
    os.chdir(cwd)
    #print ("cwd=", cwd)
except:
    pass
    #sys.exit()

sys.path.append('./modules/')

# Обработка ключей, нужен ли запуск в консольном режиме?
for arg in sys.argv:
    if arg == u'--run':
        import ui.cli.shell as shell

# Наверное переделать, запуск делать в зависимоти от ключей
if len(sys.argv) == 1:
    import ui.dialog.shell as shell

# Создание группы для текущего процесса и перевод в нее процесса
try:
    os.setpgrp()
except:
    pass
#print (os.getpgrp())

try:
    code = shell.main()
except:
    try:
        os.killpg(0, signal.SIGTERM)
    except:
        pass

    shell.exit()
    pass

sys.exit(code)
