// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract SBTExperimental {
    struct SBT {
        uint256 tokenId;
        string tokenURI;
    }

    uint256 public tokenCounter;

    string public name;
    string public symbol;
    address public admin;

    mapping(address => SBT) private SBTs;

    // keccak-256 of empty-string used in check for token existence
    bytes32 empty =
        0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470;

    event Transfer(
        address indexed from,
        address indexed to,
        uint256 indexed tokenId
    );
    event Mint(uint256 _tokenId, address _soul);
    event Burn(uint256 _tokenId, address _soul);
    event Update(uint256 _tokenId, address _soul);

    constructor(
        string memory _name,
        string memory _symbol,
        address _admin
    ) {
        name = _name;
        symbol = _symbol;
        admin = _admin;
        tokenCounter = 0;
    }

    function mint(address _soul, string memory _tokenURI) external {
        require(
            keccak256(bytes(_tokenURI)) != empty,
            "_tokenURI may not be empty"
        );
        require(
            keccak256(bytes(SBTs[_soul].tokenURI)) == empty,
            "Soul already has this SBT"
        );
        require(msg.sender == admin, "Only admin can mint new SBTs");
        SBTs[_soul] = SBT(tokenCounter, _tokenURI);
        emit Mint(tokenCounter, _soul);
        emit Transfer(address(0), _soul, tokenCounter);
        tokenCounter = tokenCounter + 1;
    }

    function burn(address _soul) external {
        require(
            msg.sender == _soul || msg.sender == admin,
            "Only the admin or the Soul owning the SBT can burn the SBT"
        );
        uint256 _tokenId = SBTs[_soul].tokenId;
        delete SBTs[_soul];
        emit Burn(_tokenId, _soul);
    }

    function update(address _soul, string memory _tokenURI) external {
        require(msg.sender == admin, "Only admin can update soul data");
        uint256 _tokenId = SBTs[_soul].tokenId;
        SBTs[_soul] = SBT(_tokenId, _tokenURI);
        emit Update(_tokenId, _soul);
    }

    function hasSBT(address _soul) external view returns (bool) {
        if (keccak256(bytes(SBTs[_soul].tokenURI)) == empty) {
            return false;
        } else {
            return true;
        }
    }

    function getSBT(address _soul) external view returns (SBT memory) {
        return SBTs[_soul];
    }

    function tokenId(address _soul) external view returns (uint256) {
        return SBTs[_soul].tokenId;
    }

    function tokenURI(address _soul) external view returns (string memory) {
        return SBTs[_soul].tokenURI;
    }
}
