# Lixur

![Screenshot 2021-11-18 192213ccc](https://user-images.githubusercontent.com/87288707/155904619-8dca0af8-4e9f-433f-8c2e-60e7b0e97a64.jpg)

![image](https://user-images.githubusercontent.com/87288707/155904797-03df3651-ea9d-40e9-9998-14726876519b.png) 
![image](https://img.shields.io/badge/server-online-success) 
![image](https://img.shields.io/badge/version-0.0.1-blueviolet)
![image](https://img.shields.io/badge/type-Testnet%20Beta-informational)


### What is Lixur ?
Welcome, we're glad to have you! Lixur is an open-sourced project building a distributed ledger platform. Lixur plans on implementing things such as DAGs and A.I smart contracts which enables fast, privacy-preserving, feeless, infinitely scalable, quantum resistant and an interconnected ecosystem, which users can make use of for any application requiring decentralized, automated intelligence and more. To learn more, please read the whitepaper [ 📖 Here 📖](https://github.com/LixurProtocol/Lixur-Protocol/wiki/Lixur-Whitepaper-1.8.6)

### The Testnet Beta is finally released!: 
After around six months (November 2nd, 2022 to May 5th, 2022), we've finally been able to release the Testnet Beta! This project is by no means complete and may feature plenty of bugs, security holes, etc. Please be aware of this. This is the Testnet Beta of course!

### How to Run:
Step 1. Disable your anti-virus so it doesn't interfere with your code.

Step 2. Download the executable file here: [Download Lixur Client](https://drive.google.com/file/d/11U0ye49QJn9fbxKf0jTkZW3lR8i8ZVN6/view?usp=sharing)

Step 3. Download a JSON Viewer and make sure it's on. If you are using Firefox, skip. [Download JSON Viewer for Chrome](https://bit.ly/3MUUISo)

Step 4. Unzip the 'lixur_client.zip' file and launch 'run.exe'.

Step 5. It should say "You have connected to the server successfully!" on the screen, if not, The server is down or a connection failure occured, if so, try executing the file again.

Step 6. Type the following address in your browser: "127.0.0.1:5000", this may give an error the first time you attempt to do it but keep refreshing, it should eventually work, and there you go, you're in! Since it's a Testnet, the coins are worthless. Every new user starts off with 69,420,000 LXR!

### Testnet Navigation Help, Tips and Notes:
1. 127.0.0.1:5000/ - Displays the graph/blockchain.
2. 127.0.0.1:5000/stats - Displays statistics for the graph/blockchain.
3. 127.0.0.1:5000/wallet/new - Generates a new wallet (keystore and phrase) - "WARNING! You'll overwrite your phrase and keystore files in your "/user" folder if you have one already, which will make you permanently lose access to your funds!"
4. 127.0.0.1:5000/wallet/load - Loads up the existing wallet stored on the device. You'll need to generate a wallet (keystore and phrase) file first before accessing this page.
5. 127.0.0.1:5000/transaction - Used for sending transactions to other addresses on the network.

Refresh, refresh, refresh! It solves a lot of problems if you are encountering "Internal Server Errors". 99% of the time, it's that the sats hasn't arrived to show you yet so it can't present it to you! Also, make sure your terminal, the .exe file is open so you can see the errors popping up, etc.

If your balance ever doesn't work correctly, or if anything doesn't work correctly, refreshing the graph or the page almost always helps.
If refreshing doesn't work, any other errors you encounter, please email me at "naisukhy@gmail.com" or submit the issue on the repository page here with a picture, exact time with the time zone and describe the error as precisely as possible.

Your keystore and phrase file is what allows you to access your wallet, if you ever delete it, you're basically deleting your access to your funds permanently! If you want to have multiple wallets, after generating a wallet, move your keystore and phrase out of it's original directory and make a new one, if you ever want to boot your old one again, get your old keystore and phrase and put it in the "/user" directory.

When sending a transaction, make sure you enter the exact address and amount, if not, you'll have to do it over and over again until it works.

### How to Contribute

So you want to contribute? Please, please join our Discord Server and our JetBrains Space Collaboration Platform if you want to contribute to this project. It's a must. Our project management and our project checklist is avaiable on JetBrains and our primary source of communication is Discord, it only takes a minute at most to signup! Open issues or contact us on Discord/JetBrains for things you want to see added, modified, discuss ideas or help out with existing issues. If you have any questions, please contact me on Jetbrains, Discord or if those aren't possible, my email which is `naisukhy@gmail.com` Currently, we're primarily interested in frontend developers and people who are good at distributed computing.

<br> [Click here to join our Official Discord Server Link](https://discord.gg/HCRAQHKGeG)
<br> [Click here to join our Official Jetbrains Space Group Link](https://lixur.jetbrains.space/oauth/auth/invite/4bf814e7091de971b3c9fde59b99eb63)

You could also submit a pull request (fork the code first) and introduce yourself, why you're interested in this project and promise us you'll join the Jetbrains and the Discord Servers. We need to keep in touch with all of our developers.

***If you find any bugs, or anything that should be added, initiate a pull request, add the issue to the repository page or email me personally at:*** `naisukhy@gmail.com`

---

``Addressing a potential concern: For those examining the code and are concerned with the speed of Python, This code will soon feature a JIT Complier that will accelerate the code either with Numba, accelerating execution speed on par or even better than Go, C++ or Julia. Solving the speed dilemma. Here are some examples to illustrate this...``

<br> ![image](https://user-images.githubusercontent.com/87288707/155394541-28719860-ac4e-4db8-97d4-c7c2980cb273.png)
<br> ![image](https://user-images.githubusercontent.com/87288707/155394794-6cd735c6-93ea-41fc-abb3-844f90c60162.png)
<br> ![image](https://user-images.githubusercontent.com/87288707/155395059-717c2782-cd2c-4974-bcc5-7c718c9a4561.png)
<br> ![image](https://user-images.githubusercontent.com/87288707/155395258-632c6132-cb67-43b9-9d6c-c7021bdd2b17.png)

#### Other Links
* https://users.rust-lang.org/t/why-my-rust-code-is-10-times-slower-than-python-with-numba/57738
