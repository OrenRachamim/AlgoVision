import warnings

import pytest

warnings.filterwarnings("ignore")


@pytest.fixture(scope="session")
def synthetic():
    from algovision.data.synthetic import GENERATORS
    return GENERATORS
