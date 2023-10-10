#!/bin/bash

if [ $1="env" ];then
    . settings.env
fi
python3 ./gpt-bot.py