from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


# Create your tests here.
class ShortenTests(APITestCase):

    def setUp(self):
        self.register_data = {
            "username": "david",
            "email": "david@david.com",
            "password": "david1331",
        }
        self.short_link_data = {
            "original_url": "https://example.com/example",
        }
        self.short_link_with_title_data = {
            "title": "Titutlo de test",
            "original_url": "https://example.com/example",
        }
        self.short_link_data_incorrect = {"original_url": "no-is-url"}

        reesponse = self.client.post(reverse("register"), data=self.register_data)
        response_data = reesponse.json()
        self.token = response_data.get("access_token")

    def test_short_link(self):
        # sin titulo
        url = reverse("shortlink-list")
        response = self.client.post(url, data=self.short_link_data)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response_data)
        self.assertIn("title", response_data)
        self.assertIsNone(response_data["title"])
        self.assertIn("original_url", response_data)
        self.assertEqual(
            response_data["original_url"], self.short_link_data["original_url"]
        )
        self.assertIn("short_url", response_data)
        self.assertIn("code", response_data)
        self.assertTrue(response_data["code"].isalnum())
        self.assertEqual(len(response_data["code"]), 6)

        # con titulo
        response = self.client.post(url, data=self.short_link_with_title_data)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response_data)
        self.assertIn("title", response_data)
        self.assertEqual(
            response_data["title"], self.short_link_with_title_data["title"]
        )
        self.assertIn("original_url", response_data)
        self.assertEqual(
            response_data["original_url"],
            self.short_link_with_title_data["original_url"],
        )
        self.assertIn("short_url", response_data)
        self.assertIn("code", response_data)
        self.assertTrue(response_data["code"].isalnum())
        self.assertEqual(len(response_data["code"]), 6)

    def test_short_link_incorrect(self):
        url = reverse("shortlink-list")
        response = self.client.post(url, data=self.short_link_data_incorrect)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_links(self):
        url = reverse("shortlink-list")

        # empty links
        response_empty = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response_empty.status_code, status.HTTP_200_OK)
        response_data_empty = response_empty.json()
        self.assertEqual(len(response_data_empty), 0)

        # create the items
        self.client.post(
            url,
            data=self.short_link_with_title_data,
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        self.client.post(
            url,
            data=self.short_link_with_title_data,
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        # more items
        response_items = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response_items.status_code, status.HTTP_200_OK)
        response_items_data = response_items.json()
        self.assertEqual(len(response_items_data), 2)

    def test_get_links_incorrect(self):
        # sin autorización
        url = reverse("shortlink-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_link(self):
        url_post = reverse("shortlink-list")
        # create one item
        response_post = self.client.post(
            url_post,
            data=self.short_link_with_title_data,
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        short_link = response_post.json()
        link_id = short_link.get("id")

        url_get = reverse("shortlink-detail", args=[link_id])

        response = self.client.get(url_get, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response_data)
        self.assertIn("title", response_data)
        self.assertIsNotNone(response_data["title"])
        self.assertIn("original_url", response_data)
        self.assertIn("short_url", response_data)
        self.assertIn("code", response_data)
        self.assertEqual(len(response_data["code"]), 6)

    def test_get_link_incorrect(self):
        url = reverse("shortlink-detail", args=[1])
        # sin autorización
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # no existe elemento
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_link(self):
        url_post = reverse("shortlink-list")
        response = self.client.post(
            url_post,
            data=self.short_link_with_title_data,
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        shortLink = response.json()
        shortLink["title"] = "Nuevo titulo"

        url_update = reverse("shortlink-detail", args=[1])
        response = self.client.put(
            url_update, data=shortLink, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn("id", response_data)
        self.assertIn("title", response_data)
        self.assertIsNotNone(response_data["title"])
        self.assertEqual(response_data["title"], "Nuevo titulo")
        self.assertIn("original_url", response_data)
        self.assertIn("short_url", response_data)
        self.assertIn("code", response_data)
        self.assertEqual(len(response_data["code"]), 6)

    def test_update_link_incorrect(self):
        url_update = reverse("shortlink-detail", args=[1])

        # sin autorización
        response = self.client.put(url_update, data=self.short_link_with_title_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # sin que el link exista
        response = self.client.put(
            url_update,
            data=self.short_link_with_title_data,
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # sin datos y existe
        # creamos el shortlink primero
        url_post = reverse("shortlink-list")
        self.client.post(
            url_post,
            data=self.short_link_with_title_data,
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        response = self.client.put(
            url_update,
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_link(self):
        url_post = reverse("shortlink-list")
        response_post = self.client.post(
            url_post,
            data=self.short_link_with_title_data,
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        response_post_data = response_post.json()
        link_id = response_post_data.get("id")

        url_delate = reverse("shortlink-detail", args=[link_id])
        response_delete = self.client.delete(
            url_delate, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_link_incorrect(self):
        url = reverse("shortlink-detail", args=[1])

        # sin autorización
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # no existe elemento
        response = self.client.delete(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_redirect(self):
        # Creamos un link primero
        url_post = reverse("shortlink-list")
        response_post = self.client.post(
            url_post,
            data=self.short_link_with_title_data,
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        response_post_data = response_post.json()
        code = response_post_data.get("code")
        # Asemos la redireccion
        url = reverse("redirects", args=[code])

        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_redirect_incorrect(self):
        # Creamos un link primero
        url_post = reverse("shortlink-list")
        response_post = self.client.post(
            url_post,
            data=self.short_link_with_title_data,
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        response_post_data = response_post.json()
        code = response_post_data.get("code")

        # Con codigo incorrecto
        url = reverse("redirects", args=["123456"])

        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(code, "123456")

    def test_get_qr(self):
        url = reverse("shortlink-get-qr")

        response = self.client.post(
            url, data=self.short_link_data, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "image/png")

    def test_get_qr_incorrect(self):
        url = reverse("shortlink-get-qr")

        response = self.client.post(
            url,
            data=self.short_link_data_incorrect,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
