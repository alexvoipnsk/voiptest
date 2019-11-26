#!/bin/bash

# Тест TAUxx.
#
# Переменные командной строки
# $1 TAU_IP_address:port 1
# $2 SIPP_IP_address
# $3 SIPP_PORT1

TAUIP=$1
SIPPIP=$2
SIPPORT=$3

# Путь к скриптам
SRC_PATH=~/test/tauxx/bug
TEMP_PATH=~/test/temp
AUDIO_PATH=../test/audio

# Путь к sipp
SIPP_PATH=~/sipp

# Номера абонентов
# Number A - SIP user
# USER_A=200100
# DOM_A=voip.local

# Удаляем файлы с данными (на случай, если они не были удалены)
#sudo rm $TEMP_PATH/$USER_A-$USER_B.csv

# Удаляем файл (необходим для поиска ошибки) с результатами по каждому тесту
sudo rm $TEMP_PATH/results_taubug.txt

# Создаем файлы с данными
#echo "SEQUENTIAL;
#$USER_A;$DOM_A;$USER_B;" > $TEMP_PATH/$USER_A-$USER_B.csv

# Переменные для подсчета успешных, неуспешных вызовов и номер теста
FAIL_COUNT=0
SUCC_COUNT=0

# Функция подсчета успешных и неуспешных вызовов
REZULT ()
{
  if test $? -ne 0
      then
          FAIL_COUNT=$(($FAIL_COUNT+1))
          echo Test $COUNT failed >> $TEMP_PATH/results_taubug.txt
      else
          SUCC_COUNT=$(($SUCC_COUNT+1))
          echo Test $COUNT passed >> $TEMP_PATH/results_taubug.txt
  fi
}

## Set DSCP for traffic
sudo iptables -t mangle -A OUTPUT -p udp -m udp --sport $4 -j DSCP --set-dscp-class cs3 # mark SIP UDP packets with CS3
sudo iptables -t mangle -A OUTPUT -p udp -m udp --sport 6000:8887 -j DSCP --set-dscp-class ef # mark RTP packets with EF

## Registrations

COUNT=1
sudo $SIPP_PATH/sipp $TAUIP -sf $SRC_PATH/regans_408.xml -mi $SIPPIP -m 1 -nd -i $SIPPIP -p $SIPPORT -recv_timeout 200s -timeout_error &
REZULT
sleep 2

# Удаляем файлы с данными
#sudo rm $TEMP_PATH/$USER_A-$USER_B.csv

# Вывод результата  
echo "Success $SUCC_COUNT, Failed $FAIL_COUNT"	

  if test $FAIL_COUNT -ne 0
        then 
        exit 1
        else 
        exit 0
  fi
