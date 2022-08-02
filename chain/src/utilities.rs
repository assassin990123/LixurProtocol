#[derive(Clone, PartialEq)]
#[derive(serde::Serialize, serde::Deserialize)]
pub struct Transaction {
    pub sender: String,
    pub receiver: String,
    pub amount: f64,
    pub signature: (String, String), 
    pub status: &'static str,
    pub transaction_type: &'static str,
    pub readable_hash: String,
    pub weight: u32,
    pub timestamp: (String, f64),
    pub index: u32,
    pub edges: Vec<(String, String)>,
    pub validators: Vec<String>,
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