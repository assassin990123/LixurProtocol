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
use std::time::Instant;

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

// This function returns the amount of transactions of a given chain.
pub fn count_chain_length (chain: &Vec<(String, Transaction)> ) -> u32 {
    return chain.len() as u32;
}

// This generates the index number for each transaction.
pub fn generate_index (chain: &Vec<(String, Transaction)>) -> u32 {
    return count_chain_length(chain) + 1;
}

// Returns the number of times an address has made a transaction on the chain.
pub fn get_appearances (chain: Vec<(String, Transaction)>, tx_id: String) -> usize {
    return chain.iter().filter(|i| i.0 == tx_id).count();
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
        if &transaction.1.sender == address && &transaction.1.receiver == address {
            balance += transaction.1.amount;
        }
        if &transaction.1.sender == address {
            balance -= transaction.1.amount;
        } else if &transaction.1.receiver == address {
            balance += transaction.1.amount;
        }
    }
    return balance;
}

// This function checks if an address exists on the chain
pub fn does_address_exist (chain: &Vec<(String, Transaction)>, address: String) -> bool {
    let mut exists = false;
    for tx in chain.iter() {
        if tx.1.sender == address || tx.1.receiver == address {
            exists = true;}
        }
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
pub fn select_confirm_tips <'a> (chain: &mut Vec<(String, Transaction)>) {
    if chain.len() < 1 {
        for x in chain.iter_mut() {
            x.1.edges.push(("None".to_string(), "None".to_string()));}
    } else { 
    let time = Instant::now();
    let validation_count = 2;
    let mut unconfirmed: Vec<(String, Transaction)> = Vec::new();
    let mut valid: Vec<(String, Transaction)> = Vec::new();
    let mut selected: Vec<(String, Transaction)> = Vec::new();
    let mut weights: Vec<u32> = Vec::new();

    for tx in chain.iter_mut() {
        if tx.1.status != "confirmed" {
            unconfirmed.push(tx.clone())}}
    
    for tx in unconfirmed.iter() {
        if is_valid_transaction(chain, tx.1.clone()) == true {
            valid.push(tx.clone());
            weights.push(tx.1.weight.clone());
        }}
    
    let dist = WeightedIndex::new(&weights).unwrap();
    let mut rng = thread_rng();
    for _ in 0..validation_count {
        selected.push(valid[dist.sample(&mut rng)].clone())}

    for tx in selected.iter_mut() {
        tx.1.edges.push((selected[0].0.clone(), selected[1].0.clone()));
        tx.1.status = "confirmed";
        for x in chain.iter_mut() {
            if x.0 == tx.0 {
                x.1 = tx.1.clone()}}
}}}
    

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
    select_confirm_tips(chain);
    chain.push((generate_tx_id(), Transaction { sender:sender, receiver:receiver, amount:amount, signature:signature, status:"pending",
     weight:generate_index(chain), index: generate_index(chain), timestamp: (generate_rfc_2822_timestamp(), generate_unix_timestamp()), edges: vec![]}));
    update_chain(&chain);
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
    for _z in 0..3 {
        let keys_one = generate_keypair();
        let keys_two = generate_keypair();
        let signature = sign_and_verify(&keys_one.0, &keys_one.1);
        make_transaction(chain, keys_one.2, keys_two.2, 0.0, signature.1);
    }
}

fn main() {}
