"""Вьюсеты для моделей приложения Yatube."""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Post с поддержкой CRUD операций."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Сохраняет пост с текущим пользователем как автором."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Обновляет пост, если пользователь является автором."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        serializer.save()

    def perform_destroy(self, instance):
        """Удаляет пост, если пользователь является автором."""
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Group с поддержкой только чтения."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment с поддержкой CRUD операций."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Возвращает кверисет комментариев, связанных с указанным постом."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        """Сохраняет коммент с текущим юзером-автором и указанным постом."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        """Обновляет комментарий, если пользователь является автором."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        serializer.save()

    def perform_destroy(self, instance):
        """Удаляет комментарий, если пользователь является автором."""
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        instance.delete()
