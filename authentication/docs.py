from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse, OpenApiExample


response_access_token = OpenApiResponse(
    response=OpenApiTypes.OBJECT,
    description="Retorna el token de acceso",
    examples=[
        OpenApiExample(
            name="access_token",
            value={
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMDAwMDAwLCJpYXQiOjE2MDAwMDAwMDAsImp0aSI6IjEyMzQ1Njc4OTAiLCJ1c2VyX2lkIjoxfQ.n3IA6Of8g93IMV9G5u5ziN6ZtE6fWUcNu2Z6iHCjFWo",
            },
        )
    ],
)
