from django.test import TestCase, TransactionTestCase
from pokemon.models import DummyModel, Pokedex


from integration_tests.helpers import ApplicationStartupTestCase


class TestModel_Dummy(
    ApplicationStartupTestCase
):  # class name should prefix with `Test`
    def test_some_model(_):  # function name should prefix with `test_`

        dummies = DummyModel.objects.all()
        assert len(dummies) == 0


class TestModel_Pokedex(
    ApplicationStartupTestCase
):  # class name should prefix with `Test`
    def setUp(self) -> None:
        pass

    def test_sanity_have_row(_):  # function name should prefix with `test_`
        entries = Pokedex.objects.all()
        assert len(entries) > 0
