import pytest
from brownie import accounts, config, exceptions, network, SBTExperimental

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

name = "SBT Test"
symbol = "SBT"

token_uri = "https://charlidao-assets.s3.eu-west-2.amazonaws.com/cdao-treasurer.json"


@pytest.fixture
def accs():
    if (
        network.show_active()
        in LOCAL_BLOCKCHAIN_ENVIRONMENTS + LOCAL_BLOCKCHAIN_ENVIRONMENTS
    ):
        return [accounts[0], accounts[1]]
    return [
        accounts.add(config["wallets"]["account_1"]),
        accounts.add(config["wallets"]["account_2"]),
    ]


@pytest.fixture
def sbt(accs):
    if len(SBTExperimental) > 0:
        contract = SBTExperimental[-1]
    contract = SBTExperimental.deploy(name, symbol, accs[0].address, {"from": accs[0]})
    print(f"Contract address: {contract.address}")
    return contract


@pytest.fixture
def mint(accs, sbt):
    if not sbt.hasSBT(accs[0].address):
        sbt.mint(accs[0].address, token_uri, {"from": accs[0]})
    if not sbt.hasSBT(accs[1].address):
        sbt.mint(accs[1].address, token_uri, {"from": accs[0]})


def test_name_symbol(sbt):
    assert sbt.name() == name
    assert sbt.symbol() == symbol


def test_disallow_empty_uri(sbt, accs):
    error_message = "_tokenURI may not be empty"
    try:
        sbt.mint(accs[0].address, "", {"from": accs[0]})
        assert False
    except exceptions.VirtualMachineError as e:
        assert e.revert_msg == error_message
    except ValueError as e:
        assert error_message in str(e)


def test_user_cannot_mint(sbt, accs):
    error_message = "Only admin can mint new SBTs"
    try:
        sbt.mint(accs[1].address, token_uri, {"from": accs[1]})
        assert False
    except exceptions.VirtualMachineError as e:
        assert e.revert_msg == error_message
    except ValueError as e:
        assert error_message in str(e)


def test_has_sbt_returns_false(accs, sbt):
    assert sbt.hasSBT(accs[0].address) == False


def test_has_sbt_returns_true(sbt, accs, mint):
    assert sbt.hasSBT(accs[0])
    assert sbt.hasSBT(accs[1])


def test_get_sbt(sbt, accs, mint):
    assert sbt.getSBT(accs[0]) == (0, token_uri)


def test_get_token_id(sbt, accs, mint):
    assert sbt.tokenId(accs[0]) == 0


def test_get_token_uri(sbt, accs, mint):
    assert sbt.tokenURI(accs[0]) == token_uri


def test_user_cannot_update(sbt, accs, mint):
    error_message = "Only admin can update soul data"
    try:
        sbt.update(accs[0], f"{token_uri}gibberish", {"from": accs[1]})
        assert False
    except exceptions.VirtualMachineError as e:
        assert e.revert_msg == error_message
    except ValueError as e:
        assert error_message in str(e)


def test_admin_can_update(sbt, accs, mint):
    sbt.update(accs[0], f"{token_uri}gibberish", {"from": accs[0]})
    assert sbt.getSBT(accs[0]) == (0, f"{token_uri}gibberish")


def test_user_cannot_burn(sbt, accs, mint):
    error_message = "Only the admin or the Soul owning the SBT can burn the SBT"
    try:
        sbt.burn(accs[0], {"from": accs[1]})
        assert False
    except exceptions.VirtualMachineError as e:
        assert e.revert_msg == error_message
    except ValueError as e:
        assert error_message in str(e)


def test_owner_can_burn(sbt, accs, mint):
    sbt.burn(accs[1], {"from": accs[1]})
    assert sbt.hasSBT(accs[1]) == False


def test_admin_can_burn(sbt, accs, mint):
    sbt.burn(accs[1], {"from": accs[0]})
    assert sbt.hasSBT(accs[1]) == False
