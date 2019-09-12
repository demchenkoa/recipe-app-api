from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
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
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(user=self.request.user).order_by('-name').distinct()

    def perform_create(self, serializer):
        """create object and associate with authenticated user """
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet,
                 mixins.DestroyModelMixin):

    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """filter tags for authenticated user only"""

        queryset = Tag.objects.filter(user=self.request.user).order_by('-name')

        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )

        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.distinct()

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

    @staticmethod
    def _params_to_ints(qs_params):
        """convert a list of str ids to list of ints"""
        return [int(param) for param in qs_params.split(',')]

    def get_queryset(self):
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset

        if tags:
            tags = RecipeViewSet._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tags)

        if ingredients:
            ingredients = RecipeViewSet._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredients)

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """return appropriate serializer class"""

        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer

        if self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
