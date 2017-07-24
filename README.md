# YaMetrika AddIPFilter

Скрипт, упрощающий добавление фильтров по IP-адресам в настройки счетчиков через API Яндекс.Метрики.

## Использование

1. Получите токен для работы с API. Можно запросить по ссылке: 
https://oauth.yandex.ru/authorize?response_type=token&client_id=<ID приложения>

2. Установите зависимости, определенные в `requirements.txt`, в виртуальное python-окружение с помощью команды:
    
        pip install -r requirements.txt


3. Запустите скрипт:

        python main.py --ip=<ip> --token=<token>

   Доступные параметры:
    
        --mode MODE        Режим: add или delete.
        --ip IP            IP-адрес для создания фильтра.
        --status STATUS    Статус фильтра: active или disabled.
        --action ACTION    Тип фильтра: include или exclude.
        --logfile LOGFILE  Текстовой файл для записи отчета.
        --token TOKEN      Токен для работы с API. Можно запросить по ссылке: 
                           https://oauth.yandex.ru/authorize?response_type=token&client_id=<ID приложения>



## Автор

Евгений Зятев ([eu@zyatev.ru](mailto:eu@zyatev.ru))