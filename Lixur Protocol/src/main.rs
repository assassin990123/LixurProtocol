pub use sha2::{Sha256, Digest};
pub use pqcrypto_dilithium::dilithium5::detached_sign as detached_sign;
pub use pqcrypto_dilithium::dilithium5::keypair as keypair;
pub use pqcrypto_dilithium::dilithium5::open as open;
pub use pqcrypto_dilithium::dilithium5::public_key_bytes as public_key_bytes;
pub use pqcrypto_dilithium::dilithium5::secret_key_bytes as secret_key_bytes;
pub use pqcrypto_dilithium::dilithium5::sign as dilithium_sign;
pub use pqcrypto_dilithium::dilithium5::signature_bytes as signature_bytes;
pub use pqcrypto_dilithium::dilithium5::verify_detached_signature as verify_detached_signature;

fn hash_bytes(bytes: pqcrypto_dilithium::dilithium5::PublicKey) -> String {
    let mut hasher = Sha256::new();
    hasher.update(bytes: pqcrypto_dilithium::dilithium5::PublicKey);
    let result = hasher.finalize();
    return format!("{:x}", result).to_string();
}

fn hash_string (string: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(string);
    let result = hasher.finalize();
    return format!("{:x}", result).to_string();
}

fn generate_keypair () -> (pqcrypto_dilithium::dilithium5::PublicKey, pqcrypto_dilithium::dilithium5::SecretKey, String) {
    let (public_key_bytes, private_key_bytes) = keypair();
    let hex_address = hash_bytes(public_key_bytes);
    return (public_key_bytes, private_key_bytes, hex_address);
}

fn main() {
    let hexa_address = generate_keypair().2;
    println!("Your Lixur address is: {}", hexa_address);
}