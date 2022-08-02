#![allow(dead_code)]
pub use pqcrypto_dilithium::dilithium5::DetachedSignature;
pub use pqcrypto_traits::sign::PublicKey;
pub use pqcrypto_traits::sign::SecretKey;
pub use pqcrypto_traits::sign::VerificationError;
pub use pqcrypto_traits::sign::DetachedSignature as SignatureDetached;
pub use pqcrypto_dilithium::dilithium5::detached_sign;
pub use pqcrypto_dilithium::dilithium5::verify_detached_signature;
pub use pqcrypto_dilithium::dilithium5::keypair;
pub use magic_crypt::{new_magic_crypt, MagicCryptTrait, MagicCryptError};
pub use sha2::{Sha256, Digest};
pub use std::io::Read;
pub use std::path::Path;
pub use std::io::Write;
pub use std::fs::File;
pub use rand::Rng;

// This function generates and returns a Dilithium-5 derived public, private and a wallet address. 
pub fn generate_keypair() -> (pqcrypto_dilithium::dilithium5::PublicKey, pqcrypto_dilithium::dilithium5::SecretKey, String) {
    let (public_key, private_key) = keypair();
    return (public_key, private_key, hash_public_key(public_key));
}

// This function takes a private and public key, signs them and returns a signature.
pub fn sign (private_key: &pqcrypto_dilithium::dilithium5::SecretKey) -> DetachedSignature {
    return detached_sign("Lixur".to_string().as_bytes(), private_key)
}

// This function verifies the legitimacy of a signature.
pub fn verify (signature: DetachedSignature, public_key: &pqcrypto_dilithium::dilithium5::PublicKey) -> bool {
    let result = verify_detached_signature(&signature, "Lixur".to_string().as_bytes(), public_key);
    if result.is_ok() {
        return true;
    } else {
        return false;
    }
}

// This function hashes and returns a hashed string of a given public key using the SHA256 algorithm.
pub fn hash_public_key(bytes: pqcrypto_dilithium::dilithium5::PublicKey) -> String {
    let mut hasher = Sha256::new();
    hasher.update(bytes.as_bytes());
    let result = hasher.finalize();
    return format!("{:x}", result).to_string();
}

// This function hashes and returns a hashed string of a given signature using the SHA256 algorithm.
pub fn hash_encrypted_signature(encrypted_signature: String) -> String {
    let mut hasher = Sha256::new();
    hasher.update(encrypted_signature.as_bytes());
    let result = hasher.finalize();
    return format!("{:x}", result).to_string();
}

// This function hashes and returns a hashed string of a given signature using the SHA256 algorithm.
pub fn hash_string(string: &String) -> String {
    let mut hasher = Sha256::new();
    hasher.update(string);
    let result = hasher.finalize();
    return format!("{:x}", result).to_string();
}

// Generates and returns an 8 word phrase, each word consisting of four letters.
pub fn generate_phrase() -> String {
    let mut phrase = String::new();
    let mut file = File::open("src/words.txt").expect("Failed to open words.txt");
    let mut contents = String::new();
    file.read_to_string(&mut contents).expect("Failed to read words.txt");
    let words: Vec<&str> = contents.split("\n").collect();
    for _ in 0..8 {
        let index = rand::thread_rng().gen_range(0..2499);
        phrase.push_str(words[index]);
        phrase.push(' ');
    }
    let _phrase = phrase.replace("\r", "").clone().to_string();
    return _phrase[.._phrase.len() - 1].to_string();
}

// Encrypts a given phrase using AES encryption. The user inputs their phrase, public key and private key and the program returns the encrypted phrase.
pub fn encrypt_wallet(phrase: &String, public_key: &pqcrypto_dilithium::dilithium5::PublicKey, private_key: &pqcrypto_dilithium::dilithium5::SecretKey) -> (String, pqcrypto_dilithium::dilithium5::PublicKey, String, String) {
    let salt = hash_string(&generate_phrase());
    let phrase_and_salt = phrase.to_owned() + &salt;
    return (new_magic_crypt!(&phrase_and_salt, 256).encrypt_bytes_to_base64(private_key.as_bytes()), *public_key,
    hash_string(&phrase_and_salt), salt);
}

// Decrypts a given phrase using AES decryption. The user inputs their phrase, hash of the phrase + salt, salt and ciphertext and the program returns the private key.
pub fn decrypt_wallet(phrase: &mut String, hash: &String, salt: &String, ciphertext: &String) -> pqcrypto_dilithium::dilithium5::SecretKey {
    println!("Please insert your decryption phrase: ");
    loop {std::io::stdin().read_line(phrase).expect("Failed to read line");
        *phrase = phrase.replace("\r", "").replace("\n", "")[..phrase.len() - 41].to_string() + salt;
        if &hash_string(phrase) == hash {
            println!("Success! You've entered the correct phrase, decrypting...");
            let result = new_magic_crypt!(phrase, 256).decrypt_base64_to_string(ciphertext).unwrap();
            return pqcrypto_dilithium::dilithium5::SecretKey::from_bytes(&result.as_bytes()).unwrap();
        } else {
            println!("Failed to enter the correct phrase, please try again.");
        }
    }
}

// Encrypts a given signature and public key using AES encryption. The function returns both values, in an encrypted manner.
pub fn encrypt_signature_and_public_key (signature: DetachedSignature, public_key: pqcrypto_dilithium::dilithium5::PublicKey) -> (String, String) {
    let signature_cipher = new_magic_crypt!("Lixur").encrypt_bytes_to_base64(signature.as_bytes());
    let public_key_cipher = new_magic_crypt!("Lixur").encrypt_bytes_to_base64(public_key.as_bytes());
    return (signature_cipher, public_key_cipher);
}

// Decrypts a given signature using AES decryption. The function returns a decrypted signature.
pub fn decrypt_signature (ciphertext: String) -> DetachedSignature {
    return DetachedSignature::from_bytes(&new_magic_crypt!("Lixur").decrypt_base64_to_bytes(ciphertext.clone()).unwrap()).unwrap();
}

// Decrypts a given public key using AES decryption. The function returns a decrypted public key.
pub fn decrypt_public_key (ciphertext: String) -> pqcrypto_dilithium::dilithium5::PublicKey {
    return pqcrypto_dilithium::dilithium5::PublicKey::from_bytes(&new_magic_crypt!("Lixur").decrypt_base64_to_bytes(ciphertext.clone()).unwrap()).unwrap();
}

// This function generates a keystore file for a user containing the wallet information, which is paramount to be able to access their account.
pub fn generate_keystore() {
    println!("Generating keystore...");
    let (public_key, private_key, _hex_address) = generate_keypair();
    let phrase = generate_phrase();
    println!("Your address on Lixur is: {}", hash_public_key(public_key));
    println!("Your phrase is: {}. Make sure you save this somewhere and do not share it with anyone! If you lose the phrase
    you will also lose access to all of your funds.", phrase);
    let (ciphertext, public_key, hash, salt) = encrypt_wallet(&phrase, &public_key, &private_key);
    let mut file = File::create("keystore.txt").expect("Failed to create the keystore file.");
    file.write_all(&ciphertext.as_bytes()).expect("Failed to write the ciphertext to the keystore file.");
    file.write(b"\n").expect("Failed to write a newline to the keystore file.");
    println!("Ciphertext Added!");
    file.write_all(public_key.as_bytes()).expect("Failed to write the public_key to the keystore file.");
    file.write(b"\n").expect("Failed to write a newline to the keystore file.");
    println!("Public Key Added!");
    file.write_all(&hash.as_bytes()).expect("Failed to write the hash to the keystore file.");
    file.write(b"\n").expect("Failed to write a newline to the keystore file.");
    println!("Hash Added!");
    file.write_all(salt.as_bytes()).expect("Failed to write the salt to the keystore file.");
    file.write(b"\n").expect("Failed to write a newline to the keystore file.");
    println!("Salt Added!");
    println!("Keystore generated successfully!");
    println!("Please save this file somewhere safe, do not ever lose it, don't let it get corrupted, and do not share it with anyone!
    If you lose it you will permanently lose access to all of your funds.");
    println!("It's suggested you copy it to multiple devices, especially a USB drive to make sure you never lose it.")
}

// Loads an existing keystore file for a user. The only parameter needed is the path to the keystore file.
pub fn load_keystore(directory: &str) -> (pqcrypto_dilithium::dilithium5::PublicKey, pqcrypto_dilithium::dilithium5::SecretKey, String) {
    println!("Loading keystore file...");
    let mut file = File::open(directory).expect("Failed to open the keystore file. This his could be due to it being corrupted");
    let mut ciphertext = String::new();
    let mut public_key = String::new();
    let mut hash = String::new();
    let mut salt = String::new();
    file.read_to_string(&mut ciphertext).expect("Failed to read the ciphertext from the keystore file.");
    file.read_to_string(&mut public_key).expect("Failed to read the public_key from the keystore file.");
    file.read_to_string(&mut hash).expect("Failed to read the hash from the keystore file.");
    file.read_to_string(&mut salt).expect("Failed to read the salt from the keystore file.");
    let mut phrase = String::new();
    println!("Please insert your decryption phrase: ");
    loop {std::io::stdin().read_line(&mut phrase).expect("Failed to read line");
        let mut phrase_and_salt = String::new();
        phrase_and_salt.push_str(&phrase);
        phrase_and_salt.push_str(&salt);
        if hash_string(&phrase_and_salt) == hash {
            println!("Success! You've entered the correct phrase, decrypting...");
            let private_key = decrypt_wallet(&mut phrase, &hash, &salt, &ciphertext);
            let public_key = pqcrypto_dilithium::dilithium5::PublicKey::from_bytes(&public_key.as_bytes()).unwrap();
            let hex_address = hash_public_key(public_key);
            return (public_key, private_key, hex_address);
        }
    }
}

// The main function for booting and loading keystores. Think of this as a start menu for the program when it comes to wallets. 
// If a keystore exists, the function loads the wallet. If it doesn't, then a new one is created or it asks the user for the directory of the wallet.
pub fn wallet(directory: &mut String) {
    if Path::new(directory).exists() {
        println!("Keystore file detected!");
        load_keystore(directory);
    } else {
        println!("We couldn't find your keystore file, would you like to generate a new wallet? (Yes/No)");
        let mut input = String::new();
        loop {
            std::io::stdin().read_line(&mut input).expect("Failed to read line");
            if input.trim() == "Yes" {
                generate_keystore();
            } else if input.trim() == "No" {
                println!("Please enter the directory of your wallet: ");
                std::io::stdin().read_line(directory).expect("Failed to read line");
                *directory = directory.replace("\r", "").replace("\n", "")[..directory.len() - 1].to_string();
                if !Path::new(directory).exists() {
                    println!("Wallet does not exist, please create it first.");
                    return;
                } else {
                    println!("Wallet loaded successfully!");
                }
            } else {
                println!("Please enter either Yes or No.");
            }
        }
    }
}

fn main () {}