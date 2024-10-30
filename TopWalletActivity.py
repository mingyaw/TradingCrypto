import asyncio
from client import gmgn
import logging
from tabulate import tabulate
from datetime import datetime
import threading
import random
import SwapTrading
from solders.keypair import Keypair
from config import MY_WALLET, PRIVATE_KEY
from solanatracker import SolanaTracker
import asyncio
import time

SOL = 0.08898  # 本金
WALLET_HOLDING = {}
SOL_ADDR = "So11111111111111111111111111111111111111112"


class TopWalletActivity:

    def __init__(self):
        self.gmgn = gmgn()
        self.logger = logging.getLogger("TopWalletActivity")
        logging.basicConfig(level=logging.INFO)

    def print_activity_output(self, wallets):
        """
        Print the analysis output in a tabulated format.

        :param wallets: List of wallets to print.
        """
        headers = ["token_name", "token_address", "event_type", "last_active_timestamp"]
        table_data = []

        for idx, wallet in enumerate(wallets):
            last_active = datetime.fromtimestamp(wallet.get("last_active_timestamp", 0))
            table_data.append(
                [
                    idx + 1,
                    wallet.get("token_name", "N/A"),
                    wallet.get("token_address", "N/A"),
                    wallet.get("event_type", "N/A"),
                    last_active,
                ]
            )

        print(tabulate(table_data, headers=headers, tablefmt="pretty"))

    def print_holding_output(self, wallets):
        """
        Print the analysis output in a tabulated format.

        :param wallets: List of wallets to print.
        """
        headers = [
            "token_name",
            "token_address",
            "event_type",
            "token_price",
            "amount",
            "last_active_timestamp",
        ]
        table_data = []

        for idx, wallet in enumerate(wallets):
            last_active = datetime.fromtimestamp(wallet.get("last_active_timestamp", 0))
            table_data.append(
                [
                    idx + 1,
                    wallet.get("token_name", "N/A"),
                    wallet.get("token_address", "N/A"),
                    wallet.get("event_type", "N/A"),
                    wallet.get("token_price", "N/A"),
                    wallet.get("amount", "N/A"),
                    last_active,
                ]
            )

        print(tabulate(table_data, headers=headers, tablefmt="pretty"))

    async def run_check(self):
        try:
            response = self.gmgn.getWallet_activity(self.WALLET_ADDRESS, 1, 1)
            activities = response["activities"]

            self.logger.info(f"Wallet Activity for {self.WALLET_ADDRESS}:")
            self.logger.info(f"Now Time for {datetime.now()}:")
            wallet_activities = []

            # 處理交易
            global SOL, WALLET_HOLDING, SOL_ADDR
            for trade in activities:
                token_address = trade.get("token_address")
                token_name = trade["token"]["name"]
                token_price = trade["token"]["price"]
                token_event_type = trade["event_type"]
                token_timestamp = trade["timestamp"]

                walletactivity = {
                    "token_name": token_name,
                    "token_address": token_address,
                    "event_type": token_event_type,
                    "last_active_timestamp": token_timestamp,
                }
                wallet_activities.append(walletactivity)

                if token_event_type == "buy":
                    await self.handle_buy(
                        token_address, token_name, token_price, token_timestamp
                    )
                elif token_event_type == "sell":
                    await self.handle_sell(token_address, token_price, token_timestamp)

            # 輸出結果
            self.print_activity_output(wallet_activities)
            self.print_holding_output(list(WALLET_HOLDING.values()))
            # print(f"SOL : {SOL}")

        except Exception as e:
            self.logger.error(f"Error fetching top wallets: {e}")
            return []

    async def handle_buy(self, token_address, token_name, token_price, token_timestamp):
        if token_address not in WALLET_HOLDING:
            amount = 0.03 / token_price
            WALLET_HOLDING[token_address] = {
                "token_address": token_address,
                "token_name": token_name,
                "event_type": "buy",
                "token_price": token_price,
                "amount": amount,
                "last_active_timestamp": token_timestamp,
            }
            # global SOL
            # SOL -= 0.02
            await swap(SOL_ADDR, token_address, 0.1)

    async def handle_sell(self, token_address, token_price, token_timestamp):
        if token_address in WALLET_HOLDING:
            if token_timestamp > WALLET_HOLDING[token_address]["last_active_timestamp"]:
                
                response = self.gmgn.getWallet_holdings(MY_WALLET)
                holdings = response["holdings"]
                for holding in holdings:
                    
                    if holding["token"]['token_address'] == token_address:
                        # sell_value = token_price * holding["balance"]
                        await swap(token_address, SOL_ADDR, holding["balance"])

                # global SOL
                # SOL += sell_value
                del WALLET_HOLDING[token_address]


async def repeat_function():
    twa = TopWalletActivity()
    while True:
        await twa.run_check()
        await asyncio.sleep(random.randint(5, 20))
    # threading.Timer(random.randrange(10,30), repeat_function).start()


async def swap(fromToken, ToToken, amout):

    API_HOST = "https://rpc.solanatracker.io/public?advancedTx=true"
    
    start_time = time.time()

    keypair = Keypair.from_base58_string(
        PRIVATE_KEY
    )  # Replace with your base58 private key

    solana_tracker = SolanaTracker(keypair, API_HOST)

    swap_response = await solana_tracker.get_swap_instructions(
        fromToken,  # From Token
        ToToken,  # To Token
        amout,  # Amount to swap
        30,  # Slippage
        str(keypair.pubkey()),  # Payer public key
        0.0005,  # Priority fee (Recommended while network is congested)
    )

    # Define custom options
    custom_options = {
        "send_options": {"skip_preflight": True, "max_retries": 5},
        "confirmation_retries": 50,
        "confirmation_retry_timeout": 1000,
        "last_valid_block_height_buffer": 200,
        "commitment": "processed",
        "resend_interval": 1500,
        "confirmation_check_interval": 100,
        "skip_confirmation_check": False,
    }

    try:
        send_time = time.time()
        txid = await solana_tracker.perform_swap(swap_response, options=custom_options)
        end_time = time.time()
        elapsed_time = end_time - start_time

        print("Transaction ID:", txid)
        print("Transaction URL:", f"https://solscan.io/tx/{txid}")
        print(f"Swap completed in {elapsed_time:.2f} seconds")
        print(f"Transaction finished in {end_time - send_time:.2f} seconds")
    except Exception as e:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Swap failed:", str(e))
        print(f"Time elapsed before failure: {elapsed_time:.2f} seconds")
        # Add retries or additional error handling as needed


if __name__ == "__main__":
    asyncio.run(repeat_function())
