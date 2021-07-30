// SPDX-License-Identifier: MIT

pragma solidity 0.8.6;

interface INFTLock {

    function lockToken(uint256 internalTokenId) external;
    function unlockToken( uint256 internalTokenId) external;
    function withdraw(uint256 internalTokenId) external;
}
