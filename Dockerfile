FROM python:3.11-slim

# Устанавливаем необходимые пакеты для установки uv и другие зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    gcc \
    python3-dev \
    pip \
    libpq-dev \
    build-essential \
    supervisor \
    nano \
    mc \
    iputils-ping \
    locales \
    tzdata \
    ssh \
    postgresql-client \
    && sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen && locale-gen \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install uv

# Копируем проект в образ
ADD . /opt/app

# Устанавливаем рабочую директорию
WORKDIR /opt/app

# Устанавливаем зависимости проекта
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-editable

# Устанавливаем переменную окружения для использования виртуальной среды
ENV PATH="/opt/app/.venv/bin:$PATH"

# Устанавливаем переменные окружения для локализации
ENV LANG ru_RU:ru
ENV LANGUAGE ru_RU:ru
ENV LC_ALL ru_RU.UTF-8

# Копируем конфигурацию Supervisor
COPY supervisor/supervisord.conf /etc/supervisor/supervisord.conf
COPY supervisor/serv.conf /etc/supervisor/conf.d/app.conf

# Определяем тома
VOLUME /data/
VOLUME /conf/
VOLUME /static/
VOLUME /media/
VOLUME /logs/

# Устанавливаем права на entrypoint.sh
RUN chmod +x /opt/app/entrypoint.sh

# Команда запуска
CMD rm -rf static; ln -s /static static; \
    rm -rf media; ln -s /media media; \
    rm -rf logs; ln -s /logs logs; \
    /usr/bin/supervisord -c /etc/supervisor/supervisord.conf --nodaemon
