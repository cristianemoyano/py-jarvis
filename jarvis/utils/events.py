import logging
from abc import ABC, abstractmethod
from random import randrange

from logger import setup_logger

logger = logging.getLogger(__name__)
setup_logger(logger)


class Suscriber(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject):
        """
        Receive update from subject.
        """
        pass


class Publisher(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def subscribe(self, sucriber: Suscriber):
        """
        Attach an sucriber to the subject.
        """
        pass

    @abstractmethod
    def unsubscribe(self, sucriber: Suscriber):
        """
        Detach an sucriber from the subject.
        """
        pass

    @abstractmethod
    def notify(self):
        """
        Notify all sucribers about an event.
        """
        pass


class ConcretePublisher(Publisher):
    """
    The Publisher owns some important state and notifies observers when the state
    changes.
    """

    _state: int = None
    """
    For the sake of simplicity, the Publisher's state, essential to all
    subscribers, is stored in this variable.
    """

    _sucribers: list[Suscriber] = []
    """
    List of subscribers. In real life, the list of subscribers can be stored
    more comprehensively (categorized by event type, etc.).
    """

    def subscribe(self, suscriber: Suscriber):
        logger.info(
            f"{self.__class__.__name__}: Attached an suscriber: {suscriber.__class__.__name__}"
        )
        self._sucribers.append(suscriber)

    def unsubscribe(self, suscriber: Suscriber):
        logger.info(
            f"{self.__class__.__name__}: Dettached an suscriber: {suscriber.__class__.__name__}"
        )
        self._sucribers.remove(suscriber)

    """
    The subscription management methods.
    """

    def notify(self):
        """
        Trigger an update in each subscriber.
        """

        logger.info(f"{self.__class__.__name__}: Notifying observers...")
        for suscriber in self._sucribers:
            suscriber.update(self)

    def some_method(self):
        """
        Usually, the subscription logic is only a fraction of what a Subject can
        really do. Subjects commonly hold some important business logic, that
        triggers a notification method whenever something important is about to
        happen (or after it).
        """

        logger.info(f"{self.__class__.__name__}: I'm doing something important.")
        self._state = randrange(0, 10)

        logger.info(
            f"{self.__class__.__name__}: My state has just changed to: {self._state}"
        )
        self.notify()


"""
Concrete Observers react to the updates issued by the Subject they had been
attached to.
"""


class ConcreteSuscriberA(Suscriber):
    def update(self, publisher: Publisher):
        if publisher._state < 3:
            logger.info(f"{self.__class__.__name__}: Reacted to the event")


class ConcreteSuscriberB(Suscriber):
    def update(self, publisher: Publisher):
        if publisher._state == 0 or publisher._state >= 2:
            logger.info(f"{self.__class__.__name__}: Reacted to the event")


if __name__ == "__main__":
    # The client code.

    publisher = ConcretePublisher()

    observer_a = ConcreteSuscriberA()
    publisher.subscribe(observer_a)

    observer_b = ConcreteSuscriberB()
    publisher.subscribe(observer_b)

    publisher.some_method()
    publisher.some_method()

    publisher.unsubscribe(observer_a)

    publisher.some_method()
