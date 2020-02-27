
import struct

from processor.sorm.constants import (CommandCode,
                               MessageCode1,
                               MessageCode2,
                               Const,
                              )
import processor.sorm.utils as utils



# Header fields

def preamble(value):
    return 'Преамбула 0x{:02X}: '.format(value) + {
        Const.PREAMBLE: 'Верная'
    }.get(value, 'ОШИБКА! Ожидается 0x{:02X}'.format(Const.PREAMBLE))


def sormNumber(value):
    return 'Номер технических средств ОРМ 0x{:02X}: {}'.format(value, value)


def commandCode(value):
    return 'КОМАНДА 0x{:02X}: '.format(value) + {
        CommandCode.SORM_START              : '1 Запуск технических средств ОРМ',
        CommandCode.SORM_STOP               : '2 Останов технических средств ОРМ',
        CommandCode.PASSWORD_SET            : '3 Задание пароля',
        CommandCode.CONTROL_LINE_ADD        : '4 Закрепление КСЛ за группой',
        CommandCode.OBJECT_ADD              : '5 Постановка объекта на контроль',
        CommandCode.OBJECT_REMOVE           : '6 Снятие объекта с контроля',
        CommandCode.CONTROL_LINE_CONNECT    : '7 Подключение к разговорному тракту',
        CommandCode.CONTROL_LINE_DISCONNECT : '8 Освобождение КСЛ',
        CommandCode.CONTROL_LINE_REMOVE     : '9 Исключение КСЛ из группы',
        CommandCode.OBJECT_GET_INFO         : '10 Запрос на передачу данных об объектах контроля',
        CommandCode.CONTROL_LINE_GET_INFO   : '11 Запрос на передачу информации о соответствии между КСЛ и группами',
        CommandCode.SERVICES_GET_INFO       : '12 Запрос на передачу списка услуг связи',
        CommandCode.COMMAND_INTERRUPT       : '13 Прерывание выдачи сообщений на запросы содержимого таблиц',
        CommandCode.TEST_REQUEST            : '14 Тестирование каналов передачи данных',
        CommandCode.OBJECT_CHANGE           : '15 Изменение параметров объекта контроля',
        CommandCode.LINKSET_GET_INFO        : '16 Запрос на передачу информации о соответствии имени пучка каналов и его условного номера',
        CommandCode.FIRMWARE_VERSION_GET    : '17 Запрос версии ПО узла связи',
        }.get(value, 'ОШИБКА! Неизвестная команда')


def payloadLength(value):
    return 'Длина команды в байтах 0x{:02X}: {}'.format(value, value)


def password(value):
    valueBytes = utils.printableBytes(value.encode(Const.DEFAULT_CODEC))
    return 'Пароль 0x{}: {}'.format(valueBytes, value)


def messageCode1(value):
    return 'СООБЩЕНИЕ КПД1 0x{:02X}: '.format(value) + {
        MessageCode1.STATION_FAILURE        : '1 Авария',
        MessageCode1.FIRMWARE_REBOOT        : '2 Перезапуск ПО станции',
        MessageCode1.OBJECT_INFO            : '3 Данные об объектах контроля',
        MessageCode1.CONTROL_LINE_INFO      : '4 Информация о соответствии между КСЛ и группами',
        MessageCode1.SERVICES_INFO          : '5 Список услуг связи',
        MessageCode1.INTRUSION              : '6 Несанкционированный доступ к программным средствам технических средств ОРМ',
        MessageCode1.CONFIRM_RECEIPT        : '7 Подтверждение приёма команды из пункта управления ОРМ',
        MessageCode1.CONFIRM_EXECUTION      : '8 Подтверждение о выполнении команды из пункта управления ОРМ',
        MessageCode1.TEST_RESPONSE          : '9 Ответное тестовое сообщение',
        MessageCode1.LINKSET_INFO           : '10 Данные о соответствии условных номеров пучков каналов и их реальных станционных имён',
        MessageCode1.FIRMWARE_VERSION_INFO  : '11 Версия ПО станции',
        MessageCode1.MESSAGE_TRANSMISSION   : '12 Передача сообщений электросвязи',
        }.get(value, 'ОШИБКА: Неизвестное сообщение')


def messageCode2(value):
    return 'СООБЩЕНИЕ КПД2 0x{:02X}: '.format(value) + {
        MessageCode2.CALL_SETUP             : '1.1 Приём полного номера телефона вызываемого',
        MessageCode2.CALL_ANSWER            : '1.2 Ответ вызываемого абонента',
        MessageCode2.CALL_HANGUP            : '1.3 Разъединение',
        MessageCode2.VAS_ACTIVATION         : '1.4 Использование услуг связи',
        MessageCode2.CONTROL_LINE_CONNECTED : '2.1 Подключение контрольной соединительной линии',
        MessageCode2.CONTROL_LINE_DISCONNECTED : '2.2 Освобождение контрольной соединительной линии',
        MessageCode2.TEST_RESPONSE          : '2.3 Ответное тестовое сообщение',
        }.get(value, 'ОШИБКА: Неизвестное сообщение')


def messagesCount(value):
    valueBytes = utils.printableBytes(struct.pack('<1H', value))
    return 'Количество сообщений 0x{}: {}'.format(valueBytes, value)


def messagesNumber(value):
    valueBytes = utils.printableBytes(struct.pack('<1H', value))
    return 'Номер сообщения 0x{}: {}'.format(valueBytes, value)


def reserve(value):
    return 'Байт "Резерв" 0x{:02X}: '.format(value) + {
        Const.MSG1_RESERVE_BYTE: 'Верный',
    }.get(value, 'ОШИБКА! Ожидается 0x{:02X}'.format(Const.MSG1_RESERVE_BYTE))


def version(value):
    return 'Версия технических требований 0x{:02X}: '.format(value) + {
        Const.MSG1_SORM_VERSION: 'Верная',
    }.get(value, 'ОШИБКА! Ожидается 0x{:02X}'.format(Const.MSG1_SORM_VERSION))


def selectionSign(value):
    return 'Признак отбора объекта контроля 0x{:02X}: '.format(value) + {
        0x01: 'А-номер, полный совмещённый',
        0x03: 'А-номер, полный раздельный',
        0x02: 'А-номер, статистический',

        0x04: 'Б-номер, полный совмещённый',
        0x0C: 'Б-номер, полный раздельный',
        0x08: 'Б-номер, статистический',

        0x10: 'Пучок каналов, полный совмещённый',
        0x30: 'Пучок каналов, полный раздельный',
        0x20: 'Пучок каналов, статистический',

        0x40: 'ДВО, полный совмещённый',
        0xC0: 'ДВО, полный раздельный',
        0x80: 'ДВО, статистический',
    }.get(value, 'ОШИБКА! Неизвестный признак')


def callAttribute(value):
    return 'Параметры связи 0x{:02X}: '.format(value) + {
        0x11: 'Исходящая, установлена автоматикой)',
        0x12: 'Входящая, установлена автоматикой)',
        0x14: 'МН транзит, установлена автоматикой)',
        0x18: 'МГ транзит, установлена автоматикой)',
        0x1C: 'Внутристанционная, установлена автоматикой)',

        0x21: 'Исходящая, установлена полуавтоматикой)',
        0x22: 'Входящая, установлена полуавтоматикой)',
        0x24: 'МН транзит, установлена полуавтоматикой)',
        0x28: 'МГ транзит, установлена полуавтоматикой)',
        0x2C: 'Внутристанционная, установлена полуавтоматикой)',
    }.get(value, 'ОШИБКА! Неизвестные параметры')


def vasPhase(value):
    return 'Код фазы услуги 0x{:02X}: '.format(value) + {
        0x00: 'Обычный вызов)',
        0x01: 'Заказ услуги)',
        0x02: 'Проверка услуги)',
        0x03: 'Отмена услуги)',
        0x04: 'Активизация услуги)',
        0x05: 'Передача информации при установленном соединении)',
    }.get(value, 'ОШИБКА! Неизвестные параметры')



# Payload fields

def newPassword(value):
    valueBytes = utils.printableBytes(value.encode(Const.DEFAULT_CODEC))
    return 'Новый пароль 0x{}: {}'.format(valueBytes, value)


def lineGroupNumber(value):
    return 'Номер группы КСЛ 0x{:02X}: {}'.format(value, value)


def lineGroupType(value):
    return 'Тип группы КСЛ 0x{:02X}: '.format(value) + {
        0x01: 'Группа для совмещенного контроля',
        0x11: 'Группа для раздельного контроля',
    }.get(value, 'ОШИБКА! Неизвестный тип')


def lineANumber(stream, line):
    return 'Номер КСЛ-А 0x{:02X}: Поток {}, КСЛ {}'.format(utils.mergeStreamAndLine(stream, line),
                                                           stream,
                                                           line
                                                          )


def lineBNumber(stream, line):
    return 'Номер КСЛ-Б 0x{:02X}: Поток {}, КСЛ {}'.format(utils.mergeStreamAndLine(stream, line),
                                                           stream,
                                                           line
                                                          )


def objectNumber(value):
    valueBytes = utils.printableBytes(struct.pack('<1H', value))
    return 'Номер объекта контроля 0x{}: {}'.format(valueBytes, value)


def objectType(value):
    return 'Тип объекта контроля 0x{:02X}: '.format(value) + {
        0x01: 'Абонент данного узла связи',
        0x02: 'Абонент ТфССОП с полным номером телефона или идентификатор',
        0x12: 'Абонент ТфССОП с неполным номером телефона',
        0x03: 'Пучок каналов',
    }.get(value, 'ОШИБКА! Неизвестный тип')


def phoneType(value):
    return 'Признак номера телефона 0x{:02X}: '.format(value) + {
        0x01: 'Абонент данного узла',
        0x04: 'Абонент ТфССОП России',
        0x05: 'Абонент ТфССОП другой страны',
        0x06: 'Телефон экстренных или справочно-информационных служб',
        0x07: 'Идентификатор IMSI или идентификатор СПРТС других стандартов',
        0xFF: '-',
    }.get(value, 'ОШИБКА! Неверный признак')


def phoneNumber(value):
    phoneBytes = utils.printableBytes(utils.phone2bcd(value))
    return 'Номер телефона 0x{}: {}'.format(phoneBytes, value)


def phoneLength(value):
    return 'Длина номера 0x{:02X}: {}'.format(value, value)


def linksetNumber(value):
    valueBytes = utils.printableBytes(struct.pack('<1H', value))
    return 'Номер пучка каналов 0x{}: {}'.format(valueBytes, value)


def controlCategory(value):
    return 'Категория контроля 0x{:02X}: '.format(value) + {
        0x01: 'Полный контроль (совмещенный)',
        0x11: 'Полный контроль (раздельный)',
        0x02: 'Статистический контроль',
    }.get(value, 'ОШИБКА! Неизвестная категория')


def priority(value):
    return 'Метка приоритета 0x{:02X}: '.format(value) + {
        0x01: 'Приоритетный объект контроля',
        0x02: 'Обычный объект контроля',
        0xFF: 'Обычный объект контроля (статистический контроль)'
    }.get(value, 'ОШИБКА! Неизвестная метка')


def testMessageNumber(value):
    return 'Номер тестового сообщения 0x{:02X}: {}'.format(value, value)


def callNumber(value):
    valueBytes = utils.printableBytes(struct.pack('<1H', value))
    return 'Номер вызова 0x{}: {}'.format(valueBytes, value)


def failureType(value):
    return 'Тип аварии 0x{:02X}: '.format(value) + {
        0x01: 'Искажение или потеря таблиц СОРМ',
        0x02: 'Таблицы СОРМ целы, требуется вмешательство оператора',
        0x03: 'Таблицы СОРМ целы, не требуется вмешательство оператора',
        0x04: 'Изменение характеристик линии связи',
    }.get(value, 'ОШИБКА! Неизвестный тип')


def failureCode(value):
    return 'Код аварии 0x{:02X}: '.format(value) + {
        0x01: 'Авария потока Е1 потеря сигнала (LOS)',
        0x02: 'Удалённая авария потока Е1 (RAI)',
        0x03: 'Перезапуск SIP-адаптера',
    }.get(value, 'ОШИБКА! Неизвестный код')


def subscriberSetState(value):
    return 'Состояние абонентского комплекта 0x{:02X}: '.format(value) + {
        0x00: 'Исправен, нет ограничений по пользованию связью',
        0x01: 'Неисправен',
        0x03: 'Заблокирован',
        0x07: 'Есть ограничения по пользованию связью',
        0xFF: 'Информация недоступна',
    }.get(value, 'ОШИБКА! Неизвестное состояние')


def vasCount(value):
    return 'Общее количество услуг связи 0x{:02X}: {}'.format(value, value)


def vasCode(value):
    return 'Код услуги связи 0x{:02X}: '.format(value) + {
        0x21: 'Безусловная переадресация (CFU)',
        0x29: 'Переадресация при занятости (CFB)',
        0x2A: 'Переадресация при неответе (CFNR)',
        0x20: 'Любая переадресация (All CF)',
        0x42: 'Удержание вызова (HOLD)',
        0x52: 'Трехсторонняя связь (3PTY)',
        0x50: 'Все многосторонние конференции (CONF)',
        0x31: 'Передача вызова (CT)',
        0x32: 'Перехват вызова (CP)',
        0xFF: '-',
    }.get(value, 'ОШИБКА! Неизвестный код')


def intrusionCode(value):
    return 'Код доступа 0x{:02X}: '.format(value) + {
        0x01: 'Доступ с запрещённого порта',
        0x02: 'Доступ с ошибочным паролем',
        0x03: 'Чтение/запись таблиц данных технических средств ОРМ',
        0x04: 'Переназначение порта связи с ПУ',
        0x05: 'Доступ с неправильным номером технических средств ОРМ'
        }.get(value, 'ОШИБКА! Неизвестный код')


def eventDate(day, hour, minute, second):
    valueBytes = utils.printableBytes(struct.pack('<4B', day, hour, minute, second))
    return 'Время события 0x{}: день {} в {:02}:{:02}:{:02}'.format(valueBytes, day, hour, minute, second)


def intrusionMessage(value):
    return 'Дополнительная информация: {}'.format(value)


eltexStatus = {
    0x10: 'Eltex: неверная длина команды или количество знаков в номере',
    0x11: 'Eltex: ошибка параметров',
    0x12: 'Eltex: неверный тип объекта',
    0x13: 'Eltex: неверный тип номера',
    0x14: 'Eltex: неверная категория',
    0x15: 'Eltex: ошибка приоритета',
    0x16: 'Eltex: не принята: СОРМ уже стартовал',
    0x17: 'Eltex: не принята: СОРМ не запущен',
    0x18: 'Eltex: не принята: неверный номер СОРМ',
    0x19: 'Eltex: неверная длина номера',
    0x20: 'Eltex: Не задан ни номер, ни транк при постановке на контроль',
    0x21: 'Eltex: прервано по команде ПУ',
    0x25: 'Eltex: транк-группа не задана',
    0x2D: 'Eltex: не принята: идёт выполнение ранее поданой команды',
    0x30: 'Eltex: группа определена другим типом',
    0x31: 'Eltex: таблица объектов переполнена, мониторинг не начат',
    0x32: 'Eltex: в указанной группе нет такой КСЛ',
    0x33: 'Eltex: объект уже задан',
    0x34: 'Eltex: неверный номер объекта',
    0x35: 'Eltex: номер не найден',
    0x36: 'Eltex: номер уже задан',
    0x37: 'Eltex: номер объекта не подходит для команды',
    0x38: 'Eltex: неверный тип объекта или неверный тип номера',
    0x39: 'Eltex: вывод уже завершен',
    0x3A: 'Eltex: КСЛ-А уже закреплена',
    0x3B: 'Eltex: совпадает номер',
    0x3D: 'Eltex: неверный номер объекта',
    0x3E: 'Eltex: неверный номер группы КСЛ',
    0x3F: 'Eltex: неверный номер КСЛ-А',
    0x40: 'Eltex: не совпадающая/неверная КСЛ',
    0x41: 'Eltex: ошибка команды',
    0x44: 'Eltex: количество цифр не совпадает',
    0x47: 'Eltex: не задан номер для транка',
    0x48: 'Eltex: задан и номер объекта и номер транка',
    0x49: 'Eltex: не найден транк с таким номером',
    0x4A: 'Eltex: такой транк уже контроллируется',
    0x4B: 'Eltex: общее количество контроллируемых транков достигло десяти',
    0x4C: 'Eltex: номер транка не совпадает с ранее заданным',
    0x4E: 'Eltex: задан номер транка не для того типа объекта',
    0x53: 'Eltex: не найден ни номер, ни направление',
    0x54: 'Eltex: порт не локальный',
    0x55: 'Eltex: признак номера неверен',
    0x56: 'Eltex: неверный тип объекта для локального порта',
    0x57: 'Eltex: передан неподходящий признак номера для данного номера',
    0x5F: 'Eltex: нет КСЛ, соответствующих запросу, КСЛ не выбрана',
    0x61: 'Eltex: ДВО не заданы',
    0x73: 'Eltex: ошибка выделения КСЛ',
    }


def receiptStatus(value):
    statusText = {
        0x00: 'Принято к исполнению',
        0x01: 'Отказ - неверный формат или параметры команды',
        0x02: 'Отказ - СОРМ не запущен',
        }
    statusText.update(eltexStatus)
    return 'Признак приёма команды 0x{:02X}: '.format(value) +\
            statusText.get(value, '(ОШИБКА! Неизвестный признак)')


def executionStatus(value):
    statusText = {
        0x00: 'Выполнена успешно',
        0x01: 'Не выполнена',
        0x03: 'Не выполнена - неверный пароль',
        0x05: 'Не выполнена - неверный номер технических средств ОРМ',
        0x07: 'Не выполнена - технические средства ОРМ запущены',
        }
    statusText.update(eltexStatus)
    return 'Признак выполнения команды 0x{:02X}: '.format(value) +\
            statusText.get(value, '(ОШИБКА! Неизвестный признак')


def controlChannelStatus(channel1, channel2):
    return 'Состояние КПД1 0x{:02X}; КПД2 0x{:02X}:'.format(channel1, channel2) + '\n' +\
           'Поток: ' + ''.join(['{:<3}'.format(i) for i in reversed(range(8))]) + '\n' +\
           'КПД1:  ' + ''.join(['{:<3}'.format(i) for i in utils.int2bitarray(channel1)]) + '\n' +\
           'КПД2:  ' + ''.join(['{:<3}'.format(i) for i in utils.int2bitarray(channel2)])


def linksetName(value):
    return 'Станционное имя пучка каналов: {}'.format(value)


def firmwareVersion(value):
    return 'Версия ПО станции: {}'.format(value)


def stationType(value):
    return 'Тип узла связи 0x{:02X}: '.format(value) + {
        0x01: 'Оконечный',
        0x02: 'Транзитный',
        0x03: 'Оконечно-транзитный'
        }.get(value, 'ОШИБКА! Неизвестный тип')


def operationCode(value):
    return 'Код операции 0x{:02X} '.format(value) + {
        0x00: 'Нормальное подключение КСЛ',
        0x01: 'Нет доступных КСЛ в группе',
        0xFF: 'Статистический контроль',
    }.get(value, '(ОШИБКА! Неизвестный код!)')


def operationCodeDisconnect(value):
    return 'Код завершения соединения 0x{:02X} '.format(value) + {
        0x01: 'По техническим причинам)',
        0x02: 'После неполного набора)',
        0x03: 'При занятом вызываемом абоненте)',
        0x04: 'При неответе абонента Б)',
        0x05: 'После разговорного состояния)',
    }.get(value, '(ОШИБКА! Неизвестный код!)')


def operationCodeControlLineConnect(value):
    return 'Код подключения КСЛ 0x{:02X} '.format(value) + {
        0x00: 'Нормальное подключение',
    }.get(value, '(ОШИБКА! Неизвестный код)')


def operationCodeControlLineDisconnect(value):
    return 'Код освобождения КСЛ 0x{:02X} '.format(value) + {
        0x01: 'По команде №8 (Освобождение КСЛ)',
        0x02: 'По приоритету объекта контроля',
        0x03: 'По приоритету, выполнена команда №7 (Подключение к разговорному тракту)',
        0x04: 'Неисправность станционного оборудования',
        0x05: 'По команде №6 (Снятие объекта с контроля)',
        0x06: 'По команде №2 (Остановка СОРМ)',
    }.get(value, '(ОШИБКА! Неизвестный код!)')


def additionalCode(value):
    return 'Дополнительный код 0x{:02X}: {}'.format(value, value)


def unknownBytes(value):
    return 'Содержимое сообщения:\n0x' +\
            utils.printableBytes(struct.pack('<1H', value))
