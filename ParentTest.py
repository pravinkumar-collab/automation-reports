import pytest


@pytest.mark.usefixtures("setup_and_teardown","delete_user_before_test")
class ParentTest:
    pass



