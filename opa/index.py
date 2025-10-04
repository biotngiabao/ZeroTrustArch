from opa_client.opa import OpaClient

client = OpaClient(host="localhost", port=8181)
try:
    print(client.check_connection())  # True
finally:
    client.close_connection()


policy_name = "api_policy"

client.update_policy_from_file(
    filepath="/Users/baothainguyengia/Desktop/Cryptography & Network Security/code /opa/policies/api.rego",
    endpoint=policy_name,
)


def is_allowed(input_data, package_path, rule_name="allow"):
    result = client.query_rule(
        input_data=input_data, package_path=package_path, rule_name=rule_name
    )
    return result.get("result", False)


print(
    is_allowed(
        input_data={
            "method": "GET",
            "path": ["finance.php"],
            "token": {"roles": ["billing.viewer"]},
        },
        package_path="authz",
    )
)  # True
