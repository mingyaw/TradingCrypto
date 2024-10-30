import requests
import random

class gmgn:
    BASE_URL = "https://gmgn.ai/defi/quotation"

    user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Linux; Android 10; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 8.0.0; Nexus 5X Build/OPR6.170623.013) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.99 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/89.0"
        ]
    
    # proxies = {'http': 'http://1.1.1.99:80', 'https': 'https://131.196.114.9:6969'}
    
    def __init__(self):
        headers = random.choice(self.user_agents)
        self.headers = {
                "Accept":"application/json, text/plain, */*",
                "User-Agent": headers,
                "Referer": 'https://gmgn.ai/discover/H8iNB0SJ?chain=sol',
                "If-Modified-Since": 'W/"30aa3-y1nrWBj0XQhBl4P1FjKfAK8WlbM"',
                # "Cookie": '_ga=GA1.1.379394457.1729492141; __cf_bm=X9zbjtFgUTiRLHAmCf7cwKe2f3vS6po5gC5QB7UYchs-1730100854-1.0.1.1-AYYoLcmoD3I6czo0xS0mRDkJ03ipOzO7iGUHnjU3Cut1qhrqXGrU0do7EtGa53A_1mjqYVQsgQ3O8hFgmm_N7g; cf_clearance=I4S5RkYRn52znqTd1AAORaSbnolQab.aLkECY0a0jKk-1730101048-1.2.1.1-whunhnRCo35jsK.ZUev3wjBEAMkF2h66M6kNcNPB3_R.K_A_GGv4nLh.ytA1I6nUmKKpU7X8.4qqtwEXDLBVTa6CIswc2gSbxjiQaz1H40Fr.vBNUuOf98NMmFuOxbsKi11OF9_ylpgKi2BT2efm19bNXbs2dYVBpqAaz2DCaGhpfd2NTGaS.bCDSU_6G9QDFSLjFSJCagUAyF01Dnj2puo9A5bsPMTBvZTY.53oLyefpefRAPSQc6XVC8O9JQ3lvk.uolsLSwMR2eYdFJs4zUy3lvJWOWft7GAhRwI6xSC396PLHtBsV1lbFsx1xSdFmH7iA9Bh7WOFESd6FAEnN.C20H5WpZSngligO1Zp.YamHYmGSB2K68fBjGU4q0nS1kG2RTELGHj6l_82flk7tNPzNlj8Rbqtvfq3o.dviVuKvehUGCBSPgWRsMYcD8Ag; _ga_0XM0LYXGC8=GS1.1.1730101047.8.1.1730101056.0.0.0'
            }
        print(self.headers)

    def getTokenInfo(self, contractAddress: str) -> dict:
        """
        Gets info on a token.
        """
        if not contractAddress:
            return "You must input a contract address."
        url = f"{self.BASE_URL}/v1/tokens/sol/{contractAddress}"
        jsonResponse = requests.get(url, headers=self.headers).json()['data']['token']

        return jsonResponse
    
    def getNewPairs(self, limit: int = None) -> dict:
        """
        Limit - Limits how many tokens are in the response.
        """
        if not limit:
            limit = 50
        elif limit > 50:
            return "You cannot have more than check more than 50 pairs."
        
        url = f"{self.BASE_URL}/v1/pairs/sol/new_pairs?limit={limit}&orderby=open_timestamp&direction=desc&filters[]=not_honeypot"

        jsonResponse = requests.get(url, headers=self.headers).json()['data']

        return jsonResponse
    
    def getTrendingWallets(self, timeframe: str = None, walletTag: str = None) -> dict:
        """
        Gets a list of trending wallets based on a timeframe and a wallet tag.

        Timeframes\n
        1d = 1 Day\n
        7d = 7 Days\n
        30d = 30 days\n

        ----------------

        Wallet Tags\n
        pump_smart = Pump.Fun Smart Money\n
        smart_degen = Smart Money\n
        reowned = KOL/VC/Influencer\n
        snipe_bot = Snipe Bot\n

        """
        if not timeframe:
            timeframe = "7d"
        if not walletTag:
            walletTag = "smart_degen"
        
        url = f"{self.BASE_URL}/v1/rank/sol/wallets/{timeframe}?tag={walletTag}&orderby=pnl_{timeframe}&direction=desc"
        jsonResponse = requests.get(url, headers=self.headers).json()['data']
        return jsonResponse
    
    def getTrendingTokens(self, timeframe: str = None) -> dict:
        """
        Gets a list of trending tokens based on a timeframe.

        Timeframes\n
        1m = 1 Minute\n
        5m = 5 Minutes\n
        1h = 1 Hour\n
        6h = 6 Hours\n
        24h = 24 Hours\n
        """
        timeframes = ["1m", "5m", "1h", "6h", "24h"]
        if timeframe not in timeframes:
            return "Not a valid timeframe."

        if not timeframe:
            timeframe = "1h"

        if timeframe == "1m":
            url = f"{self.BASE_URL}/v1/rank/sol/swaps/{timeframe}?orderby=swaps&direction=desc&limit=20"
        else:
            url = f"{self.BASE_URL}/v1/rank/sol/swaps/{timeframe}?orderby=swaps&direction=desc"
        
        jsonResponse = requests.get(url, headers=self.headers).json()['data']

        return jsonResponse

    def getTokensByCompletion(self, limit: int = None) -> dict:
        """
        Gets tokens by their bonding curve completion progress.\n

        Limit - Limits how many tokens in the response.
        """

        if not limit:
            limit = 50
        elif limit > 50:
            return "Limit cannot be above 50."

        url = f"{self.BASE_URL}/v1/rank/sol/pump?limit={limit}&orderby=progress&direction=desc&pump=true"

        jsonResponse = requests.get(url, headers=self.headers).json()['data']

        return jsonResponse
    
    def findSnipedTokens(self, size: int = None) -> dict:
        """
        Gets a list of tokens that have been sniped.\n

        Size - The amount of tokens in the response
        """

        if not size:
            size = 10
        elif size > 39:
            return "Size cannot be more than 39"
        
        url = f"{self.BASE_URL}/v1/signals/sol/snipe_new?size={size}&is_show_alert=false&featured=false"

        jsonResponse = requests.get(url, headers=self.headers).json()['data']

        return jsonResponse
    
    def getGasFee(self):
        """
        Get the current gas fee price.
        """
        url = f"{self.BASE_URL}/v1/chains/sol/gas_price"
        jsonResponse = requests.get(url, headers=self.headers).json()['data']

        return jsonResponse
    
    def getTokenUsdPrice(self, contractAddress: str = None) -> dict:
        """
        Get the realtime USD price of the token.
        """
        if not contractAddress:
            return "You must input a contract address."
        
        url = f"{self.BASE_URL}/v1/sol/tokens/realtime_token_price?address={contractAddress}"

        jsonResponse = requests.get(url, headers=self.headers).json()['data']

        return jsonResponse

    def getTopBuyers(self, contractAddress: str = None) -> dict:
        """
        Get the top buyers of a token.
        """
        if not contractAddress:
            return "You must input a contract address."
        
        url = f"{self.BASE_URL}/v1/tokens/top_buyers/sol/{contractAddress}"

        jsonResponse = requests.get(url, headers=self.headers).json()['data']

        return jsonResponse

    def getSecurityInfo(self, contractAddress: str = None) -> dict:
        """
        Gets security info about the token.
        """
        if not contractAddress:
            return "You must input a contract address."
        
        url = f"{self.BASE_URL}/v1/tokens/security/sol/{contractAddress}"

        jsonResponse = requests.get(url, headers=self.headers).json()['data']

        return jsonResponse
    
    def getWalletInfo(self, walletAddress: str = None, period: str = None) -> dict:
        """
        Gets various information about a wallet address.

        Period - 7d, 30d - The timeframe of the wallet you're checking.
        """

        periods = ["7d", "30d"]

        if not walletAddress:
            return "You must input a wallet address."
        if not period or period not in periods:
            period = "7d"
        
        url = f"{self.BASE_URL}/v1/smartmoney/sol/walletNew/{walletAddress}?period={period}"

        jsonResponse = requests.get(url, headers=self.headers).json()['data']

        return jsonResponse
    
    def getWallet_activity(self, walletAddress: str = None, limit: str = None, cost: str = None) -> dict:

        url = f"{self.BASE_URL}/v1/wallet_activity/sol?type=buy&type=sell&wallet={walletAddress}&limit={limit}&cost={cost}"
        jsonResponse = requests.get(url, headers=self.headers).json()['data']
    
        return jsonResponse
    
    def getWallet_holdings(self, walletAddress: str = None) -> dict:

        url = f"https://gmgn.ai/api/v1/wallet_holdings/sol/{walletAddress}?limit=3&orderby=last_active_timestamp&direction=desc"
        jsonResponse = requests.get(url, headers=self.headers).json()['data']
    
        return jsonResponse
