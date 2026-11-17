# Mini Chain

A small, educational blockchain written in Python and Flask: hash-linked blocks, proof-of-work mining, a REST API and multi-node consensus.

> **Educational project.** This is a learning tool and is not secure. See [Limitations](#limitations).

## Features

- Blocks linked by SHA-256 hashes, so editing history is detectable
- Proof-of-work mining with adjustable difficulty
- Transaction pool and mining reward
- Multi-node consensus using the longest-valid-chain rule

## Quick start

Requires Python 3.10 or newer.

```bash
git clone https://github.com/h4rl0/mini-chain.git
cd mini-chain
python -m venv .venv
```

Activate the virtual environment.

**Windows (PowerShell):**

```bash
.venv\Scripts\Activate.ps1
```

**Mac / Linux:**

```bash
source .venv/bin/activate
```

Install the dependencies and start a node:

```bash
python -m pip install -r requirements.txt
python blockchain.py
```

Open http://127.0.0.1:5000 in your browser (If port 5000 is taken run `python blockchain.py -p 5050` instead.)


## Limitations 
- Not secure. It exists to teach mechanics
- Anyone can submit a transaction as anyone.
- No double-spend protection
- No authentication
- In-memory only

## Acknowledgements 
The structure follows Daniel van Flymen's tutorial "Learn Blockchains by Building One" (HackerNoon, 2017). This version was rewritten for current Python and Flask, with a different proof-of-work design and full chain validation.