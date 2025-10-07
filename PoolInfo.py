from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from pathlib import Path

class RawTokenAmount(BaseModel):
  decimals: int
  tokenAmount: str

class TokenBalanceChange(BaseModel):
  mint: str
  rawTokenAmount: RawTokenAmount
  tokenAccount: str
  userAccount: str

class AccountDataEntry(BaseModel):
  account: str
  nativeBalanceChange: int
  tokenBalanceChanges: List[TokenBalanceChange]

class InnerInstruction(BaseModel):
  accounts: List[str]
  data: str
  programId: str

class Instruction(BaseModel):
  accounts: List[str]
  data: str
  innerInstructions: List[InnerInstruction]
  programId: str

class NativeTransfer(BaseModel):
  amount: int
  fromUserAccount: str
  toUserAccount: str

class TokenTransfer(BaseModel):
  fromTokenAccount: str
  fromUserAccount: str
  mint: str
  toTokenAccount: str
  toUserAccount: str
  tokenAmount: float
  tokenStandard: str

class PoolInfo(BaseModel):
  accountData: List[AccountDataEntry]
  description: str
  events: Dict[str, Any]
  fee: int
  feePayer: str
  instructions: List[Instruction]
  nativeTransfers: List[NativeTransfer]
  signature: str
  slot: int
  source: str
  timestamp: int
  tokenTransfers: List[TokenTransfer]
  transactionError: Optional[Dict[str, Any]] = None
  type: str


  def dump_to_file(self, filepath: str | Path = "data/webhooks/ps_webhooks.jsonl") -> None:
    # Get the directory of this file and construct absolute path
    current_dir = Path(__file__).parent
    path = current_dir / filepath
    with path.open("a", encoding="utf-8") as f:
      f.write(self.model_dump_json() + "\n")