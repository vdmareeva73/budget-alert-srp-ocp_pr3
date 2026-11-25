from abc import ABC, abstractmethod


class BudgetItem:
    def __init__(self, name, cfo, plan, forecast, probability):
        self.name = name
        self.cfo = cfo
        self.plan = plan
        self.forecast = forecast
        self.probability = probability

    @property
    def excess_percent(self):
        if self.plan == 0:
            return 0.0
        return ((self.forecast - self.plan) / self.plan) * 100

    @property
    def needs_alert(self):
        return self.probability > 50


class BudgetDataProvider:
    def get_items(self):
        return [
            BudgetItem("Маркетинг", "Продажи", 1_200_000, 1_420_000, 73),
            BudgetItem("Аренда офиса", "Дирекция", 500_000, 480_000, 18),
            BudgetItem("ФОТ", "HR", 2_000_000, 2_150_000, 61),
            BudgetItem("IT-услуги", "IT", 300_000, 295_000, 32),
        ]


class AlertStrategy(ABC):
    @abstractmethod
    def create_message(self, item):
        pass


class OverrunAlertStrategy(AlertStrategy):
    def create_message(self, item):
        if not item.needs_alert:
            return None
        reason = "в последние месяцы расход выше среднего"
        return (
            f"Статья «{item.name}», ЦФО «{item.cfo}»: при текущем темпе расход за год "
            f"составит {item.forecast / 1_000_000:.2f} млн руб. при лимите "
            f"{item.plan / 1_000_000:.1f} млн (+{item.excess_percent:.0f}%). "
            f"Вероятность перерасхода: {item.probability}%. "
            f"Причина: {reason}."
        )


class NoRiskStrategy(AlertStrategy):
    def create_message(self, item):
        if item.needs_alert:
            return None
        return (
            f"Статья «{item.name}», ЦФО «{item.cfo}»: риска перерасхода нет "
            f"(вероятность {item.probability}%)."
        )


class AlertService:
    def __init__(self, strategies):
        self.strategies = strategies

    def process(self, items):
        messages = []
        for item in items:
            for strategy in self.strategies:
                message = strategy.create_message(item)
                if message:
                    messages.append(message)
                    break
        return messages


class BudgetAlertApp:
    def __init__(self, data_provider, alert_service):
        self.data_provider = data_provider
        self.alert_service = alert_service

    def run(self):
        print("=== Проверка риска перерасхода ===\n")
        items = self.data_provider.get_items()
        messages = self.alert_service.process(items)
        for msg in messages:
            print(msg)
        print("\nПроверка завершена.")


if __name__ == "__main__":
    provider = BudgetDataProvider()
    strategies = [OverrunAlertStrategy(), NoRiskStrategy()]
    service = AlertService(strategies)
    app = BudgetAlertApp(provider, service)
    app.run()
