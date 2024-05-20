import pytest
from helpers.grpc import client
from grpc._channel import _InactiveRpcError


def test_create_user():
    res = client.create_user(
        name='Bruce',
        age=33
    )
    assert res.id != 0


def test_get_user():
    name = 'Alex'
    age = 30
    res_create = client.create_user(
        name=name,
        age=age
    )

    user = client.get_user(res_create.id)
    assert user.id == res_create.id
    assert user.name == name
    assert user.age == age


def test_get_user_negative():
    with pytest.raises(_InactiveRpcError) as e:
        client.get_user(-1)


def test_update_user():
    name = 'Peter'
    age = 22
    res_create = client.create_user(
        name=name,
        age=age
    )

    new_name = 'Peter_new'
    new_age = 23
    user = client.update_user(res_create.id, name=new_name, age=new_age)
    assert user.id == res_create.id
    assert user.name == new_name
    assert user.age == new_age


def test_update_user_negative():
    with pytest.raises(_InactiveRpcError) as e:
        client.update_user(-1, 'Negative', 22)


def test_delete_user():
    name = 'Rachel'
    age = 27
    res_create = client.create_user(
        name=name,
        age=age
    )

    user = client.delete_user(res_create.id)
    assert user.id == res_create.id


def test_delete_user_negative():
    with pytest.raises(_InactiveRpcError) as e:
        client.delete_user(-1)
