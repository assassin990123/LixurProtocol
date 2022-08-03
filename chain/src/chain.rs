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
pub fn count_chain_length (chain: &Vec<(String, Transaction)> ) -> u128 {
    return chain.len() as u128;
}

// This function returns the amount of confirmed transactions on the chain.
pub fn count_confirmed_chain_length (chain: &Vec<(String, Transaction)> ) -> u128 {
    let mut count = 0;
    for (_, tx) in chain.iter() {
        if tx.status == "confirmed" {
            count += 1;
        }
    }
    return count;
}

// This generates the index number for each transaction.
pub fn generate_index (chain: &Vec<(String, Transaction)>) -> u128 {
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
pub fn is_valid_transaction (chain: &Vec<(String, Transaction)>, mut transaction: Transaction) -> bool {
    let sender = transaction.sender.clone();
    let receiver = transaction.receiver.clone();

    // If the user doesn't have enough money, then the transaction is marked as failed.
    if get_balance (&chain, &sender) < transaction.amount {
        transaction.status = "failed";
        return false;}

    // If the user tries to send negative amounts of money, the transaction is marked as failed.
    if transaction.amount < 0.0 {
        println!("You can't send negative quantities of LXR");
        transaction.status = "failed";
        return false;}

    // If the user tries to send themselves money, the transaction is marked as failed.
    if &sender == &receiver {
        println!("You can't send LXR to yourself");
        transaction.status = "failed";
        return false;}
    
    // If the user ties to send fake or invalid signatures, the transaction is marked as failed.
    if verify(decrypt_signature(transaction.signature.0),
    &decrypt_public_key(transaction.signature.1)) != true {
        println!("The signature is invalid");
        transaction.status = "failed";
        return false;}
    
    // If the person the user is trying to send LXR to doesn't exist, the transaction is marked as failed.
    // if does_address_exist(chain, transaction.receiver) == false {
    //     transaction.status = "failed";
    //     println!("The receiver's address does not exist on the chain");
    //     return false;}
    
    // If the user's address is not on the chain, the transaction is marked as failed.
    // if does_address_exist(chain, transaction.sender) == false {
    //     transaction.status = "failed";
    //     println!("Your address does not exist on the chain");
    //     return false;}

    else {return true;}
}

// If a transaction hasn't been validated for x amount of time, it will be marked as failed.
pub fn declare_failed_transaction (chain: &mut Vec<(String, Transaction)>) {
    let hours = 3600.0*24.0; // 24 hours in seconds
    loop {
    for tx in chain.iter_mut() {
        // Get the current time in unix timestamp format.
        let current_unix_timestamp = generate_unix_timestamp().as_secs_f64();
        // If a transaction has been labeled as "pending" for more than 24 hours, it will be marked as "failed".
        if tx.1.status == "pending" && current_unix_timestamp - tx.1.timestamp.1 > hours  {
            println!("Transaction {} failed", tx.0);
                tx.1.status = "failed";
            }
        }
    update_chain(chain);
    }
}

// This function selects other unconfirmed transactions to confirm in a biased manner, prioritizing ones with higher weights.
pub fn select_confirm_tips <'a> (chain: &mut Vec<(String, Transaction)>, id: String, own_weight: u128)-> (String, String) {
    // This usually takes a few milliseconds to perform, on faster PCs, it can be a few microseconds even.

    // All of the vectors and variables are initialized here.
    let validation_count = 2;

    // If the chain is empty, this transaction won't have any edges.
    if chain.len() == 0 {
        return ("None".to_string(), "None".to_string())} 
    
    // If the chain only has the genesis transaction, that will be the one we will validate.
    if chain.len() == 1 {
        for tx in chain.iter_mut() {
            // We will add ourselves as the validator of this transaction, and will edit the (cumulative) weight of the transaction.
                tx.1.validators.push(id.clone());
                tx.1.weight = tx.1.weight + own_weight;
    
            // The transaction's status will be set to "confirmed" if it has two validators otherwise, its status doesn't change.
            if tx.1.validators.len() == validation_count {tx.1.status = "confirmed"}
        } return (chain[0].0.clone(), "None".to_string())

    // Else, it will have to have x number of edges, which is determined by the number the variable "validation_count".
    } else { 
    
    // Initializing all of the necessary vectors.
    let mut unconfirmed: Vec<(String, Transaction)> = Vec::new();
    let mut valid: Vec<(String, Transaction)> = Vec::new();
    let mut selected: Vec<(String, Transaction)> = Vec::new();
    let mut weights: Vec<u128> = Vec::new();

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

        // We will add ourselves as the validator of this transaction, and will edit the (cumulative) weight of the transaction.
            tx.1.validators.push(id.clone());
            tx.1.weight = tx.1.weight + own_weight;

        // The transaction's status will be set to "confirmed" if it has two validators otherwise, its status doesn't change.
        if tx.1.validators.len() == 2 {tx.1.status = "confirmed"}

        // The transaction is now updated with the changes. 
        for x in chain.iter_mut() {
            if x.0 == tx.0 {
                x.1 = tx.1.clone()}}}
                
    // The edges are returned to be added to the current transaction performing the tip selection.
    return edges;   
    }
}

// This function updates the chain.
pub fn update_chain (chain: &mut Vec<(String, Transaction)>) {
    let directory = "chain/chain.json";
    
    // If the file exists, we will edit it and add the new transactions.
    if Path::new(directory).exists() {
        OpenOptions::new().write(true).truncate(true).open(directory).unwrap().write_all(serde_json::to_string(&chain).unwrap().as_bytes()).expect("Something went wrong.");
    } 
    
    // Else, we will create a new file and add the new transactions.
    else {
    File::create(directory).unwrap().write_all(serde_json::to_string(&chain).unwrap().as_bytes()).unwrap();
    }  
}

// This function makes a transaction and adds it to the chain.
pub fn make_transaction (chain: &mut Vec<(String, Transaction)>, id: String, sender: String, receiver: String, amount: f64, signature: (String, String)) {
    // We initialize the weight of this transaction.
    let own_weight = 1;

    // We gather the edges of the transaction being made.
    let edges = select_confirm_tips(chain, id.clone(), own_weight as u128);

    // We add the transaction to the chain.
    chain.push((id.clone(), Transaction { sender:sender, receiver:receiver, amount:amount, signature:signature, status:"pending",
    weight:1, index: generate_index(chain), timestamp: (generate_rfc_2822_timestamp(), generate_unix_timestamp().as_secs_f64()), edges: vec![edges],
    transaction_type: "transaction", readable_hash: "None".to_string(), validators: vec![]}));

    // We update the chain with the new transaction.
    update_chain(chain)
}

// Generates a completely random transaction to the chain.
pub fn generate_random_transaction (chain: &mut Vec<(String, Transaction)>) {
    let keys_one = generate_keypair();
    let keys_two = generate_keypair();
    let signature = sign(&keys_one.1);
    make_transaction(chain, generate_tx_id(), keys_one.2, keys_two.2, 0.0,
    encrypt_signature_and_public_key(signature, keys_one.0));
}

// This function generates the first transactions to the chain.
pub fn generate_genesis_transactions (chain: &mut Vec<(String, Transaction)>) {
    let validation_count = 2;
    for _z in 0..validation_count {
        let keys_one = generate_keypair();
        let keys_two = generate_keypair();
        let signature = sign(&keys_one.1);
        make_transaction(chain, generate_tx_id(), keys_one.2, keys_two.2, 0.0,
        encrypt_signature_and_public_key(signature, keys_one.0));
    }
}

// Initates the chain and generates the first transactions.
pub fn initiate_chain () {
    let chain = &mut generate_chain();
    let generation_number = 1;
    generate_genesis_transactions(chain);
    for _x in 0..generation_number {
        generate_random_transaction(chain);
    }
    // declare_failed_transaction(chain);
}

fn main() {}