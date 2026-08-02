"""Domain entities. No pandas, no SQL, no I/O — just the business shape of a transaction."""

from dataclasses import dataclass
from enum import Enum


class TransactionType(str, Enum):
    CASH_IN = "CASH_IN"
    CASH_OUT = "CASH_OUT"
    DEBIT = "DEBIT"
    PAYMENT = "PAYMENT"
    TRANSFER = "TRANSFER"


@dataclass(frozen=True)
class Transaction:
    step: int  # 1 hour per step, simulating 30 days
    type: TransactionType
    amount: float
    origin_account: str
    origin_balance_before: float
    origin_balance_after: float
    dest_account: str
    dest_balance_before: float
    dest_balance_after: float
    is_fraud: bool
    is_flagged_fraud: bool

    @property
    def origin_balance_delta(self) -> float:
        return self.origin_balance_after - self.origin_balance_before

    @property
    def balance_mismatch(self) -> bool:
        """True when the reported balances don't reconcile with the amount moved —
        a cheap, high-signal anomaly flag used constantly in the SQL/EDA layers."""
        expected_after = self.origin_balance_before - self.amount
        return abs(expected_after - self.origin_balance_after) > 0.01
