use chain::*;

fn main () {
    let chain = &mut generate_chain();
    let generation_number = 2;
    generate_genesis_transactions(chain);
    for _x in 0..generation_number {
        generate_random_transaction(chain);
    }
}