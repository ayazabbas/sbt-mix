from brownie import accounts, config, SBTExperimental


def deploy():
    account = accounts.add(config["wallets"]["account_1"])
    if len(SBTExperimental) > 0:
        answer = input(
            f"Contract is already deployed at {SBTExperimental[-1].address} - do you want to deploy a new one anyway? [y/n]"
        ).lower()
        if answer not in ["y", "yes"]:
            print("Deployment cancelled by user.")
            exit(1)
    name = input("SBT Name: ")
    symbol = input("SBT Symbol: ")
    admin = input("Admin Address (leave blank to use contract owner): ")
    if admin.trim() == "":
        admin = account.address

    contract = SBTExperimental.deploy(name, symbol, admin, {"from": account})
    print(f"Contract deployed at {contract.address}")


def main():
    deploy()
