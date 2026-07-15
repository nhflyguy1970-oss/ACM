# CognitiveStore Architecture — Durable Persistence

**Status:** Canonical for Phase 2 (P2.1)  
**Rule:** ACM owns persistence. Hosts never own ACM storage files.

## Purpose

Make ACM production-ready with durable, recoverable, host-independent storage — **without** changing cognition.

## Design

| Component | Role |
|-----------|------|
| `CognitiveStore` | In-process living substrate (unchanged cognitive API) |
| Codec (`acm.persistence.codec`) | Versioned snapshot JSON + checksum |
| `SqliteDurableStore` | Replaceable backend (transactions, WAL, backups) |
| `DurableCognitiveStore` | Public façade: flush / export / import / backup / restore / verify |
| `CognitiveEngine(persist_path=...)` | Optional durable attach + `auto_persist` |

## Properties

- Crash recovery via SQLite WAL + latest checkpoint load  
- Transactions on save  
- Schema version + forward migration hook  
- Integrity: `PRAGMA integrity_check` + snapshot checksum (sha256)  
- Import / export portable JSON snapshots  
- Backup / restore of backend file  
- Concurrency: `RLock` around backend ops  
- Technology independence: backend swappable; codec is the contract  

## Intentional omissions

Hosts embedding ACM rows in their own DBs as SoT; vector DB as memory model; distributed consensus.
