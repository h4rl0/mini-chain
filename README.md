# Mini Chain

A small, educational blockchain written in Python and Flask: hash-linked blocks, proof-of-work mining, a REST API, multi-node consensus and a browser dashboard.

> **Educational project.** This is a learning tool and is not secure. See [Limitations](#limitations).

## Features

- Blocks linked by SHA-256 hashes, so editing history is detectable
- Proof-of-work mining with adjustable difficulty
- Transaction pool and mining reward
- Multi-node consensus using the longest-valid-chain rule
- Browser dashboard (`index.html`) with a visual chain, hash tooltips and a tamper simulator

## Quick start

Requires Python 3.10 or newer.

```
git clone https://github.com/h4rl0/mini-chain.git
cd mini-chain
python -m venv .venv
```

Activate the virtual environment.

Windows (PowerShell):

```
.venv\Scripts\Activate.ps1
```

Mac / Linux:

```
source .venv/bin/activate
```

Install the dependencies and start a node:

```
python -m pip install -r requirements.txt
python blockchain.py
```

The node runs at http://127.0.0.1:5000 and serves a JSON API (see [API](#api)). If port 5000 is taken, run `python blockchain.py -p 5050` instead.

## Web dashboard

`index.html` is a standalone page that talks to a running node. There is nothing extra to install.

1. Start a node as above (`python blockchain.py`).
2. Open `index.html` in your browser by double-clicking it.
   - If your browser blocks it, run `python -m http.server 8080` in the project folder and open http://127.0.0.1:8080/index.html.
3. Check the two settings at the top of the page:
   - **Node**: the address of your node. The default is `http://127.0.0.1:5000`. Change it if you used `-p`.
   - **Difficulty**: must match `DIFFICULTY` in `blockchain.py` (default 4), because the node doesn't expose it. If it's wrong, valid blocks will show as broken.

Both settings are remembered in your browser.

### What you can do

- **Hover a block** to see its full hash, with the proof-of-work zeros highlighted. Click it to inspect its transactions, and click a hash to copy it.
- **Mine** a block to seal the pending transactions and earn the 1-coin reward.
- **Send a transaction.** Coins only exist from mining rewards, so mine first, then click *Send from this node*.
- **Tamper simulator**: edits an in-memory copy of the chain to show how changing one block breaks every later link. Your real node is never modified.
- **Network**: add a peer and press *Resolve conflicts* to adopt the longest valid chain.

### Try two nodes

```
python blockchain.py -p 5001
```

1. In the dashboard for the node on port 5000, add `http://127.0.0.1:5001` as a peer.
2. Change the **Node** field to `http://127.0.0.1:5001` and mine a few blocks.
3. Change it back to `http://127.0.0.1:5000` and press **Resolve conflicts**. The longer chain wins.

### Notes

- The dashboard needs CORS enabled on the node, otherwise the browser blocks its requests. `blockchain.py` enables it with `CORS(app)` from `flask-cors`, which is listed in `requirements.txt`.
- Block hashes are computed in the browser using the same rules as the Python code (`json.dumps(block, sort_keys=True)` then SHA-256).
- The node has no endpoint for listing pending transactions or peers, so those panels only show what was added from the page you have open.

## API

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/chain` | Full chain and its length |
| POST | `/transactions/new` | Add a transaction (`sender`, `recipient`, `amount`) |
| GET | `/mine` | Mine a block from the pending transactions |
| POST | `/nodes/register` | Register peers (`{"nodes": ["http://127.0.0.1:5001"]}`) |
| GET | `/nodes/resolve` | Replace this chain with the longest valid one from peers |

## Limitations

- Not secure. It exists to teach mechanics
- Anyone can submit a transaction as anyone
- No double-spend protection (the dashboard's balance check runs in the browser and is not a security feature)
- No authentication
- In-memory only: restarting the node resets the chain

## Acknowledgements

The structure follows Daniel van Flymen's tutorial "Learn Blockchains by Building One" (HackerNoon, 2017). This version was rewritten for current Python and Flask, with a different proof-of-work design and full chain validation.

The web dashboard (`index.html`) was designed and written with [Claude](https://claude.ai) (Anthropic) as my design skills are abysmal.
