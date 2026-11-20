from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Abstract base class for order discount strategies (Strategy pattern)."""

    @abstractmethod
    def apply(self, total: float) -> float:
        """Return the discounted total for the given order total."""
        pass


class NoDiscount(DiscountStrategy):
    """Applies no discount and returns the total unchanged."""

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """Applies a percentage discount, e.g. PercentageDiscount(10) takes 10% off."""

    def __init__(self, percentage: float) -> None:
        if percentage < 0 or percentage > 100:
            raise ValueError("Discount percentage must be between 0 and 100.")
        self.__percentage: float = percentage

    @property
    def percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)


class BulkDiscount(DiscountStrategy):
    """Subtracts a fixed amount when the total meets or exceeds a threshold."""

    def __init__(self, threshold: float, amount: float) -> None:
        if threshold <= 0:
            raise ValueError("Bulk discount threshold must be greater than zero.")
        if amount < 0:
            raise ValueError("Bulk discount amount cannot be negative.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    @property
    def threshold(self) -> float:
        return self.__threshold

    @property
    def amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return max(0.0, total - self.__amount)
        return total


class StudentDiscount(DiscountStrategy):
    """Applies a student percentage discount (default 5% off)."""

    def __init__(self, percentage: float = 5.0) -> None:
        if percentage < 0 or percentage > 100:
            raise ValueError("Discount percentage must be between 0 and 100.")
        self.__percentage: float = percentage

    @property
    def percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)
