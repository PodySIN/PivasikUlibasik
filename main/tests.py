"""
Модуль для тестов сайта
"""

from django.test import TestCase, Client
from main.models import Users


class BaseTests:
    def setUp(self):
        self.client = Client()

    def logining(self):
        login_info = {
            "username": "TestCaseUser101",
            "password": "TestCasePassword101",
        }
        Users.objects.create_user(**login_info)
        response = self.client.post("/login/", login_info, follow=True)
        self.assertTrue(response.context["user"].is_active)


class IndexPageTestCase(TestCase):
    """
    Тесты для главной страницы
    """

    def setUp(self) -> None:
        self.client = Client()
        self.response = self.client.get("/")

    def test_correct_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_check_title(self) -> None:
        self.assertEqual("ПивасикУлыбасик", self.response.context["Title"])

    def test_check_templates(self) -> None:
        self.assertTemplateUsed(self.response, "pages/index.html")


class ProfilePageTestCase(TestCase, BaseTests):
    """
    Тесты для страницы профиля
    """

    def setUp(self) -> None:
        super().setUp()
        super().logining()
        self.response = self.client.get("/profile/")

    def test_check_correct_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_check_title(self) -> None:
        self.assertEqual("ПивасикУлыбасик", self.response.context["Title"])

    def test_check_templates(self) -> None:
        self.assertTemplateUsed(self.response, "pages/profile.html")


class AboutUsPageTestCase(TestCase):
    """
    Тесты для страницы о нас
    """

    def setUp(self) -> None:
        self.client = Client()
        self.response = self.client.get("/about_us/")

    def test_correct_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_check_title(self) -> None:
        self.assertEqual("ПивасикУлыбасик", self.response.context["Title"])

    def test_check_templates(self) -> None:
        self.assertTemplateUsed(self.response, "pages/about_us.html")


class CatalogPageTestCase(TestCase):
    """
    Тесты для страницы каталога
    """

    def setUp(self) -> None:
        self.client = Client()
        self.response = self.client.get("/catalog/")

    def test_correct_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_check_title(self) -> None:
        self.assertEqual("ПивасикУлыбасик", self.response.context["Title"])

    def test_check_templates(self) -> None:
        self.assertTemplateUsed(self.response, "pages/catalog.html")


class LoginPageTestCase(TestCase):
    """
    Тесты для страницы входа пользователя в систему.
    """

    def setUp(self) -> None:
        self.client = Client()
        self.response = self.client.get("/login/")

    def test_correct_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_check_title(self) -> None:
        self.assertEqual("ПивасикУлыбасик", self.response.context["Title"])

    def test_check_templates(self) -> None:
        self.assertTemplateUsed(self.response, "pages/login.html")


class RegistrationPageTestCase(TestCase):
    """
    Тесты для страницы регистрации.
    """

    def setUp(self) -> None:
        self.client = Client()
        self.response = self.client.get("/registration/")

    def test_correct_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_check_title(self) -> None:
        self.assertEqual("ПивасикУлыбасик", self.response.context["Title"])

    def test_check_templates(self) -> None:
        self.assertTemplateUsed(self.response, "pages/registration.html")


class ParticularBeerPageTestCase(TestCase):
    """
    Тесты для страницы конкретного пива.
    """

    def setUp(self) -> None:
        self.client = Client()
        self.response = self.client.get("/particular_beer/1/")

    def test_correct_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_check_title(self) -> None:
        self.assertEqual("ПивасикУлыбасик", self.response.context["Title"])

    def test_check_templates(self) -> None:
        self.assertTemplateUsed(self.response, "pages/particular_beer.html")


class ParticularShopPageTestCase(TestCase):
    """
    Тесты для страницы конкретного магазина.
    """

    def setUp(self) -> None:
        self.client = Client()
        self.response = self.client.get("/particular_shop/1/")

    def test_correct_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_check_title(self) -> None:
        self.assertEqual("ПивасикУлыбасик", self.response.context["Title"])

    def test_check_templates(self) -> None:
        self.assertTemplateUsed(self.response, "pages/particular_shop.html")


class ParticularVacancyPageTestCase(TestCase):
    """
    Тесты для страницы конкретной вакансии.
    """

    def setUp(self) -> None:
        self.client = Client()
        self.response = self.client.get("/particular_vacancy/1/")

    def test_correct_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_check_title(self) -> None:
        self.assertEqual("ПивасикУлыбасик", self.response.context["Title"])

    def test_check_templates(self) -> None:
        self.assertTemplateUsed(self.response, "pages/particular_vacancy.html")


class PrivacyPolicyPageTestCase(TestCase):
    """
    Тесты для страницы законов и правил.
    """

    def setUp(self) -> None:
        self.client = Client()
        self.response = self.client.get("/privacy_policy/")

    def test_correct_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_check_title(self) -> None:
        self.assertEqual("ПивасикУлыбасик", self.response.context["Title"])

    def test_check_templates(self) -> None:
        self.assertTemplateUsed(self.response, "pages/privacy_policy.html")


class ShopCatalogPageTestCase(TestCase):
    """
    Тесты для страницы каталога магазинов.
    """

    def setUp(self) -> None:
        self.client = Client()
        self.response = self.client.get("/shop_catalog/")

    def test_correct_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_check_title(self) -> None:
        self.assertEqual("ПивасикУлыбасик", self.response.context["Title"])

    def test_check_templates(self) -> None:
        self.assertTemplateUsed(self.response, "pages/shops_catalog.html")


class VacancyPageTestCase(TestCase):
    """
    Тесты для страницы с вакансиями.
    """

    def setUp(self) -> None:
        self.client = Client()
        self.response = self.client.get("/vacancy/")

    def test_correct_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_check_title(self) -> None:
        self.assertEqual("ПивасикУлыбасик", self.response.context["Title"])

    def test_check_templates(self) -> None:
        self.assertTemplateUsed(self.response, "pages/vacancy.html")
