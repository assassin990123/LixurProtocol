'''
Current TODO:
1. Implement the weights to make the Enchanted Consensus

# We need to establish a multi-node environment
# Once we have this, we can start to refine the transfer process

TODO: We don't check if the sender has enough resources in their wallet right now. For that purpose, we might have to
search the whole Tangle (local copy of it) and look for transactions involving sender's address, and calculate their
balance. This would be validation part.
# Then we can also validate authenticity on the ledger as well for these transactions

TODO:
1. Figure out how to update the cumulative
2. How to only allow the first node to get the 69420000 LXR and nobody else (something you need to do before release) in
a multi-node setting.

Also, make sure the finality time is how long it took to make the transaction so it should be calculated within the
make transaction function. This needs to be solved.

Also hide or hash IP and Port identities, maybe with schemes for privacy.
Also, ensure that it works as a distributed network, where everyone is updated on the network of the current state

Balances are maintained on the graph, not a list... When a wallet is created, a transaction to itself identifying it's
starting balance is needed. Also, before testnet launch, ensure that you maximize the entire program for as much performance as possible, from using
Numba JIT compilation, RustPython to using multithreading and processing, and using NumPy and even using PyPy maybe

------------------------------------------------------------------------------------------------------------------------

In very simple terms, a consensus mechanism is...

An algorithm that can be used to ensure that while nodes are voting on the contents of the ledger that the honest ones
agree on the same thing and always win.

Consensus is only used when there is a conflict, or you could run it everytime a transaction is posted so you don't have to write code to identify
a byzantine. Previously any conflicts were resolved when selecting tips (the random walk in the original whitepaper).

What is a conflicting transaction in IOTA?***

Use ZK-sNARKS to retrieve the graph faster so nodes can operate as quickly as possible

We will have to resolve this later to check if they are conflicting.

Tips validate pending transactions with the consensus mechanism, after it validates it, it goes to get validated.

Dynamic Spam Protection, difficulty adjusts with network activity. Should not be limiting to the point it
hampers performance, should be able to be done on any device.

Suppose a node receives two transactions that spend all of the IOTA in an address.
Both transactions are perfectly legal by themselves.
Thus, the node has a dilemma: which transaction should it put in its database?
It can't allow both, since that would spend the same IOTA twice (called a "double spend").
------------------------------------------------------------------------------------------------------------------------
'''