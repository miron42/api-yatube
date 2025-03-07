"""Вьюсеты для моделей приложения Yatube."""
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
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

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

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

    def update(self, request, *args, **kwargs):
        """Обработка запроса на обновление комментария."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Обработка запроса на удаление комментария."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        """Получает объект комментария, проверяя существование поста."""
        comment_id = self.kwargs.get('pk')
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id, post=post)
        return comment

    def list(self, request, *args, **kwargs):
        """Обработка GET-запроса для получения всех комментариев к посту."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        comments = Comment.objects.filter(post=post)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)
