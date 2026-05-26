from locust import task, events
from locust.env import Environment

from clients.http.gateway.locust import GatewayHTTPTaskSet
from seeds.scenarios.existing_user_issue_virtual_card import ExistingUserIssueVirtualCardSeedsScenario
from seeds.schema.result import SeedUserResult
from tools.user import LocustBaseUser


@events.init.add_listener
def init(environment: Environment, **kwargs):
    seeds_scenario = ExistingUserIssueVirtualCardSeedsScenario()

    seeds_scenario.build()
    environment.seeds = seeds_scenario.load()

class IssueVirtualCardTaskSet(GatewayHTTPTaskSet):
    seed_user: SeedUserResult

    # Метод вызывается при запуске каждой сессии пользователя (до начала задач)
    def on_start(self) -> None:
        super().on_start()

        # Получаем следующего пользователя из списка (по порядку!)
        self.seed_user = self.user.environment.seeds.get_random_user()

    @task(3)
    def get_accounts(self):
        self.accounts_gateway_client.get_accounts(user_id=self.seed_user.user_id)

    @task(1)
    def issue_virtual_card(self):
        self.cards_gateway_client.issue_virtual_card(user_id=self.seed_user.user_id, account_id=self.seed_user.debit_card_accounts[0].account_id)


class IssueVirtualCardScenarioUser(LocustBaseUser):
    tasks = [IssueVirtualCardTaskSet]