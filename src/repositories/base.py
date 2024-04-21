import abc


class BaseRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, item):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference):
        raise NotImplementedError


class BaseUnitOfWork(abc.ABC):
    users: BaseRepository
    companies: BaseRepository

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
