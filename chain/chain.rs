pub use rand::Rng;
pub use chrono::Utc;
pub use std::fs::File;
pub use std::io::Write;

mod utilities;
use crate::utilities::{Transaction, Chain};

// Generates and returns a new, empty chain (directed acyclic graph).
fn generate_chain() -> Vec<(&'static str, Transaction)> {
    return Chain::new();
}

// Returns the length of the chain.
fn count_chain_length (chain: &Vec<(&'static str, Transaction)> ) -> usize {
    return chain.len();
}

// Generates an index for a transaction.
fn generate_index(chain: &Vec<(&'static str, Transaction)> ) -> usize {
    return count_chain_length(chain) + 1;
}

// Retrieves a certain transaction based on it's ID.
fn fetch_transaction(chain: Vec<(&'static str, Transaction)>, tx_id: &'static str) -> Option<Transaction> {
    return chain.iter().find(|i| i.0 == tx_id).and_then(|i| Some(i.1.clone()))
}

// Returns the number of times an address has made a transaction on the chain.
fn get_appearances (chain: Vec<(&'static str, Transaction)>, tx_id: &'static str) -> usize {
    return chain.iter().filter(|i| i.0 == tx_id).count();
}

// Checks the balance of a user.
fn check_balance (chain: &Vec<(&'static str, Transaction)>, address: &str) -> f64 {
    let mut balance = 0.0;
    for transaction in chain.iter() {
        if transaction.1.sender_address == address && transaction.1.receiver_address == address {
            balance += transaction.1.amount;
        }
        if transaction.1.sender_address == address {
            balance -= transaction.1.amount;
        } else if transaction.1.receiver_address == address {
            balance += transaction.1.amount;
        }
    }
    return balance;
}

// Checks if a transaction is valid.
fn is_valid_transaction (graph: &Vec<(&'static str, Transaction)> , transaction: Transaction) -> bool {
    if transaction.amount == 0.0 {
        println!("You can't send 0 LXR");
        return false;}

    if check_balance(&graph, transaction.sender_address) < transaction.amount {
        return false;}

    if transaction.amount < 0.0 {
        println!("You can't send negative quantities of LXR");
        return false;}

    if transaction.sender_address == transaction.receiver_address {
        println!("You can't send LXR to yourself");
        return false;}

    if transaction.signature.len() != 64 {
        println!("Invalid signature");
        return false;}
    
    if does_address_exist(&graph, transaction.receiver_address) == false {
        println!("Receiver address does not exist");
        return false;}
    
    if does_address_exist(&graph, transaction.sender_address) == false {
        println!("You don't even exist on the network, how did you even get this far?");
        return false;}

    else {return true;}
}

// Checks if a transaction is valid, if so, it adds it to the chain.
fn validate_and_append_transaction (mut chain: Vec<(&'static str, Transaction)>, transaction: Transaction) {
    if transaction.amount == 0.0 {
        println!("You can't send 0 LXR");}

    if check_balance(&chain, transaction.sender_address) < transaction.amount {
        println!("You don't have enough LXR to send that amount");}

    if transaction.amount < 0.0 {
        println!("You can't send negative quantities of LXR");}

    if transaction.sender_address == transaction.receiver_address {
        println!("You can't send LXR to yourself");}

    if transaction.signature.len() != 64 {
        println!("Invalid signature");}
    
    if does_address_exist(&chain, transaction.receiver_address) == false {
        println!("Receiver address does not exist");}
    
    if does_address_exist(&chain, transaction.sender_address) == false {
        println!("You don't even exist on the network, how did you even get this far?");}

    else { // If it is valid, the transaction gets added to the chain.
        chain.push((transaction.signature, transaction));
    }
}

// Checks if an address exists on the chain
fn does_address_exist (chain: &Vec<(&'static str, Transaction)>, address: &str) -> bool {
    let mut exists = false;
    for tx in chain.iter() {
        if tx.1.sender_address == address || tx.1.receiver_address == address {
            exists = true;}
        }
    return exists;
}

// Generates random indexes from 0 to the length of the graph. 
fn generate_random_indexes (chain: &Vec<(&'static str, Transaction)>) -> (usize, usize) {
    let mut rng = rand::thread_rng();
    let index_one = rng.gen_range(0..count_chain_length(chain));
    let mut index_two = rng.gen_range(0..count_chain_length(chain));
    while index_one == index_two {
        index_two = rng.gen_range(0..count_chain_length(chain));
    }
    return (index_one, index_two);
}

// Selects and confirms transactions.
fn select_edges_and_confirm_transactions <'a> (chain: &Vec<(&'static str, Transaction)>)
    -> ((&'a str, Transaction), (&'a str, Transaction), u128) {
    let (index_one, index_two) = generate_random_indexes(&chain);
    let mut selected: Vec<(&'static str, Transaction)> = Vec::new();
    for _i in 0..2 {
        for tx in chain.iter() {
            if tx.1.index == index_one || tx.1.index == index_two {
                selected.push(tx.clone());}}}

    for i in 0..2 {
        if is_valid_transaction(&chain, selected[i].1.clone()) == true {
            continue;
        } else {
            panic!("Found an invalid transaction!");
        }}

    let tx_one = selected[0].clone();
    let tx_two = selected[1].clone();
    let cumulative = &selected[0].1.weight + &selected[1].1.weight;
    return (tx_one, tx_two, cumulative);
}

// This function is used to create a transaction and add it to the chain.
fn make_transaction (mut chain: Vec<(&'static str, Transaction)>, sender_address: &'static str, receiver_address: &'static str,
amount: f64, signature: &'static str) {
    let chain_ref = &chain;
    let edges_and_weights = select_edges_and_confirm_transactions(chain_ref);
    let transaction = Transaction {sender_address: sender_address, receiver_address: receiver_address, amount: amount,
    index: generate_index(chain_ref), timestamp: Utc::now(), signature: signature, weight: edges_and_weights.2, 
    edges: vec![edges_and_weights.0.1, edges_and_weights.1.1],};
    validate_and_append_transaction(chain, transaction);  
}

fn main () {}
