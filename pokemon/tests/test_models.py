from django.test import TransactionTestCase
from pokemon.models import DummyModel


class TestModels(TransactionTestCase):  # class name should prefix with `Test`
    def test_some_model(_):  # function name should prefix with `test_`

        dummies = DummyModel.objects.all()
        assert len(dummies) == 0
