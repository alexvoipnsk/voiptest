# -*- coding: utf-8 -*-

from dialog import Dialog

import tempfile

def percent(number, percent):
    return int(float(number) / 100 * percent)

class UI():
    OK = 'ok'
    CANCEL = 'cancel'
    BACK = 'back'
    ESC = 'esc'

    BORDER_WIDTH = 5
    BORDER_HEIGHT = 6
    DETAIL_LINES = 2

    def __init__(self):
        self.d = Dialog(DIALOGRC=u'modules/ui/dialog/dialog.rc')
        return


    def draw_form(self, header, hint, inputs, size = (0, 0)):
        yl = 1
        xl = 1
        yi = 1
        xi = 40

        if size[1]:
            xi = (lambda x: x if x > 40 else 40)(percent(size[1], 20))
        field_length = 256
        input_length = 256
        elements = []

        for key, description, value in inputs:
            element = (description,
                       yl,
                       xl,
                       value,
                       yi,
                       xi,
                       field_length,
                       input_length,
                       0x0)
            elements.append(element)
            yl += 1
            yi += 1

        code, values = self.d.mixedform(header, elements, size[0], percent(size[1], 90), 0)
        out = inputs

        for i, v in enumerate(values):
            out[i] = (inputs[i][0], inputs[i][1], v)

        return code, out


    def draw_menu(self, header, hint, items, size = (0, 0)):
        height, width = size
        self.d.set_background_title(header)
        code, tags = self.d.menu(hint, height, width, 0, items)
        return code, tags


    def draw_yesno(self, text):
        code = self.d.yesno(text)
        return code


    def draw_msgbox(self, text):
        code = self.d.msgbox(text)
        return code


    def draw_gauge_start(self, title, text, size = (0,0), percent = 0):

        if not size:
            size = self.maxwindowsize

        height, width = size

        self.d.set_background_title(title)

        code = self.d.gauge_start(text, height, width, percent, no_collapse=True, cr_wrap=False)

        return code


    def draw_gauge_update(self, title, elements, percent=0, details=u'', size = (20, 76)):

        height, width = size

        data_area_height = height - self.BORDER_HEIGHT
        data_area_width = width - self.BORDER_WIDTH

        details_area_height = self.DETAIL_LINES
        details_area_width = self.BORDER_WIDTH

        main_area_height = data_area_height
        main_area_width = data_area_width

        out = u''

        for name, status in elements[-main_area_height:]:
            status = u'[{:^7}]'.format(status)
            max_name_len = main_area_width - len(status)
            #visible_name = (lambda x, n: x if x[-1] < n else x[:n])(name, max_name_len)
            visible_name = name
            x_padding = u''.join([u'.' for i in range(max_name_len - len(name) + 1)])
            out += visible_name + x_padding + status + u'\n'

        #y_padding = u''

#        for i in range(main_area_height - len(elements[-main_area_height:])):
#            y_padding += str(i) + u'\n'

        #out += y_padding
        #out += u'--\n'
        #out += details

        code = self.d.gauge_update(percent, out, True)

        return code


    def draw_gauge_stop(self):
        code = self.d.gauge_stop()
        return code

    def draw_mixedgauge(self, title, elements, percent, height, width):

        self.d.set_background_title(title)

        data_area_height = height - self.BORDER_HEIGHT
        data_area_width = width - self.BORDER_WIDTH

        code = self.d.mixedgauge(u'', height, width, percent, elements[-data_area_height:])
        return code


    def draw_array_editor(self, title, in_array, size = (0, 0)):

        self.d.set_background_title(title)

        with tempfile.NamedTemporaryFile('w') as file:
            for i in in_array:
                file.write(i + u'\n')
            file.flush()
            code, text = self.d.editbox(file.name, 0, 0)

        out_array = [text.splitlines()]
        return code, out_array


    def clear(self):
        self.d.clear()
        return


    def get_maxsize(self):
        return self.d.maxsize()


    def get_maxwindowsize(self):
        maxy, maxx = self.maxsize
        return maxy - 2, maxx


    maxsize = property(get_maxsize)

    maxwindowsize = property(get_maxwindowsize)
