from data_gathering.Pool import Pool
class PoolTracker:
  def __init__(self, pool: Pool):
    self.pool = pool
    self.sol_price = 200
    self.data = []

  def track_token(self):
    p = self.pool
    p.record_initial_data()
    while p.status == "live":  
      self.data.append(p.get_data())
    p.generate_summary()
    pass
  
