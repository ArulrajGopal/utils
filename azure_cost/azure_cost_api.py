import requests
from azure.identity import ClientSecretCredential

# 🔹 Replace with your Azure AD App Registration details
TENANT_ID = "<tenant-id>"
CLIENT_ID = "<client-id>"
CLIENT_SECRET = "<client-secret>"

# 🔹 Subscription
SUBSCRIPTION_ID = "<subscription-id>"

# Authenticate with Azure AD
credential = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
token = credential.get_token("https://management.azure.com/.default").token

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Pick the specific date you want costs for
date = "2025-08-01"

# Build the REST API URL with date filters
url = (
    f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}/providers/Microsoft.Consumption/usageDetails"
    f"?$filter=properties/usageStart ge '{date}' and properties/usageEnd le '{date}'"
    f"&api-version=2019-10-01"
)

# Call the API
resp = requests.get(url, headers=headers)

if resp.status_code == 200:
    data = resp.json()

    print(f"Azure Costs for {date}\n" + "-"*40)
    for item in data.get("value", []):
        props = item["properties"]
        resource = props.get("instanceName") or props.get("resourceId")
        cost = props.get("costInBillingCurrency")
        currency = props.get("billingCurrencyCode")
        print(f"Resource: {resource}, Cost: {cost} {currency}")

    # If there are more pages, use nextLink
    if "nextLink" in data:
        print("\n⚠️ More pages of data available. Use nextLink for pagination.")
else:
    print("Error:", resp.status_code, resp.text)
