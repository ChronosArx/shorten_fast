from rest_framework.response import Response
from rest_framework import status


class CreateSerializerMixin:
    """
    This class use a serializer to create the object and
    returns the data whith the serializer in serializer_class
    """

    create_serializer_class = None

    def get_serializer_class(self):
        if self.action == "create" and self.create_serializer_class is not None:
            return self.create_serializer_class
        if self.action == "get_qrcode" and self.create_serializer_class is not None:
            return self.create_serializer_class
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_serializer = self.serializer_class(serializer.instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
