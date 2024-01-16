import pytest
from utils.user.user_type_util import UserType
from users import models

def test_get_user_type():
    with pytest.raises(Exception, match=r'User type \(\w+\) does not exist'):
        UserType.get_user_type('some_user_type')



