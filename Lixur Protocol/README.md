### How to run a Node:

* `run_node.py` is where you run the whole thing. Can be run by using; `python runNode.py <hostip> <port>` (Go to CMD, and enter "netstat -a" for your IPs and Ports. 
* Example command to run a node: python run_node.py 123.4.5.6 78900
* It starts a web server on host:port using Python Flask web framework. 

	* To run multiple nodes on the same computer, you need to change the port number.

* To create a new transaction, send a POST request to the node, providing ip:port and transaction as POST request parameters as follows,
* 
    ` $ curl -v 123.4.5.6 78900/transactions/new -X POST -d "sndr_addr=(insert_here)&rcvr_addr=(insert_here)&value=(insert_here)" `

    * TODO: We don't check if the sender has enough resources in their wallet right now. For that purpose, we might have to search the whole Tangle (local copy of it) and look for transactions involving sender's address, and calculate his balance. This would be validation part


* We can check the balance of a wallet address, from a node. For this, send a POST request with addrees=XYZ parameter like this;

    ` $ curl -v 123.4.5.6 78900/wallet/balance -X POST -d "address=0123"`


* You can list all the addresses of the wallet of a specific Node like this;

    `$ curl -v 123.4.5.6 78900/wallet/addresses -X GET`


* Get the current view of current node's Tangle in JSON format, send the following GET request

    `$ curl 123.4.5.6 78900/dag -X GET`


* To get a PNG image of the current node's Tangle, send the following GET request,

    `$ curl 123.4.5.6 78900/dag/png -X GET --output tangle.png ; eog --fullscreen tangle.png &` or `$ curl 123.4.5.6 78900/dag/png -X GET --output tangle.png
    
    * TODO: add a printed timestamp on the PNG file

* We can register a new neighbour to this node.

    `$ curl -v 123.4.5.6 78900/node/register_neighbours -H "Content-Type: application/json" -X POST -d '{"neighbours":[{"ip":"localhost", "port":"8080"}, {"ip":"192.168.1.2", "port":"1234"}]}'`
    
    * In the above POST request, we send a JSON string, which has an list item "neighbours". This list has (ip, port) pairs for each neighbour we are trying to register. 


### Implementation notes (from original Tango):

* The main objects are the Node, wallet(light node) and the Tangle
* Both nodes and wallets can initiate transactions.
* A node can have more than one wallets.
* A wallet can exist in our outside a fullNode. When inside a node its a wallet and when outside its refered to as a light-node. 


### Additional nodes:

* When a node isues a transaction, it must confirm at least 2 other transactions before its transaction can be added to the tangle.
* To confirm a transaction, the node must check for conflict. If the transaction has conflict then the node must not approve it.
* When a node issues a transaction it must solve a crypto puzzle for this transaction to be considered valid. 
	This is achieved by nding a nonce such that the hash of that nonce concatenated with 	  some data from the approved transaction has a particular form. In the case of the    Bitcoin protocol, the hash must have at least a predened number of leading zeros.  

* A transaction must have a weight property:

* A transaction must have cumulative weight. Cumulative weight  =  weight of transaction + own weights of all transactions that directly or iderectly approves it.

* Tips = Total number of unapproved transactions in the system at any time t

* Any node, at the moment when it issues a transaction, observes not the actual state of the tangle, but the one exactly h time units ago. This means, in particular, that a transaction attached to the tangle at time t only becomes visible to the network at time t+h.

* A tip can be in hidden or revealed state. A transaction attached at time t remains in hidden state until time t+h when it then moves to revealed state.

* Consider large weight attack: This is a threat when large weight is used as a basis for tips selection in the tip selection algorithm.

#### <sup>*</sup> As of (December 2021) Mostly forked from (https://github.com/aliteke/Tango)
