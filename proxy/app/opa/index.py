from opa_client.opa import OpaClient


class OPAService:
    def __init__(self, host="localhost", port=8181):
        self.client = OpaClient(host=host, port=port)
        if not self.check_connection():
            raise ConnectionError("Failed to connect to OPA server")
        else:
            print("Connected to OPA server")

    def check_connection(self):
        try:
            return self.client.check_connection()  # True
        finally:
            self.client.close_connection()

    def update_policy_from_file(self, filepath, endpoint):
        self.client.update_policy_from_file(filepath=filepath, endpoint=endpoint)

    def is_allowed(self, input_data, package_path, rule_name="allow"):
        result = self.client.query_rule(
            input_data=input_data, package_path=package_path, rule_name=rule_name
        )
        return result.get("result", False)


opa_client = OPAService(host="localhost", port=8181)
