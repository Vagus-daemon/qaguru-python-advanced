1. Клонировать репозиторий

```bash
git clone https://github.com/Vagus-daemon/qaguru-python-advanced.git
```

2. Установить зависимости

```bash
poetry update
```

3. Запустить postgresql  и прилоэение в докере

```bash
docker compose up 
```

4. Запустить тесты командой

```bash
pytest
```