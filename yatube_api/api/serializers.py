"""Сериализаторы для моделей приложения Yatube."""

from rest_framework import serializers

from posts.models import Post, Group, Comment


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        """Метакласс для сериализатора PostSerializer."""

        model = Post
        fields = ('id', 'author', 'text', 'pub_date', 'group', 'image')


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""

    class Meta:
        """Метакласс для сериализатора GroupSerializer."""

        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """Метакласс для сериализатора CommentSerializer."""
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
