"""Сериализаторы для моделей приложения Yatube."""

from rest_framework import serializers
from posts.models import Post, Group, Comment


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post."""

    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        """Метакласс для сериализатора PostSerializer."""

        model = Post
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""

    class Meta:
        """Метакласс для сериализатора GroupSerializer."""

        model = Group
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        """Метакласс для сериализатора CommentSerializer."""

        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
