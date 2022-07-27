#![allow(dead_code)]

use std::thread;
use random_choice::random_choice;
use std::time::{SystemTime, Duration};
use std::fs::OpenOptions;
use chrono::Utc;
use sha2::{Sha256, Digest};
use std::fs::File;
use std::io::Write;
use std::path::Path;
// use std::io::Read;
// use serde::Serialize;
// use serde::ser::{Serializer};
// use std::time::{Instant};
// use thousands::Separable;
// extern crate crypto;
// use crypto::generate_keypair;

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
fn generate_chain () -> Vec<(String, Transaction)> {
    return Chain::new();
}

// This function returns the amount of transactions of a given chain.
fn count_chain_length (chain: &Vec<(String, Transaction)> ) -> usize {
    return chain.len();
}

// Returns the number of times an address has made a transaction on the chain.
fn get_appearances (chain: Vec<(String, Transaction)>, tx_id: String) -> usize {
    return chain.iter().filter(|i| i.0 == tx_id).count();
}

// This function generates and returns a Unix timestamp, which is the number of seconds since January 1, 1970, at midnight in UTC tim.
fn generate_unix_timestamp () -> Duration {
    return Duration::from_secs(SystemTime::now().duration_since(SystemTime::UNIX_EPOCH).unwrap().as_secs());
}

// This function generates and returns the current UTC time, formatted like this: Sat, 23 Jul 2022 19:08:43 +0000
fn generate_rfc_2822_timestamp () -> String {
    return Utc::now().to_rfc2822();
}

// This functions returns the balance of a given address.
fn get_balance (chain: &Vec<(String, Transaction)>, address: &String) -> f64 {
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
fn does_address_exist (chain: &Vec<(String, Transaction)>, address: String) -> bool {
    let mut exists = false;
    for tx in chain.iter() {
        if tx.1.sender == address || tx.1.receiver == address {
            exists = true;}
        }
    return exists;
}

// This function checks if a transaction is a valid transaction and returns the result, either true or false.
fn is_valid_transaction (chain: &Vec<(String, Transaction)>, transaction: Transaction) -> bool {
    let sender = transaction.sender.clone();
    let receiver = transaction.receiver.clone();

    if transaction.amount == 0.0 {
        println!("You can't send 0 LXR");
        return false;}

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
fn select_confirm_tips <'a> (chain: &Vec<(String, Transaction)>) -> Vec<(String, Transaction)> {
    let validation_count = 2;
    let mut unconfirmed: Vec<(String, Transaction)> = Vec::new();
    let mut valid: Vec<(String, Transaction)> = Vec::new();
    let mut weights: Vec<f64> = Vec::new();

    for tx in chain.iter() {

        if tx.1.status == "unconfirmed" {
            unconfirmed.push(tx.clone());}}
        
    for tx in unconfirmed.iter() {
        if is_valid_transaction(chain, tx.1.clone()) == true {
            valid.push(tx.clone());
            weights.push(tx.1.weight);}};

    // Choose three random transactions from the valid vec, and select them based on their weights.
    let mut selected: Vec<(String, Transaction)> = Vec::new();
    let mut indexes = vec![];
    let mut number: usize = 0;

    for _x in valid.iter() {
        number += 1;
        indexes.push(number);}

    let choices = random_choice().random_choice_f64(&indexes, &weights, validation_count);
    
    for x in choices.iter() {
        selected.push(valid[**x - 1].clone());}

    for x in selected.iter_mut() {
        x.1.edges.push(x.0.clone());
        x.1.status = "confirmed";}

    return selected;

}

// This function updates the chain.
fn update_chain (chain: Vec<(String, Transaction)>) {
    if Path::new("main/chain.json").exists() {
        OpenOptions::new().write(true).truncate(true).open("main/chain.json").unwrap().write_all(serde_json::to_string(&chain).unwrap().as_bytes()).expect("Something went wrong.");
    } else {
    File::create("main/chain.json").unwrap().write_all(serde_json::to_string(&chain).unwrap().as_bytes()).unwrap();
    }  
}

// This function makes a transaction and adds it to the chain.
fn make_transaction (mut chain: Vec<(String, Transaction)>, sender: String, receiver: String, amount: f64, signature: String) {
    let thread = thread::spawn (move || {
    chain.push((generate_tx_id(), Transaction { sender:sender, receiver:receiver, amount:amount, signature:signature, status:"unconfirmed", weight:1.0, timestamp: generate_rfc_2822_timestamp(), edges: vec![]}));
    update_chain(chain);});
    thread.join().unwrap();
}

// This function generates the first transactions to the chain.
// fn generate_chain_genesis_transactions (mut chain: Vec<(String, Transaction)>) {
//     for _z in 0..2 {
//         // None
//     }
// }

fn main() {
    let key = generate_phrase();
    println!("Your phrase is: {}", key);
}
