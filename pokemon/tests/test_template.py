from django.test import SimpleTestCase


class TestSome(SimpleTestCase):  # class name should prefix with `Test`
    def test_Nothing(_):  # function name should prefix with `test_`
        assert True
