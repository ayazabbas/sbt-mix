from brownie import accounts, config, SBTExperimental


def get_sbt():
    account = accounts.add(config["wallets"]["account_1"])
    contract = SBTExperimental[-1]

    soul = input("Soul address: ")
    if contract.hasSBT(soul):
        print(f"SBT: {contract.getSBT(soul)}")
    else:
        print("Soul does not have this SBT.")


def main():
    get_sbt()
