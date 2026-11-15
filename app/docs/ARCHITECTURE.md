# Architecture summary

## Purpose and threat model

An intentionally insecure messenger. There is one fixed design, no rounds. The flaws live in the crypto and in the client's error handling, not in the framing.

- **Channel:** deliberately unprotected (`ws://` and plain HTTP, no TLS). The attacker sees the whole broadcast feed, so the job is breaking the crypto, not getting on the network path.
- **Server:** trusted only for the key directory (first-come, no overwrite). It stamps nothing and is not trusted for time or ordering.
- **Attacker:** a registered user who sees everything and can inject frames.
- **Out of scope:** replay protection (a captured frame can be rebroadcast at any time), name squatting, lost-key recovery.
- **Known limitations to document:**
  - A malicious server could do key substitution.
  - Senders control their own `timestamp`, so they control their message's position in the chat order.
  - A replayed frame slots into its original position by `timestamp`, so it can be easy to overlook in the UI.

## Components

1. **Relay server:** HTTP API plus a receive-only WebSocket feed. It never interprets ciphertext or verifies signatures.
2. **Client:** key generation, encrypt/decrypt, sign/verify, CLI. It keeps a local copy of sent plaintext, since Alice can't decrypt her own outgoing messages.
3. **Crypto module:** `encrypt(key, msg)`, `decrypt(key, msg)`, sign/verify, hash, key generation.
4. **Attacker tooling:** separate scripts that work on exported captures or a passive sniffer client.

## Transport

- **WebSocket:** live feed only, simplex: server to client. The server pushes each stored frame to every open socket. Clients send nothing on it, and the server ignores or closes on incoming data frames.
- **HTTP:** everything else
  - `POST /register` (name, public key): `INSERT` into `keys`, returning 409 on a name conflict.
  - `GET /keys/{name}`
  - `POST /messages`: the server checks size and basic JSON shape, stores the frame, then broadcasts it.

*This is a draft schema, final API contracts are TBD.*
- Acks and rejections are HTTP status codes (200, 400, 409, 413). Nothing on the socket is ever a reply.
- **Echo to the sender:** the server has no per-connection identity, so it can't exclude the sender's own socket. Alice receives her own frame like everyone else and her client drops it because `to` isn't her. Nothing depends on this.
- **Liveness:** the server sends WebSocket ping/pong control frames and drops sockets that don't answer or whose send buffer keeps growing. These are protocol-level frames, not application messages, so the relay needs no message types, request IDs, or per-client replies. Clients reconnect automatically when the connection dies.

## Server state

- **Sockets:** an in-memory set.
- **Database:** two tables - keys for distribution, messages purely for logging purposes.

```sql
CREATE TABLE keys (
  name       TEXT PRIMARY KEY,
  public_key TEXT NOT NULL
);

CREATE TABLE messages (
  sender    TEXT,           -- copied from the frame, for readability only
  recipient TEXT,
 timestamp       INTEGER,        -- sender's claimed timestamp (ms), unverified
  frame     TEXT NOT NULL   -- the raw JSON, stored verbatim
);
```
*This is a draft schema. As this component is not an essential part of the project, final DB design decisions are TBD.*

- **First-come, no overwrite** is enforced atomically by the primary key on `keys.name`.
- **`messages` is a log.** The server never queries it. The extra columns exist so the log is readable. The hidden SQLite `rowid` gives arrival order if ever needed, and there are no explicit ids.
- **Column names:** `from` and `to` are reserved SQL words, hence `sender` and `recipient`.
- **Parsing on insert:** filling these columns means the server reads the envelope's `from`, `to`, and `timestamp`. It never touches the ciphertext or signature. A frame lacking the expected fields is rejected with 400. The `frame` column is the source of truth, since the other columns are copies of unverified, sender-claimed values.
- **Export:** a script dumps `messages` to `.jsonl`, sorted by `timestamp` if desired, as the attacker's dataset.
- No login and no per-connection identity.

## Identity and keys

- **One RSA key pair per user**, used for both decryption and signing. The shared use is a deliberate flaw that enables the signing oracle.
- The private key is generated on the client, never leaves the device, and is persisted to a file.
- Registration is first-come, with no overwrite, no proof of possession, and no key changes. The server only sanity-checks the key.
- **Usernames** are 1 to 32 bytes, 8-bit character encoding, and must not contain the padding byte. This is enforced at registration. Longer usernames can not be truncated. This mechanism is what makes the fixed-width padding in the signature (below) unambiguous.
- Receiving needs no authentication, since only the private-key holder can read a frame. Sending is authenticated by signatures that recipients verify against the directory.

## Frame (envelope)

```json
{
  "from": "alice",
  "to": "bob",
  "timestamp": 1731672000123,
  "ciphertext": "<base64>",
  "signature": "<base64>"
}
```

- **Order:** encrypt-then-sign.
- **Encrypted payload:** strict JSON `{"from": "...", "text": "..."}`, encrypted to the recipient's public key. The inner `from` prevents signature stripping and re-signing as someone else, because the receiver compares it to the envelope's `from`.
- **Signature:** over `H(pad(from, 32) ||timestamp|| ciphertext)`, where `from` is right-padded with a padding byte to a fixed 32-byte width so every field sits at a fixed position in the hash input. This relies on registration enforcing a username rule (see Identity and keys) so two different names can never pad to the same bytes.
- **`timestamp`:** the sender's clock in milliseconds, covered by the signature. It is the only timestamp in the system and is used for ordering. For now it can't be trusted, as it's client-provided, but it's kept in the frame in case of a future architecture change.
- **`to` is deliberately unsigned.** This gives a bit of extra signing oracle surface (re-addressing a valid frame) and no damage apart from that (a re-adressed frame won't be read by the new recipient as the private keys won't match).
- **No checksum, magic bytes or server-assigned fields.** The strict JSON parse is the failure signal.
- One frame per recipient.

## Ordering

- Clients order messages by the signed `timestamp`, so all clients agree on the order regardless of delivery.
- Ties and same-millisecond collisions are a race condition. The timestamps can't be trusted anyway.
- There is no freshness check and no clock-sync assumption for now.

## Client receive logic

1. Ignore the frame if `to` isn't me. This also drops the echo of my own sent frames.
2. Verify the signature against `from`'s registered key.
3. Decrypt.
4. Parse the payload strictly. On failure, send an error bounce (see below).
5. Reject the frame if the payload's `from` doesn't equal the envelope's.
6. Display the message, ordered by `timestamp`.

## The deliberate oracle (error bounce)

- On parse failure, the client automatically sends a normal frame back to the sender through `POST /messages`: `from: alice, to: mallory`, payload `{"from": "alice", "text": "error: malformed message, content=<hex of decrypted bytes>"}`, encrypted to the sender's key and signed as usual.
- Only the original sender can read it. The feed pushes it to everyone, but other clients drop it at step 1. No new frame type is needed.
- A client never sends an error in response to an error message, which prevents ping-pong loops.
- **Attack flow:**
  1. Mallory builds the forged frame (`from: alice`, `to: bob`, `timestamp`, `ciphertext: C`) and computes its hash `h`.
  2. He sends Alice a frame with `ciphertext = h`, signed with his own key.
  3. Alice's client decrypts, which yields her signature on `h`. The result fails to parse, so the bounce leaks it.
  4. Mallory attaches the leaked value as the signature on the forged frame, which Bob accepts.
- Blinding works the same way and hides what is being asked.
- With no time window, there is no deadline on this round trip, and a leaked signature stays valid forever.

## Deliberate weaknesses and the attacks they enable

| Weakness | Attack |
|---|---|
| Cryptographic weaknesses | Not a scope of this document |
| Shared key, no padding, raw bytes in the bounce | Signing oracle (direct or blinded) |
| Unsigned `to` | Re-addressing a valid frame |
| No replay protection | Rebroadcast a captured frame at any time |
| Sender-controlled `timestamp` | Pinning or burying a message in the chat order |
| Visible metadata (`from`, `to`, `timestamp`, length) | Traffic analysis |

## Optional extension: time window (replay protection)

A receiver-side check only. Nothing else in the design changes.

- **Client:** add one step after "ignore if not for me": drop the frame if `|local_now - timestamp| > N`, with N around 30 to 60 seconds. Add the constant `N`.
- **Wire format, signature, server, DB:** unchanged, because `timestamp` is already in the signed frame.
- **What it gives:** a captured frame expires once its `timestamp` falls outside the window, so later replays fail. Replay inside the window still works.
- **What it doesn't give:** a trustworthy clock. A sender can sign any `timestamp` within ±N of the receiver's clock, which only shifts their own position in the chat order.
- **Clock sync:** clients now need roughly synced clocks, or a generous N.
- **Asymmetric option:** allow a small future tolerance (a few seconds) and a larger past tolerance. A symmetric window lets Mallory set `timestamp` to about `now + N` and keep a forged frame valid for up to about `2N`.
- **Signing oracle:** the trigger, bounce, and broadcast round trip now has to fit inside the window. This is easy in a scripted attack, but it is a deadline that didn't exist before.
- **Weaknesses table:** "no replay protection" becomes "replay inside the window."
- **Interaction with catch-up:** if both extensions are built, fetched history would fail the window check, so it must skip that step, which weakens replay protection for those frames.

## Optional extension: catch-up on reconnect

Without it, a client that is offline or reconnects misses whatever was broadcast in the meantime. To add it, you would extend:

- **Server HTTP API:** add `GET /messages?since=<timestamp>`, returning stored frames with `timestamp > since`, optionally filtered by `recipient` and capped per request. The `timestamp` and `recipient` columns, which are otherwise only for readability, would now be queried, so add an index on them.
- **Cursor caveat:** `timestamp` is sender-claimed, so a frame with an older `timestamp` can arrive at the server after a newer one, and a `since=<timestamp>` cursor can miss it. Either fetch with an overlap margin and deduplicate, or use the hidden `rowid` as the cursor and return it with each record.
- **Client state:** persist the last-seen cursor to disk, next to the private key, and update it after each processed frame.
- **Reconnect flow:** on startup and after each reconnect, fetch the gap over HTTP, run it through the receive logic, then continue with the live feed. Frames that arrive on the socket during the fetch must be buffered, and duplicates dropped by a stable key such as `(from, timestamp, signature)`.
- **Client liveness:** if no pings or frames arrive for longer than the interval plus a margin, treat the socket as dead, reconnect, and run the catch-up fetch.
- **Replay window:** with no window in the base design, fetched history needs no special handling. If the time-window extension is also built, see its interaction note above.
- **Exports:** the same endpoint can serve the attacker's dataset, which makes the export script optional.
