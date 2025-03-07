"""Приложение Posts для проекта Yatube."""

from django.apps import AppConfig


class PostsConfig(AppConfig):
    """Конфигурация приложения Posts."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
