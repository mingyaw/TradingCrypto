# TradingCrypto

TradingCrypto is a Python-based project designed for automated trading by following smart money. This repository implements strategies to track and follow the trades of successful investors to optimize trading decisions.

## Prerequisites
- Python 3.x
- Dependencies:
  - `httpx`
  - `tabulate`
  - `gmgn`
  - `logging`
  - `solanatracker`
    
## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/mingyaw/TradingCrypto.git
    cd TradingCrypto
    ```
2. Install the required packages:
    ```bash
    pip install httpx tabulate solana base58 requests aiohttp
    ```

## Usage
1. Configure your trading parameters in the `config.py` file.
2. Run the script to search gmgn smart money wallet:
    ```bash
    python smart_money_follower.py
    ```
3. Run the main script to start automated trading:
   ```bash
    python TopWalletActivity.py
    ```
   
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
