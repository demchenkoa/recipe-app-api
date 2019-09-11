from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Tag, Ingredient, Recipe
from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """create object and associate with authenticated user """
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet,
                 mixins.DestroyModelMixin):

    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """filter tags for authenticated user only"""
        return Tag.objects.filter(user=self.request.user).order_by('-name')

    def perform_destroy(self, instance):
        instance.delete()


class IngredientViewSet(BaseRecipeAttrViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecipeViewSet(viewsets.ModelViewSet):
    """manage recipes in database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
