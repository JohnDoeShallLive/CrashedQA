def partial_refund(amount: float, percentage: float) -> float:
    """
    Calculates a partial refund.
    Intentionally uses float arithmetic instead of Decimal to produce off-by-one cent errors
    on specific amounts, representing a legacy rounding bug.
    """
    # BUG: Float arithmetic on large values can lead to precision errors.
    # Example: 1000.01 * 0.1 should be 100.001 (rounded to 100.00)
    # but float might return 100.00100000000001
    refund = amount * percentage
    return refund

def get_balance(user_id: str) -> float:
    # Mock balance
    return 5000.0
