# Differential verification

The unit of progress is an original function, not an estimated percentage of
the game. Every function moves through these states:

| State | Meaning |
|---|---|
| `unverified` | Hypothesis or translation without comparison |
| `partial` | Some effects match; cases or dependencies remain |
| `trace-matched` | Matches recorded fixtures and traces |
| `accepted` | Repeatable match, reviewed with no relevant unknowns |

## Minimum evidence

- Exact game identity and input fingerprints.
- Original virtual address and, when possible, file or segment offset.
- Bytes or assembly saved at a stable path.
- Inferred calling convention: input, output, and preserved registers.
- Memory ranges read and written.
- Hardware dependencies and called functions.
- Input fixtures and expected states.
- Test command and result.

## Proposed comparison

For a specific call, MAME captures:

1. registers before entry;
2. memory regions the function may read;
3. registers at return; and
4. modified regions and relevant access sequences.

The same fixture is passed to the native harness. The test stops at the first
difference and retains a compact diff. A similar final image is not sufficient:
two implementations can look identical while differing in RNG, timing,
overflow, or internal state.

## Rule for new code

A hardware replacement is verified against MAME's observable behavior but is
marked `hardware-shim`, not recovered game code. This prevents an accidental
reimplementation from being presented as original logic.
