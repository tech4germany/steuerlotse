from unittest.mock import MagicMock


class MockIndivSaltHash(MagicMock):
    counter = 0

    def hash(self, value):
        hash_value = value + str(self.counter)
        MockIndivSaltHash.counter = MockIndivSaltHash.counter + 1 if MockIndivSaltHash.counter < 9 else 0
        return hash_value

    def verify(self, value, hashed_value):
        return value == hashed_value[:-1]


class MockGlobalSaltHash(MagicMock):

    def hash(self, value):
        return value + str(0)

    def verify(self, value, hashed_value):
        if value is None:
            raise TypeError('secret must be unicode or bytes, not None')
        return value == hashed_value[:-1]
