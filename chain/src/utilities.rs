#[derive(Debug, Clone, PartialEq)]
#[derive(serde::Serialize, serde::Deserialize)]
pub struct Transaction {
    pub sender: String,
    pub receiver: String,
    pub amount: f64,
    pub signature: String, 
    pub status: &'static str,
    pub weight: f64,
    pub timestamp: String,
    pub edges: Vec<String>,
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

