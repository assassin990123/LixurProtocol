"""
Estimated Testnet Beta Release: March 2022 (But progress greatly depends on how fast we can implement a functional peer to peer network, if we can do this in two days,
then 7-14 days after should be the release date hopefully). PS: Update the code on GitHub before you post this to the Discord Server.
----------------------------------------------------------------------------------------------------------------------------------------------------------
*: Focus on recruiting developers.

*: We need to establish a peer to peer connection framework where multiple devices can interact and append to the ledger and network. We will know we have
completed this when I can run the program from multiple devices and they can submit their own transactions and on the /node page, there should be
two or more nodes available and can send any node on the network a message back and forth. After this, find a way to retrieve the SHA512 ID from the code
but if not, then give them your own ID. The IP Addresses MUST be IPv6! (A week maybe, I don't know much about networking).
*: Make the Enchanted Consensus Weighted and then add that logic to the is_valid_transaction() function in graph.py. (A few days hopefully)
*: Once networking is achieved, we need to develop the framework in make_transaction() to have the ability to transfer funds. (Three days maybe)
*: Once that is achieved, have the readable addresses be related to the public address of the wallet. (One to two days at most)
*: Add your JIT Compiler throughout the code, whether this would be RustPython or Numba (About a dozen hours at most, research as biggest time waster)
*: Once that is done, clean up everywhere and simplify the code, look for anything else that needs to
be simplified, modified or otherwise added/removed. Then probably make a nice HTML page for it and you can release the Lixur Testnet Beta Version 1.0.0 (Worst case, a week)

People can spam the network sending transactions to themselves.

[!] This will be a Testnet Beta Version, the LXR will be worth nothing (Will have legit value in the Main-net) and expect chaos, haywire, bugs, malfunctions etc.
(Until Main-net Version/Main-net Beta Version is released, likely somewhere around Late 2022 to Early 2023. The purpose of the Testnet Beta is to test functionality.

Roadmap:
*: Have a Directed Acyclic Graph and functioning consensus (DAG and Enchanted), Quantum resistant cryptographic public and private keys and human-readable addresses.
[!] Almost done with this, a month maximum until this will be completed and Testnet Beta Version 1.0.0 is released.
*: The creation of a unified layer zero interoperable protocol (like Polkadot) of subgraphs (analogous to parachains on Polkadot) that can relay and store arbitrary data
and information from any amount of points in the entire Lixur ecosystem where it can do so.
*: Enable privacy capabilities and zero knowledge proof capabilities for information and data that needs to be stored as private and need quick retrieval.
*: Enable people to add subgraphs, sub-ecosystems, and nodes to the network, by themselves in a secure, trustless, and attack-resistant way.
Subsystems and subgraphs can be added and customized to the ecosystem. These graphs should be upgradeable however you want w/o hard forks.
*: Add smart contract capabilities, intelligent contract capabilities (optional at this point, can be done later) and secret databoxes, as well as token types to
support all kinds of NFTs, cryptocurrencies and others.
*: Release a hyper simple and straightforward UI for people to use to develop applications and contracts.
An A.I programmer can be a helper that can help you, do the work for you and detect loopholes and security flaws automatically.
People can use natural language processing and have it code what it wants for them, making developing applications zero-coding knowledge required.
"""
