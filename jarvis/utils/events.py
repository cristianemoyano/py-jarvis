import logging
from abc import ABC, abstractmethod
from collections.abc import Iterable

from logger import setup_logger

logger = logging.getLogger(__name__)
setup_logger(logger)


class Suscriber(ABC):
    """
    The Suscriber interface declares the on_action method, used by suscribers.
    """

    @abstractmethod
    def on_action(self, publisher, **kwargs):
        """
        Receive action from Publisher.
        """
        pass


class PublisherInterface(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def subscribe(self, sucriber: Suscriber):
        """
        Attach an sucriber to the publisher.
        """
        pass

    @abstractmethod
    def unsubscribe(self, sucriber: Suscriber):
        """
        Detach an sucriber from the publisher.
        """
        pass

    @abstractmethod
    def publish(self, **kwargs):
        """
        Notify all sucribers about an event.
        """
        pass


class Publisher(PublisherInterface):
    """
    The Publisher notifies suscribers when the publish is called
    """

    def __init__(self, event_code):
        self.event_code = event_code
        super().__init__()

    _sucribers: set[Suscriber] = set()

    def subscribe(self, suscriber: Suscriber):
        logger.info(f"{self.__class__.__name__}: Attached suscribers: {suscriber}")
        self._sucribers |= (
            set(suscriber) if isinstance(suscriber, Iterable) else {suscriber}
        )

    def unsubscribe(self, suscriber: Suscriber):
        logger.info(
            f"{self.__class__.__name__}: Dettached an suscriber: {suscriber.__class__.__name__}"
        )
        self._sucribers.remove(suscriber)

    def publish(self, **kwargs):
        """
        Trigger an event in each subscriber.
        """

        logger.info(f"{self.__class__.__name__}: Notifying observers...")
        for suscriber in self._sucribers:
            suscriber.on_action(self, **kwargs)


PIZZA_DONE_EVENT_CODE = "PIZZA_DONE"
pizza_done_event = Publisher(event_code=PIZZA_DONE_EVENT_CODE)

PIZZA_PAID_EVENT_CODE = "PIZZA_PAID"
pizza_paid_event = Publisher(event_code=PIZZA_PAID_EVENT_CODE)


class PizzaStore:
    def pay_pizza(self, client, amount, order):
        """
        Send pizza
        """
        logger.info(f"{self.__class__.__name__}: Pizza paid")
        pizza_paid_event.publish(
            sender=self.__class__, client=client, amount=amount, order=order
        )

    def send_pizza(self, toppings, size):
        """
        Send pizza
        """
        logger.info(f"{self.__class__.__name__}: Pizza sent")
        pizza_done_event.publish(sender=self.__class__, toppings=toppings, size=size)


"""
Concrete Suscribers react to the updates issued by the Publisher they had been
suscribed to.
"""


class EmailSuscriber(Suscriber):
    def on_action(self, publisher, **kwargs):
        if publisher.event_code == PIZZA_DONE_EVENT_CODE:
            logger.info(f"{self.__class__.__name__}: Sending email: {kwargs}")


class SMSSuscriber(Suscriber):
    def on_action(self, publisher, **kwargs):
        if publisher.event_code == PIZZA_DONE_EVENT_CODE:
            logger.info(f"{self.__class__.__name__}: Sending sms {kwargs}")


class PaymentSuscriber(Suscriber):
    def on_action(self, publisher, **kwargs):
        if publisher.event_code == PIZZA_PAID_EVENT_CODE:
            logger.info(f"{self.__class__.__name__}: Sending payment {kwargs}")


if __name__ == "__main__":
    # The client code.

    email_suscriber = EmailSuscriber()
    sms_suscriber = SMSSuscriber()
    payment_suscriber = PaymentSuscriber()
    pizza_done_event.subscribe({email_suscriber, sms_suscriber})
    pizza_paid_event.subscribe(payment_suscriber)

    pizza_store = PizzaStore()
    pizza_store.pay_pizza(client="John Doe", amount=185.03, order="3 Pizzas")

    pizza_store.send_pizza(**{"toppings": ["tomato"], "size": 8})

    pizza_store.send_pizza(**{"toppings": ["tomato"], "size": 8})
    pizza_store.send_pizza(**{"toppings": ["tomato"], "size": 12})

    pizza_done_event.unsubscribe(sms_suscriber)

    pizza_store.send_pizza(**{"toppings": ["tomato"], "size": 3})
