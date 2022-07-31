use std::time::{Duration};
#[derive(Debug, Clone, PartialEq)]
#[derive(serde::Serialize, serde::Deserialize)]
pub struct Transaction {
    pub sender: String,
    pub receiver: String,
    pub amount: f64,
    pub signature: String, 
    pub status: &'static str,
    pub weight: u32,
    pub timestamp: (String, Duration),
    pub index: u32,
    pub edges: Vec<(String, String)>,
}

#[derive(Clone)]
pub struct Chain{
    pub chain: Vec<(String, Transaction)>,
}

impl Chain {
    pub fn new() -> Vec<(String, Transaction)> {
        return Vec::new();
    }
}

