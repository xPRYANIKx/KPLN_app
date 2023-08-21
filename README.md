
## 1.1. БАЗА ДАННЫХ
**1.1.1. Настройка логирования БД на Windows**

Для настройки логирования базы данных **PostgreSQL** на **Windows** в виде **CSV**, следуйте инструкциям ниже:

 1. Откройте файл `postgresql.conf`, который находится в каталоге установки **PostgreSQL** (обычно в `C:\Program Files\PostgreSQL\<версия>\data`).
 2. Найдите параметр `logging_collector` и установите его значение в `on`. Этот параметр включает сбор логов.
 3. Найдите параметр `log_destination` и установите его значение в `csvlog`. Этот параметр указывает, что логи должны записываться в формате **CSV**.
 4. Найдите параметр `log_directory` и установите путь к каталогу, в котором будут сохраняться логи. Например, `log_directory = 'C:/PostgreSQL/Logs'`.
 5. Найдите параметр `log_filename` и установите паттерн имени файла логов. Например, `log_filename = 'postgresql-%Y-%m-%d_%H%M%S.csv'`. Это позволит создавать файлы логов с уникальными именами на основе текущей даты и времени.
 6. Сохраните файл `postgresql.conf`.

**1.1.2. Настройка логирования БД на Linux**

 1. Откройте файл конфигурации PostgreSQL, который обычно называется `postgresql.conf`.
   Расположение этого файла может различаться в зависимости от вашей установки PostgreSQL, но обычно он находится в директории `/etc/postgresql/<версия>/main/`.
 2. Найдите секцию `Logging and Reporting` в файле конфигурации.
 3. Раскомментируйте или добавьте следующие строки в секцию `Logging and Reporting`:
   ```
   log_destination = 'csvlog'
   logging_collector = on
   log_directory = '<путь_к_директории_логов>'
   log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
   ```
Здесь `<путь_к_директории_логов>` должен быть путем к директории, где вы хотите хранить лог-файлы в формате CSV. Вы можете выбрать любую директорию на вашем сервере.

 4. Сохраните файл конфигурации и перезапустите службу **PostgreSQL**, чтобы изменения вступили в силу. На большинстве **Linux-систем** вы можете использовать следующую команду для перезапуска:
   ```
   sudo service postgresql restart
   ```
Теперь **PostgreSQL** будет логировать события в базе данных в формате **CSV**. Лог-файлы будут сохраняться в указанной вами директории с именем `postgresql-<дата_и_время>.log`.
Обратите внимание, что лог-файлы могут занимать значительное место на диске, поэтому регулярно проверяйте их размер и удаляйте старые файлы, если они больше не нужны.
