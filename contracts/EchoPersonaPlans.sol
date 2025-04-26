// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract EchoPersonaPlans {
    address public owner;

    enum Plan {
        Basic,
        Premium,
        Pro
    }

    struct Subscription {
        address user;
        Plan plan;
        uint256 timestamp;
        uint256 amountPaid;
        uint256 expiry;
    }

    mapping(address => Subscription) public subscriptions;

    event Subscribed(address indexed user, Plan plan, uint256 amount);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not contract owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function subscribe(Plan plan) public payable {
        uint256 cost = getPlanPrice(plan);
        require(msg.value == cost, "Incorrect payment");

        uint256 duration = 30 days;

        subscriptions[msg.sender] = Subscription({
            user: msg.sender,
            plan: plan,
            timestamp: block.timestamp,
            amountPaid: msg.value,
            expiry: block.timestamp + duration
        });

        emit Subscribed(msg.sender, plan, msg.value);
    }

    function getSubscription(
        address user
    ) public view returns (Subscription memory) {
        return subscriptions[user];
    }

    function getPlanPrice(Plan plan) public pure returns (uint256) {
        if (plan == Plan.Basic) return 0 ether;
        if (plan == Plan.Premium) return 0.003 ether;
        if (plan == Plan.Pro) return 0.005 ether;
        revert("Invalid plan");
    }

    function withdraw() external onlyOwner {
        payable(owner).transfer(address(this).balance);
    }

    function isSubscriptionActive(address user) public view returns (bool) {
        return subscriptions[user].expiry > block.timestamp;
    }
}
