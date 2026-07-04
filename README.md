# Лабораторная работа №8: Kubernetes - Helm и Kustomize

## Описание

Цель лабораторной работы - освоить инструменты **Helm** и **Kustomize** для управления приложениями в Kubernetes.

В ходе работы были выполнены две задачи:

1. На сервере **Ubuntu 24.04** из проекта **Prometheus + Grafana** создан Helm Chart и выполнено развертывание системы мониторинга в Kubernetes.
2. На сервере **Linux Debian** для приложения **Flask + Redis** созданы окружения **Development** и **Production** с использованием **Kustomize**.

---

## Выполнение работы

### Сервер Ubuntu 24.04

**Проект:** Prometheus + Grafana

Структура проекта:

```text
.
├── blackbox-deployment.yaml
├── blackbox-service.yaml
├── compose.yml
├── grafana
│   └── datasource.yml
├── grafana-cm0-configmap.yaml
├── grafana-data-persistentvolumeclaim.yaml
├── grafana-deployment.yaml
├── grafana-service.yaml
├── prom-data-persistentvolumeclaim.yaml
├── prometheus
│   └── prometheus.yml
├── prometheus-cm0-configmap.yaml
├── prometheus-deployment.yaml
├── prometheus-service.yaml
├── promgra
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── README.md
│   └── templates
│       ├── blackbox-deployment.yaml
│       ├── blackbox-service.yaml
│       ├── grafana-cm0-configmap.yaml
│       ├── grafana-data-persistentvolumeclaim.yaml
│       ├── grafana-deployment.yaml
│       ├── grafana-service.yaml
│       ├── prom-data-persistentvolumeclaim.yaml
│       ├── prometheus-cm0-configmap.yaml
│       ├── prometheus-deployment.yaml
│       └── prometheus-service.yaml
└── promgra-0.0.1.tgz
```

### Helm Chart

Для системы мониторинга создан Helm Chart `promgra`, содержащий шаблоны для следующих компонентов:

- Prometheus;
- Grafana;
- Blackbox Exporter;
- Services;
- PersistentVolumeClaims;
- ConfigMap.

### Файл `values.yaml`

Параметризованы основные настройки Helm Chart:

- внешний IP-адрес;
- внешний порт Grafana;
- пароль администратора Grafana.

Пример:

```yaml
EXTERNAL_IP: 172.16.10.3
EXTERNAL_PORT: 3113
GF_ADMIN_PASSWORD: HiGrafana
```

### Развертывание

Установка Helm Chart:

```bash
helm install promgra ./promgra-0.0.1.tgz
```

Изменение параметров релиза:

```bash
helm upgrade promgra ./ --set EXTERNAL_PORT=3456
```

Проверка установленных значений:

```bash
helm get values promgra --all
```

В результате в кластере были развернуты:

- Prometheus;
- Grafana;
- Blackbox Exporter;
- необходимые сервисы и постоянные тома хранения данных.

---

## Сервер Debian

**Проект:** Flask + Redis

Структура проекта:

```text
.
├── base
│   ├── flask_redis
│   │   ├── app.py
│   │   ├── compose.yml
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── flask.yml
│   ├── flask-service.yml
│   ├── redis.yml
│   ├── redis-service.yml
│   └── kustomization.yaml
├── dev
│   ├── deployment-patch.yaml
│   ├── service-patch.yaml
│   └── kustomization.yaml
└── prod
    ├── deployment-patch.yaml
    └── kustomization.yaml
```

### Base

Каталог `base` содержит общие Kubernetes-манифесты:

- Deployment Flask;
- Deployment Redis;
- Service Flask;
- Service Redis;
- базовый файл `kustomization.yaml`.

### Development

Каталог `dev` содержит патчи для окружения разработки:

- собственное имя Deployment;
- отдельный Service;
- настройки окружения **DEVELOPMENT**;
- собственный внешний порт.

Развертывание:

```bash
kubectl apply -k dev
```

### Production

Каталог `prod` содержит патчи для рабочего окружения:

- собственное имя Deployment;
- настройки окружения **PRODUCTION**;
- отдельный внешний порт;
- возможность выполнения Rolling Update.

Развертывание:

```bash
kubectl apply -k prod
```

Перезапуск Deployment:

```bash
kubectl rollout restart deployment prod-flask-app
```

---

## Результат

После выполнения лабораторной работы:

### Helm

- создан собственный Helm Chart;
- Prometheus, Grafana и Blackbox Exporter успешно развернуты в Kubernetes;
- параметры приложения настраиваются через файл `values.yaml`;
- выполнено обновление релиза с помощью `helm upgrade`.

### Kustomize

Созданы два независимых окружения:

- **Development**
- **Production**

Каждое окружение имеет:

- собственный Deployment;
- собственный Service;
- собственные настройки;
- отдельный внешний порт.

Пример ответа приложения Development:

```text
Hello World VERSION 5! I have been seen 935 times.
My name is: dev-flask-app-f57bd98f9-vgh4k
My env: DEVELOPMENT
```

Пример ответа приложения Production:

```text
Hello World VERSION 5! I have been seen 945 times.
My name is: prod-flask-app-58549967fb-gkh8n
My env: PRODUCTION
```

Во время обращения к приложению наблюдается смена имени Pod, что подтверждает работу нескольких реплик и корректное выполнение **Rolling Update**.

## Используемые технологии

- Kubernetes
- Helm
- Kustomize
- Docker
- Flask
- Redis
- Prometheus
- Grafana
- Blackbox Exporter
- YAML
