from brownie import accounts, config, SBTExperimental


def mint():
    account = accounts.add(config["wallets"]["account_1"])

    if len(SBTExperimental) < 0:
        print("Contract deployment not found.")
        exit(1)

    contract = SBTExperimental[-1]

    address = input("Recipient Address: ")
    token_uri = input("Token URI: ")

    SBTExperimental.mint(address, token_uri, {"from": account})

    print(f"Minted SBT: {contract.getSBT(address)}")


def main():
    mint()
