@app.route('/transactions/new', methods=['GET', 'POST'])
def new_transaction():
    private_key = cryptography.get_ex_private_key(cryptography)
    public_key = cryptography.get_ex_public_key(cryptography)
    alphanumeric_address = cryptography.get_ex_alphanumeric_address(cryptography)

    if private_key and public_key is not None:
        print("You're about to make a transaction...")
        response = node.graph.make_transaction(
            alphanumeric_address,
            input("Enter the recipient's address: "),
            float(input("Enter the amount of LXR to send: ").replace(",", "")),
            cryptography.sign_tx(public_key, private_key, "Lixur"))
    else:
        return jsonify("[-] Private key or public key is not found "), 400

    node.refresh()
    return jsonify(response), 201

@app.route('/wallet', methods=['GET', 'POST'])
def address_retrieval():
    wallet = Wallet()
    wallet.access_wallet()

    alphanumeric_address = cryptography.get_ex_alphanumeric_address(cryptography)
    readable_address = cryptography.get_ex_readable_address(cryptography)

    if util.get_graph_tx_count() < 4:
        node.graph.make_transaction(
            alphanumeric_address,
            alphanumeric_address,
            69420000,
            cryptography.sign_tx(cryptography.get_public_key(cryptography), cryptography.get_private_key(cryptography), "Lixur"))
        node.refresh()
    elif util.get_graph_tx_count() >= 4:
        pass
    node.refresh()

    response = {
        "alphanumeric_address": alphanumeric_address,
        "readable_address": readable_address,
        "balance": "{:,}".format(util.get_balance(alphanumeric_address)) + " LXR"
    }

    return jsonify(response), 201

# Keystore logistics.