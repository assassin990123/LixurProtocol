use chrono::{DateTime, Utc};

#[derive(Debug)]
#[derive(Clone)]

pub struct Transaction {
    pub sender_address: &'static str,
    pub receiver_address: &'static str,
    pub amount: f64,
    pub timestamp: DateTime<Utc>,
    pub signature: &'static str,
    pub weight: u128,
    pub edges: Vec<Transaction>, // I have no clue the true type
    pub index: usize,
}

impl ToString for Transaction {
    fn to_string(&self) -> String {
        return format!("{}", self.sender_address);
    }
}
    
pub struct Chain {
    pub transaction: Vec<(&'static str, Transaction)>,
}

impl Chain {
    pub fn new() -> Vec<(&'static str, Transaction)> {
        return Vec::new();
    }
}
