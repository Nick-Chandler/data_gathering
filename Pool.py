class Pool:
  def __init__(self, payload, price_lookup):
    self.payload = payload
    self.base_mint = payload["baseMint"]
    self.quote_mint = payload["quoteMint"]
    self.base_dec = payload.get("baseDecimals", 0)
    self.quote_dec = payload.get("quoteDecimals", 0)
    self.base_amt = int(payload["baseVaultAmount"])
    self.quote_amt = int(payload["quoteVaultAmount"])
    self.timestamp = payload["timestamp"]
    self.pool_id = payload.get("poolAddress")

    base_price = price_lookup(self.base_mint, self.timestamp)
    quote_price = price_lookup(self.quote_mint, self.timestamp)

    self.base_usd = self._to_usd(self.base_amt, self.base_dec, base_price)
    self.quote_usd = self._to_usd(self.quote_amt, self.quote_dec, quote_price)
    self.liquidity_usd = self.base_usd + self.quote_usd
    self.liquidity_depth_min_usd = min(self.base_usd, self.quote_usd)
    self.initial_price = self._calc_initial_price()

  def _to_usd(self, amount, decimals, price_usd):
    return (amount / (10 ** decimals)) * price_usd

  def _calc_initial_price(self):
    if self.base_amt == 0:
      return None
    base_norm = self.base_amt / (10 ** self.base_dec)
    quote_norm = self.quote_amt / (10 ** self.quote_dec)
    return quote_norm / base_norm

  def summary(self):
    return {
      "pool_id": self.pool_id,
      "liquidity_usd": self.liquidity_usd,
      "initial_price": self.initial_price,
      "base_usd": self.base_usd,
      "quote_usd": self.quote_usd,
      "liquidity_depth_min_usd": self.liquidity_depth_min_usd
    }


  