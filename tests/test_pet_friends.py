from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


# 1
def test_get_api_key_invalid_user(email=invalid_email, password=valid_password):
    """Попытка получить api_key для несуществующего пользователя приводящая к ошибке"""
    status, result = pf.get_api_key(email, password)
    assert status != 200


# 2
def test_get_api_key_invalid_password(email=valid_email, password=invalid_password):
    """Попытка получить api_key для существующего пользователя c несуществующим паролем приводящая к ошибке"""
    status, result = pf.get_api_key(email, password)
    assert status != 200


# 3
def test_get_api_key_invalid_user_and_password(email=invalid_email, password=invalid_password):
    """Попытка получить api_key для несуществующего пользователя и пароля приводящая к ошибке"""
    status, result = pf.get_api_key(email, password)
    assert status != 200


# 4
def test_get_all_pets_with_invalid_key(filter=''):
    """Попытка получить список питомцев при неправильном api_key приводящая к ошибке"""
    headers = {'key': 'fjfjjfjf11100kkk8etrtr'}
    status, _ = pf.get_list_of_pets(headers, filter='')
    assert status != 200


# 5
def test_add_new_pet_simple_valid_data(name='Вася', animal_type='Кошак', age=2):
    """Добавление нового питомца по-простому(без фото)"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


# 6
def test_add_photo_pet(pet_photo='images/dog111.jpg'):
    """Добавление или изменение фото существующего питомца"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert "pet_photo" in result
    else:
        raise Exception("There is no my Pets")


# 7
def test_get_my_pets_with_valid_key(filter='my_pets'):
    """Получаем список своих питомцев"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    if len(result['pets']) == 0:
        raise Exception("There is no my pets")


# 8
def test_add_new_pet_simple_invalid_data(name='Вася', animal_type='Кошак', age=2):
    """Добавление нового питомца по-простому(без фото) с неправильным ключом"""

    headers = {'key': 'fjfjjfjf11100kkk8etrtr'}
    status, _ = pf.add_new_pet_simple(headers, name, animal_type, age)
    assert status != 200


# 9
def test_put_three_new_and_delete_correctly_one_of_three():
    """Тестирование взаимодействия функций добавления, получения списка питомцев и удаления одного из них"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pf.add_new_pet_simple(auth_key, name='Буся', animal_type='Сиамский', age=3)
    pf.add_new_pet_simple(auth_key, name='Барон', animal_type='Мейкун', age=7)
    pf.add_new_pet_simple(auth_key, name='Мурзик', animal_type='Брума', age=2)
    _, result = pf.get_list_of_pets(auth_key, filter='my_pets')
    pet_id = result['pets'][2]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


# 10
def test_add_two_animals_and_change_info_and_photo(pet_photo='images/Енот.jpg'):
    """Тестирование функций добавления, изменения информации и фото"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pf.add_new_pet_simple(auth_key, name='Рик', animal_type='Собака', age=10)
    pf.add_new_pet_simple(auth_key, name='Морти', animal_type='Кот', age=2)
    pf.add_new_pet_simple(auth_key, name='Саммер', animal_type='Попугай', age=1)
    _, result = pf.get_list_of_pets(auth_key, filter='my_pets')
    pet_id = result['pets'][2]['id']
    pf.update_pet_info(auth_key, pet_id, name='Джерри', animal_type='Енот', age=5)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    if len(result['pets']) > 0:
        status, result = pf.update_pet_photo(auth_key, pet_id, pet_photo)
        assert status == 200
        assert "pet_photo" in result
    else:
        raise Exception("There is no my Pets")


# из модуля
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Получаем api_key для пользователя"""

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


# из модуля
def test_get_all_pets_with_valid_key(filter=''):
    """Получаем список питомцев"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


# из модуля
def test_add_new_pet_with_valid_data(name='Рик', animal_type='Корги',
                                     age='5', pet_photo='images/Korgi.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


# из модуля
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/Korgi.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


# из модуля
def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")
