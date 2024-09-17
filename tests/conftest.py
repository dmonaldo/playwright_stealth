import pytest


@pytest.fixture
def page_method_generator():
    # for every way to get a page, test that
    yield