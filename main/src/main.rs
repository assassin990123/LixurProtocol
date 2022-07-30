use chain::*;

fn main () {
    let chain = &mut generate_chain();
    generate_genesis_transactions(chain)
}