#![allow(dead_code)]

use rand::distributions::WeightedIndex;
use rand::distributions::Distribution;
use rand::thread_rng;
use std::time::{SystemTime, Duration};
use std::fs::OpenOptions;
use chrono::Utc;
use sha2::{Sha256, Digest};
use std::fs::File;
use std::io::Write;
use std::path::Path;

use crypto::*;
mod utilities;
use utilities::{Transaction, Chain};

// This function generates a random transaction ID.
pub fn generate_tx_id () -> String {
    let mut hasher = Sha256::new();
    hasher.update(format!("{}", Utc::now()));
    let output = hasher.finalize();
    return format!("{:x}", output);
}

// This function generates and returns a new, empty chain (directed acyclic graph).
pub fn generate_chain () -> Vec<(String, Transaction)> {
    return Chain::new();
}

// This function returns the amount of transactions on the chain.
pub fn count_chain_length (chain: &Vec<(String, Transaction)> ) -> u32 {
    return chain.len() as u32;
}

// This function returns the amount of confirmed transactions on the chain.
pub fn count_confirmed_chain_length (chain: &Vec<(String, Transaction)> ) -> u32 {
    let mut count = 0;
    for (_, tx) in chain.iter() {
        if tx.status == "confirmed" {
            count += 1;
        }
    }
    return count;
}

// This generates the index number for each transaction.
pub fn generate_index (chain: &Vec<(String, Transaction)>) -> u32 {
    return count_chain_length(chain) + 1;
}

// This function generates and returns a Unix timestamp, which is the number of seconds since January 1, 1970, at midnight in UTC tim.
pub fn generate_unix_timestamp () -> Duration {
    return Duration::from_secs(SystemTime::now().duration_since(SystemTime::UNIX_EPOCH).unwrap().as_secs());
}

// This function generates and returns the current UTC time, formatted like this: Sat, 23 Jul 2022 19:08:43 +0000
pub fn generate_rfc_2822_timestamp () -> String {
    return Utc::now().to_rfc2822();
}

// This functions returns the balance of a given address.
pub fn get_balance (chain: &Vec<(String, Transaction)>, address: &String) -> f64 {
    let mut balance = 0.0;
    for transaction in chain.iter() {
        if transaction.1.status == "confirmed" {
        if &transaction.1.sender == address && &transaction.1.receiver == address {
            balance += transaction.1.amount;
        }
        if &transaction.1.sender == address {
            balance -= transaction.1.amount;
        } else if &transaction.1.receiver == address {
            balance += transaction.1.amount;
            }
        }
    }
    return balance;
}

// This function checks if an address exists on the chain
pub fn does_address_exist (chain: &Vec<(String, Transaction)>, address: String) -> bool {
    let mut exists = false;
    for tx in chain.iter() {
        if tx.1.status == "confirmed" {
        if tx.1.sender == address || tx.1.receiver == address {
            exists = true;}
        }}
    return exists;
}

// This function checks if a transaction is a valid transaction and returns the result, either true or false.
pub fn is_valid_transaction (chain: &Vec<(String, Transaction)>, transaction: Transaction) -> bool {
    let sender = transaction.sender.clone();
    let receiver = transaction.receiver.clone();

    if get_balance (&chain, &sender) < transaction.amount {
        return false;}

    if transaction.amount < 0.0 {
        println!("You can't send negative quantities of LXR");
        return false;}

    if &sender == &receiver {
        println!("You can't send LXR to yourself");
        return false;}

    if transaction.signature.len() != 64 {
        println!("Invalid signature");
        return false;}
    
    if does_address_exist(chain, transaction.receiver) == false {
        println!("The receiver's address does not exist on the chain");
        return false;}
    
    if does_address_exist(chain, transaction.sender) == false {
        println!("Your address does not exist on the chain");
        return false;}

    else {return true;}
}

// This function selects the tips of the chain (the unconfirmed transactions) to confirm in a biased manner, prioritizing ones with higher weights.
pub fn select_confirm_tips <'a> (chain: &mut Vec<(String, Transaction)>, signature: String) -> (String, String) {
    // All of the vectors and variables are initialized here.
    let validation_count = 2;

    // If the chain is empty, this transaction won't have any edges.
    if chain.len() == 0 {
        return ("None".to_string(), "None".to_string())} 
    
    // If the chain only has one transaction, the transaction will only have one edge. We must also validate the genesis transaction.
    if chain.len() == 1 {
        for tx in chain.iter_mut() {
            // We first check if the genesis transaction is valid, if it is, we continue. If not, we panic.
            // We will edit the transaction's validators (A validator will use it's signature). If it doesn't have any, it will only add one validator.
            if tx.1.validators.len() == 0 {
                tx.1.validators.push(signature.clone())

            // Else, if it has one validator, we will add another.
            } else {
                tx.1.validators.push(signature.clone())}
    
            // The transaction's status will be set to "confirmed", if it has two validators else, its status doesn't change.
            if tx.1.validators.len() == validation_count {tx.1.status = "confirmed"}
        } return (chain[0].0.clone(), "None".to_string())

    // Else, it will have to have x number of edges, which is determined by the number the variable "validation_count".    // 
    } else { 
    
    // Initializing all of the necessary vectors.
    let mut unconfirmed: Vec<(String, Transaction)> = Vec::new();
    let mut valid: Vec<(String, Transaction)> = Vec::new();
    let mut selected: Vec<(String, Transaction)> = Vec::new();
    let mut weights: Vec<u32> = Vec::new();

    // This for loop adds all the unconfirmed transactions to the unconfirmed vector.
    for tx in chain.iter_mut() {
        if tx.1.status != "confirmed" {
            unconfirmed.push(tx.clone())}}
    
    // All of the valid transactions on the chain gets added to the valid vector, and the weights of the transactions are added to the weights vector.
    for tx in unconfirmed.iter() {
        if is_valid_transaction(chain, tx.1.clone()) == true {
            valid.push(tx.clone());
            weights.push(tx.1.weight.clone())}}
    
    // This loop selects the unconfirmed transactions to verify, prioritizing ones with higher weights.
    let dist = WeightedIndex::new(&weights).unwrap();
    let mut rng = thread_rng();

    for _ in 0..validation_count {
        // It keeps selecting until the selected vector reaches x number of transactions, specified by the variable "validation_count".
        while selected.len() != validation_count {
            selected.push(valid[dist.sample(&mut rng)].clone())}

        // This removes any duplicate transactions from the selected vector and keeps going until there are no more duplicates.
        while selected[0] == selected[1] {
            selected.pop();
            selected.push(valid[dist.sample(&mut rng)].clone())}}
    
    // The transactions it has selected will now be confirmed.
    let edges = (selected[0].0.clone(), selected[1].0.clone());
    for tx in selected.iter_mut() {

        // We will edit the transaction's validators (A validator will use it's signature), If it doesn't have any, it will only add one validator.
        if tx.1.validators.len() == 0 {
            tx.1.validators.push(signature.clone())}

        // Else, if it has one validator, it will add another.
        else {
            tx.1.validators.push(signature.clone())}

        // The transaction's status is now confirmed.
        if tx.1.validators.len() == 2 {tx.1.status = "confirmed"}

        for x in chain.iter_mut() {
            if x.0 == tx.0 {
                x.1 = tx.1.clone()}}}
    // The edges are returned to be added to the current transaction performing the tip selection.
    return edges;   
    }
}

// This function updates the chain.
pub fn update_chain (chain: &Vec<(String, Transaction)>) {
    let directory = "chain/chain.json";
    if Path::new(directory).exists() {
        OpenOptions::new().write(true).truncate(true).open(directory).unwrap().write_all(serde_json::to_string(&chain).unwrap().as_bytes()).expect("Something went wrong.");
    } else {
    File::create(directory).unwrap().write_all(serde_json::to_string(&chain).unwrap().as_bytes()).unwrap();
    }  
}

// This function makes a transaction and adds it to the chain.
pub fn make_transaction (chain: &mut Vec<(String, Transaction)>, sender: String, receiver: String, amount: f64, signature: String) {
    let edges = select_confirm_tips(chain, signature.clone());
    chain.push((generate_tx_id(), Transaction { sender:sender, receiver:receiver, amount:amount, signature:signature, status:"pending",
    weight:1, index: generate_index(chain), timestamp: (generate_rfc_2822_timestamp(), generate_unix_timestamp().as_secs_f64()), edges: vec![edges],
    transaction_type: "transaction", readable_hash: "None".to_string(), validators: vec![]}));
    update_chain(&chain)
}

// Generates a completely random transaction to the chain.
pub fn generate_random_transaction (chain: &mut Vec<(String, Transaction)>) {
    let keys_one = generate_keypair();
    let keys_two = generate_keypair();
    let signature = sign_and_verify(&keys_one.0, &keys_one.1);
    make_transaction(chain, keys_one.2, keys_two.2, 0.0, signature.1);
}

// This function generates the first transactions to the chain.
pub fn generate_genesis_transactions (chain: &mut Vec<(String, Transaction)>) {
    let validation_count = 2;
    for _z in 0..validation_count {
        let keys_one = generate_keypair();
        let keys_two = generate_keypair();
        let signature = sign_and_verify(&keys_one.0, &keys_one.1);
        make_transaction(chain, keys_one.2, keys_two.2, 0.0, signature.1);
    }
}

fn main() {}