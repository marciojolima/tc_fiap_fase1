def test_create_dummies_users(fake_users_in_db):
    # Arrange
    fake_users = fake_users_in_db(3)
    print(fake_users)
    # Act
    # Assert
    breakpoint(fake_users)
    assert True == True  # noqa
