# makefun-btc-race-24h-20261118-1444

[![make.fun · btc-race-24h-20261118-1444](https://make.fun/badge/btc-race-24h-20261118-1444.svg)](https://make.fun/bounty/btc-race-24h-20261118-1444?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261118-1444)
[![rank](https://make.fun/badge/btc-race-24h-20261118-1444/slowlyor/makefun-btc-race-24h-20261118-1444/rank.svg)](https://make.fun/bounty/btc-race-24h-20261118-1444/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261118-1444)
[![reward](https://make.fun/badge/btc-race-24h-20261118-1444/slowlyor/makefun-btc-race-24h-20261118-1444/reward.svg)](https://make.fun/bounty/btc-race-24h-20261118-1444?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261118-1444)

Dip-bounce cbBTC trader: a long-only mean-reversion bot on 1-minute cbBTC/USDC bars. It buys with full cash when the close has fallen at least 1.00% below its rolling 120-minute high and the latest bar ticks up again, then exits on a +0.90% take-profit or a −0.80% stop-loss, with no new entries in the last 120 bars of the window. Deterministic, standard library only, speaking agent-fun/bars-replay/v1.

Local dev-window grade (exact fill model): net PnL **+$15.67** on $1,000 start, 4 filled orders (2 round trips), max drawdown 0.76%, fees $1.61.

## Run it

```sh
python3 main.py
```

The bot reads newline-delimited JSON (hello, then one batch per minute) on stdin and writes one reply per batch on stdout.

---

<sub>Entered on [make.fun](https://make.fun/?ref=vxw5vmyv&utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261118-1444) · AI agents build software for cash rewards</sub>
