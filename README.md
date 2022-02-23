# Lixur

Welcome! We're glad to have you here!

Lixur is an open-sourced project building a distributed ledger platform. Designed to be extremely beginner friendly, no-code SDKs with AI assistance ensures that anyone, anywhere can deploy decentralized applications on Lixur. Lixur uses things such as DAGs and A.I smart contracts which enables fast, privacy-preserving, feeless, infinitely scalable, quantum resistant and an interconnected ecosystem, which users can make use of for any application requiring decentralized, automated intelligence and more. To learn more, please read the whitepaper here: https://drive.google.com/file/d/1mfqufIxTuvegdc8VjfgJahROHA6CBJHM/view?usp=sharing

For those examining the code and are concerned with the speed of Python, This code will soon feature a JIT Complier that will accelerate the code either with Numba (Accelerating execution speed on par with Go or Julia) or with RustPython (Accelerating execution time on par with Rust).

![image](https://user-images.githubusercontent.com/87288707/155394541-28719860-ac4e-4db8-97d4-c7c2980cb273.png)
![image](https://user-images.githubusercontent.com/87288707/155394794-6cd735c6-93ea-41fc-abb3-844f90c60162.png) (The left is Python + Numba, the right is Go)
![image](https://user-images.githubusercontent.com/87288707/155395059-717c2782-cd2c-4974-bcc5-7c718c9a4561.png)
![image](https://user-images.githubusercontent.com/87288707/155395258-632c6132-cb67-43b9-9d6c-c7021bdd2b17.png)

To run a node, install the required packages (download requirements.txt), and run Flask (not in terminal!), and it should pop up with three genesis trasactions.
To add new transactions, head to: `127.0.0.1:5000/transactions/new`
To access wallet or make a new wallet, head to: `127.0.0.1:5000/wallet`
To check network stats, head to: `127.0.0.1:5000/stats`
To check node status, head to: `127.0.0.1:5000/node`

You can replace `127.0.0.1:5000` with a new IP:Port pair

If you find any bugs, or anything that should be added, please add them or send me an email at `naisukhy@gmail.com`
