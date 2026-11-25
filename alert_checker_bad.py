class BudgetAlertApp:
    def run(self):
        print("=== Проверка риска перерасхода ===\n")

        items = [
            {"name": "Маркетинг", "cfo": "Продажи", "plan": 1_200_000, "forecast": 1_420_000, "probability": 73},
            {"name": "Аренда офиса", "cfo": "Дирекция", "plan": 500_000, "forecast": 480_000, "probability": 18},
            {"name": "ФОТ", "cfo": "HR", "plan": 2_000_000, "forecast": 2_150_000, "probability": 61},
            {"name": "IT-услуги", "cfo": "IT", "plan": 300_000, "forecast": 295_000, "probability": 32},
        ]

        for item in items:
            name = item["name"]
            cfo = item["cfo"]
            plan = item["plan"]
            forecast = item["forecast"]
            probability = item["probability"]

            if probability > 50:
                excess = forecast - plan
                percent = (excess / plan) * 100
                reason = "в последние месяцы расход выше среднего"
                message = (
                    f"Статья «{name}», ЦФО «{cfo}»: при текущем темпе расход за год "
                    f"составит {forecast / 1_000_000:.2f} млн руб. при лимите "
                    f"{plan / 1_000_000:.1f} млн (+{percent:.0f}%). "
                    f"Вероятность перерасхода: {probability}%. "
                    f"Причина: {reason}."
                )
                print(message)
            else:
                print(
                    f"Статья «{name}», ЦФО «{cfo}»: риска перерасхода нет "
                    f"(вероятность {probability}%)."
                )

        print("\nПроверка завершена.")


if __name__ == "__main__":
    app = BudgetAlertApp()
    app.run()
