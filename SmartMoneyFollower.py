from datetime import datetime
from tabulate import tabulate
from client import gmgn
import logging
import time


class SmartMoneyFollower:
    def __init__(self):
        self.gmgn = gmgn()
        self.logger = logging.getLogger("SmartMoneyFollower")
        logging.basicConfig(level=logging.INFO)

    def get_top_wallets(self, timeframe="7d", walletTag="smart_degen"):
        """
        Fetch top performing wallets using the getTrendingWallets endpoint.

        :param timeframe: Time period for trending wallets (default "7d").
        :param walletTag: Tag to filter wallets (default "smart_degen").
        :return: List of top performing wallets.
        """
        try:
            response = self.gmgn.getTrendingWallets(timeframe, walletTag)
            return response['rank']
        except Exception as e:
            self.logger.error(f"Error fetching top wallets: {e}")
            return []

    def analyze_wallet_activity(self, wallet_address, period="7d"):
        """
        Analyze recent trading activity of a wallet using the getWalletInfo endpoint.

        :param wallet_address: Address of the wallet to analyze.
        :param period: Time period for wallet analysis (default "7d").
        :return: Wallet activity data.
        """
        try:
            response = self.gmgn.getWalletInfo(walletAddress=wallet_address, period=period)
            return response
        except Exception as e:
            self.logger.error(f"Error analyzing wallet activity: {e}")
            return {}

    def evaluate_token(self, token_address):
        """
        Evaluate a token using the getTokenInfo and getTokenUsdPrice endpoints.

        :param token_address: Address of the token to evaluate.
        :return: Token information and USD price.
        """
        try:
            token_info = self.gmgn.getTokenInfo(contractAddress=token_address)
            token_price = self.gmgn.getTokenUsdPrice(contractAddress=token_address)
            return token_info, token_price
        except Exception as e:
            self.logger.error(f"Error evaluating token: {e}")
            return {}, {}
        
    def get_wallet_activity(self, wallet_address, period="7d"):
        try:
            response = self.gmgn.getWallet_activity(wallet_address, 10,10)
            return response
        except Exception as e:
            self.logger.error(f"Error analyzing wallet activity: {e}")
            return []    

    def print_analysis_output(self, wallets):
        """
        Print the analysis output in a tabulated format.

        :param wallets: List of wallets to print.
        """
        headers = ["Rank", "Wallet Address", "Realized Profit (SOL or USD)", "Buy Transactions", "Sell Transactions", "Last Active"]
        table_data = []

        for idx, wallet in enumerate(wallets):
            # last_active = datetime.utcfromtimestamp(wallet.get('last_active_timestamp', 0)).strftime('%Y-%m-%d %H:%M:%S')
            last_active = datetime.fromtimestamp(wallet.get('last_active_timestamp', 0))
            table_data.append([
                idx + 1,
                wallet.get('wallet_address', 'N/A'),
                wallet.get('realized_profit', 'N/A'),
                wallet.get('buy', 'N/A'),
                wallet.get('sell', 'N/A'),
                last_active 
            ])

        print(tabulate(table_data, headers=headers, tablefmt="pretty"))
        print("Note: The 'Realized Profit' is represented in SOL.")

    def print_activity_output(self, wallets):
        """
        Print the analysis output in a tabulated format.

        :param wallets: List of wallets to print.
        """
        headers = ["Wallet Address", "token_address", "event_type", "last_active_timestamp"]
        table_data = []

        for idx, wallet in enumerate(wallets):
            last_active = datetime.fromtimestamp(wallet.get('last_active_timestamp', 0))
            table_data.append([
                idx + 1,
                wallet.get('wallet_address', 'N/A'),
                wallet.get('token_address', 'N/A'),
                wallet.get('event_type', 'N/A'),
                wallet.get('last_active_timestamp', 'N/A'),
                last_active 
            ])

        print(tabulate(table_data, headers=headers, tablefmt="pretty"))


    def run_strategy(self):
        """
        Orchestrate the overall strategy execution.
        """
        try:
            # Step 1: Get top wallets
            top_wallets = self.get_top_wallets()
            if not top_wallets:
                self.logger.warning("No top wallets found.")
                return

            wallet_data = []
            wallet_activities = []

            # Step 2: Analyze each wallet's activity
            for wallet in top_wallets:
                wallet_address = wallet.get('wallet_address')
                wallet_activity = self.analyze_wallet_activity(wallet_address)
                wallet_now_activity = self.get_wallet_activity(wallet_address)
                
                # Log wallet activity data vertically
                # self.logger.info(f"Wallet Activity for {wallet_address}:")
                # for key, value in wallet_activity.items():
                #     self.logger.info(f"{key}: {value}")

                # Filter wallets with a win rate higher than 0.6
                winrate = wallet_activity.get('winrate', 0)
                if winrate is not None and winrate > 0.6:
                    wallet_info = {
                        'wallet_address': wallet_address,
                        'realized_profit': wallet_activity.get('realized_profit', 0.0),
                        'buy': wallet_activity.get('buy', 'N/A'),
                        'sell': wallet_activity.get('sell', 'N/A'),
                        'last_active_timestamp': wallet_activity.get('last_active_timestamp', 0)
                    }

                    wallet_data.append(wallet_info)
                    wallet_data.sort(key=lambda element: element['realized_profit'])

                    time.sleep(1)  # Rate limiting

            # Step 4: Print the analysis output
            self.print_analysis_output(wallet_data)
        except Exception as e:
            self.logger.error(f"Error running strategy: {e}")


if __name__ == "__main__":
    follower = SmartMoneyFollower()
    follower.run_strategy()