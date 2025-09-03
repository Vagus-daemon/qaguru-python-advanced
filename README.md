1. Клонировать репозиторий

```bash
git clone https://github.com/Vagus-daemon/qaguru-python-advanced.git
```

2. Установить зависимости

```bash
poetry update
```

3. Запустить postgresql в докере

```bash
docker compose up -d
```

4. Запустить api микросервис

```bash
python  main.py
```

5. Запустить тесты командой

```bash
pytest
```