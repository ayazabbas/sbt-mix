# SBT Mix

## About

Paper by E. Glen Weyl, Puja Ohlhaver, Vitalik Buterin: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4105763

A "soul" is an account that holds "publicly visible, non-transferable (but possibly revocable-by-the-issuer) tokens". Soulbound Tokens (SBTs) are the tokens held by the soul.

There is nothing new here but there is currently no ERC standard that implements this concept. This repo showcases my attempt to implement SBTs.

## Usage

Before using, setup a .env file with `PRIVATE_KEY_1` and `WEB3_INFURA_PROJECT_ID`

Deployment
```
brownie run --network goerli scripts/deploy.py
```

Mint SBT
```
brownie run --network goerli scripts/mint.py
```

Show Data
```
brownie run --network goerli scripts/get_data.py
```

## ToDo

- Currently there is no way to view these SBTs. If we can get OpenSea to show them as an NFT collection that would be cool. Need to figure out what OpenSea looks for when indexing NFTs.
- Currently, we check for non-empty _tokenURI to determine whether a token exists. We shouldn't have to require a token URI so replace this with something better.


## Footnote

Check me out on [@AyazAbbas_](https://twitter.com/AyazAbbas_) | [LinkedIn Ayaz Abbas](https://www.linkedin.com/in/ayaz-abbas/)

Got a Web3 idea but don't know if it's viable or how to build it? CharlieDAO can help validate your idea and help you get it built, check us out: on [@charliedao_eth](https://twitter.com/charliedao_eth) | [CharlieDAO Discord](https://discord.gg/zyRCeJnF69)
