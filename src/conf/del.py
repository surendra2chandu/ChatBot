import subprocess
import json


def get_logged_in_azure_user():
    try:
        # Run Azure CLI command (pass full command as a string for shell=True on Windows)
        command = "az account get-access-token --query user --output json"
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True
        )

        if result.returncode != 0:
            raise Exception(f"Error: {result.stderr}")

        user_info = json.loads(result.stdout)
        return user_info

    except Exception as e:
        print(f"Failed to get logged-in Azure user: {e}")
        return None

# Example usage
user = get_logged_in_azure_user()

if user:
    print(f"Logged in Azure user: {user['name']} (type: {user['type']})")
else:
    print("No user is currently logged in to Azure CLI. Please run 'az login' and try again.")
