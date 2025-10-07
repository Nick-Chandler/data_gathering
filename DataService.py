from abc import ABC, abstractmethod
from solana.rpc.api import AsyncClient
from pump_swap_api import fetch_pool, fetch_pool_base_price

class DataService(ABC):
  @abstractmethod
  def get_pool_data(self):
    pass

class PumpSwapDataService(DataService):
  def __init__(self, rpc_url: str, sol_usd: float = 150.0):
    self.rpc_url = rpc_url
    self.sol_usd = sol_usd

  async def get_pool_data(self, pool_addr: str):
    async with AsyncClient(self.rpc_url) as c:
      pool_keys = await fetch_pool(pool_addr, c)
      base_price_sol, base_bal_tokens, quote_bal_sol = await fetch_pool_base_price(pool_keys, c)
      base_dec = 6  # adjust if needed based on mint metadata

      price_sol = float(base_price_sol)
      price_usd = price_sol * self.sol_usd
      liquidity_usd = (
        (base_bal_tokens / 10**base_dec) * price_usd +
        float(quote_bal_sol) * self.sol_usd
      )

      return {
        "pool": pool_addr,
        "base_mint": pool_keys["base_mint"],
        "quote_mint": pool_keys["quote_mint"],
        "price_sol": price_sol,
        "price_usd": price_usd,
        "liquidity_usd": liquidity_usd
      }