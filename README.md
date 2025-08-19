1. Клонировать репозиторий 
```bash
git clone https://github.com/Vagus-daemon/qaguru-python-advanced.git
```
2. В терминале в директории проекта создать и активировать виртуальное окружение
```bash
python -m venv .venv 
source .venv/bin/activate (Linux) / .\.venv\Scripts\Activate.ps1 (Windows)
```
3. Установить зависимости
```
pip install -r requirements.txt 
```
4. Запустить postgresql в докере
```bash
docker compose up -d
```
5. Запустить api микросервис
```bash
python  main.py
```
5. Запустить тесты командой
```bash
pytest
```