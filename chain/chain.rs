pub use rand::Rng;
pub use chrono::Utc;
pub use std::time::Instant;
pub use std::fs::File;
pub use std::io::Write;

mod utilities;
use crate::utilities::{Transaction, Chain};

fn generate_graph() -> Vec<(&'static str, Transaction)> {
    return Chain::new();
}

fn count_graph_length (graph: &Vec<(&'static str, Transaction)> ) -> usize {
    return graph.len();
}

fn generate_index(graph: &Vec<(&'static str, Transaction)> ) -> usize {
    return count_graph_length(graph) + 1;
}

fn fetch_transaction(graph: Vec<(&'static str, Transaction)>, tx_id: &'static str) -> Option<Transaction> {
    return graph.iter().find(|i| i.0 == tx_id).and_then(|i| Some(i.1.clone()))
}

fn get_appearances (graph: Vec<(&'static str, Transaction)>, tx_id: &'static str) -> usize {
    return graph.iter().filter(|i| i.0 == tx_id).count();
}

fn check_balance (graph: &Vec<(&'static str, Transaction)>, address: &str) -> f64 {
    let mut balance = 0.0;
    for transaction in graph.iter() {
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

fn does_address_exist (graph: &Vec<(&'static str, Transaction)>, address: &str) -> bool {
    let mut exists = false;
    for tx in graph.iter() {
        if tx.1.sender_address == address || tx.1.receiver_address == address {
            exists = true;}
        }
    return exists;
}

fn generate_random_indexes (graph: &Vec<(&'static str, Transaction)>) -> (usize, usize) {
    let mut rng = rand::thread_rng();
    let index_one = rng.gen_range(0..count_graph_length(graph));
    let mut index_two = rng.gen_range(0..count_graph_length(graph));
    while index_one == index_two {
        index_two = rng.gen_range(0..count_graph_length(graph));
    }
    return (index_one, index_two);
}

// (&'a mut (&'static str, Transaction), &'a mut (&'static str, Transaction), u128)

fn select_edges_and_confirm_transactions <'a> (graph: &Vec<(&'static str, Transaction)>)
    -> ((&'a str, Transaction), (&'a str, Transaction), u128) {
    let (index_one, index_two) = generate_random_indexes(graph);
    let mut selected: Vec<(&'static str, Transaction)> = Vec::new();
    for _i in 0..2 {
        for tx in graph.iter() {
            if tx.1.index == index_one || tx.1.index == index_two {
                selected.push(tx.clone());
            }
        }
    }

    for i in 0..2 {
        if is_valid_transaction(graph, selected[i].1.clone()) == true {
            continue;
        } else {
            panic!("Found an invalid transaction!");
        }
    }

    let tx_one = selected[0].clone();
    let tx_two = selected[1].clone();
    let cumulative = &selected[0].1.weight + &selected[1].1.weight;

    return (tx_one, tx_two, cumulative);
}

fn make_transaction <'a> (mut graph: Vec<(&'static str, Transaction)>, sender_address: &'static str, receiver_address: &'static str,
 amount: f64, signature: &'static str,) {
    let edges_and_weights = select_edges_and_confirm_transactions(&mut graph);
    let transaction = Transaction {sender_address: sender_address, receiver_address: receiver_address, amount: amount,
        index: generate_index(&graph), timestamp: Utc::now(), signature: signature, weight: edges_and_weights.2,
        edges: vec![edges_and_weights.0.1, edges_and_weights.1.1],};
    // If it is valid, then boot up the necessary variables (edges) and add it to the graph
    graph.push((signature, transaction));
}

fn main () {}
