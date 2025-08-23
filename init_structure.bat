@echo off
echo Создание структуры проекта PriceWatcherBot...

:: Каталоги
mkdir app
mkdir app\models
mkdir app\db
mkdir app\handlers
mkdir app\handlers\user
mkdir app\handlers\admin
mkdir app\services
mkdir app\keyboards
mkdir app\utils
mkdir tests
mkdir samples

:: Пустые Python-файлы
echo. > app\__init__.py
echo. > app\main.py
echo. > app\config.py

echo. > app\models\__init__.py
echo. > app\models\user.py
echo. > app\models\item.py

echo. > app\db\__init__.py
echo. > app\db\init_db.py
echo. > app\db\crud.py

echo. > app\handlers\__init__.py
echo. > app\handlers\user\__init__.py
echo. > app\handlers\user\start.py
echo. > app\handlers\user\add.py
echo. > app\handlers\user\list.py
echo. > app\handlers\user\settings.py
echo. > app\handlers\admin\__init__.py
echo. > app\handlers\admin\broadcast.py

echo. > app\services\__init__.py
echo. > app\services\parser.py
echo. > app\services\scheduler.py

echo. > app\keyboards\__init__.py
echo. > app\keyboards\reply.py
echo. > app\keyboards\inline.py

echo. > app\utils\__init__.py
echo. > app\utils\logging_config.py

echo. > tests\__init__.py
echo. > tests\test_parser.py
echo. > tests\test_scheduler.py

:: Примеры HTML
echo. > samples\product1.html

:: .env (шаблон)
echo BOT_TOKEN=your_token_here> .env
echo DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/dbname>> .env

:: requirements.txt
echo aiogram==3.* > requirements.txt
echo httpx >> requirements.txt
echo SQLModel >> requirements.txt
echo asyncpg >> requirements.txt
echo python-dotenv >> requirements.txt
echo APScheduler >> requirements.txt
echo beautifulsoup4 >> requirements.txt

:: Docker files
echo. > Dockerfile
echo. > docker-compose.yml

echo Структура проекта создана.
pause
