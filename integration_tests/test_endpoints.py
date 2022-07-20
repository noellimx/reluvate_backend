from django.test import TransactionTestCase
from pokemon.models import DummyModel


from django.urls import reverse


class TestEndpoints(TransactionTestCase):  # class name should prefix with `Test`
    def test_some_route(_):  # function name should prefix with `test_`

        dummies = DummyModel.objects.all()
        assert len(dummies) == 0
