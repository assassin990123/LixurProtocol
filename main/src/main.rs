use chain::*;
use std::thread::sleep;


fn main () {
    let chain = &mut generate_chain();
    let generation_number = 10;
    // generate_genesis_transactions(chain);
    for x in 0..generation_number {
        generate_random_transaction(chain);
        println!("{} transactions have been appended to the chain...", x+1);
        // sleep(Duration::from_secs());
    }
}