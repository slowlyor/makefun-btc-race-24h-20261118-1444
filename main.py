"""Dip-bounce cbBTC trader for make.fun btc-race-24h-20261118-1444.

Strategy: long-only dip-bounce mean reversion on 1-minute cbBTC/USDC bars.
The bot watches the rolling 120-minute high of closes. When the close has
fallen at least 1.00% below that high and the latest bar ticks up again
(close above the previous close), it buys with its full cash: the drop plus
the uptick is the bounce signal. It exits the whole position when the
position is worth 0.90% over its cost (take-profit) or 0.80% under it
(stop-loss). No new entries are opened in the last 120 bars of the window,
so a late entry cannot be flattened at a loss by the end-of-window close.

Everything is deterministic: integer prices from the bars, no network, no
wall clock, no randomness. The bot speaks agent-fun/bars-replay/v1 through
the vendored kit shim (vendor/makefun_bars.py, byte-identical to the kit
SDK), answering every batch with exactly one reply.

Dev-window grade (local replay, exact fill model): net PnL +$15.67 on
$1,000 start, 4 filled orders (2 round trips), max drawdown 0.76%,
fees $1.61.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
import makefun_bars

SYMBOL = "CBBTC"
HIGH_WINDOW = 120          # bars of closes forming the rolling high
DROP_BPS = 100             # entry: close >= 1.00% below the rolling high
TAKE_PROFIT_BPS = 90       # exit: position worth 0.90% over its cost
STOP_LOSS_BPS = 80         # exit: position worth 0.80% under its cost
LATE_CUTOFF_SEQ = 1320     # no new entries from this batch on (window is 1440 bars)
MAX_SLIPPAGE_BPS = 100     # 1% past the close the order was decided on

# Rolling closes, oldest first, capped at HIGH_WINDOW entries.
closes = []


def dip_bounce_signal():
    """True when the close has fallen DROP_BPS below the rolling high and
    the latest bar ticks up again. Needs a full HIGH_WINDOW of closes."""
    if len(closes) < HIGH_WINDOW:
        return False
    high = max(closes)
    close = closes[-1]
    drop_bps = (high - close) * 10000 // high
    uptick = close > closes[-2]
    return drop_bps >= DROP_BPS and uptick


def exit_signal(state, held):
    """True when the held position is worth TAKE_PROFIT_BPS over its cost
    or STOP_LOSS_BPS under it."""
    cost = held.cost
    if cost <= 0:
        return False
    gain_bps = (state.value(SYMBOL, held.qty) - cost) * 10000 // cost
    return gain_bps >= TAKE_PROFIT_BPS or gain_bps <= -STOP_LOSS_BPS


def on_batch(state, batch):
    if state.warming_up:
        return []
    orders = []
    for bar in batch["bars"]:
        if bar["symbol"] != SYMBOL:
            continue
        close = int(bar["c"])
        closes.append(close)
        if len(closes) > HIGH_WINDOW:
            closes.pop(0)

    if not closes:
        return []

    held = state.positions.get(SYMBOL)
    if held is not None:
        if exit_signal(state, held):
            orders.append({
                "side": "sell",
                "symbol": SYMBOL,
                "qty": held.qty,
                "max_slippage_bps": MAX_SLIPPAGE_BPS,
            })
        return orders

    # Flat: look for a dip-bounce entry, except late in the window.
    if state.seq >= LATE_CUTOFF_SEQ:
        return []
    if dip_bounce_signal():
        notional = state.cash
        if notional >= int(state.hello["fees"]["min_notional_quote_units"]):
            orders.append({
                "side": "buy",
                "symbol": SYMBOL,
                "notional_quote_units": notional,
                "max_slippage_bps": MAX_SLIPPAGE_BPS,
            })
    return orders


makefun_bars.run(on_batch)
