# research-agent — interview questions and answers

[README](README.md) · [Project architecture](PROJECT_ARCHITECTURE.md)

Answers below use this repository’s files and implementation. They distinguish existing behavior from suggested extensions; source links let you verify each walkthrough.

## 1. What problem does research-agent address, and what can you demonstrate?

Search then cite local notes. Goals that publish or tweet are refused.

I would demonstrate the linked implementation or examples and distinguish that evidence from any planned production features. Start with [`README.md`](README.md).

## 2. How is this repository organized?

- [`src/research/main.py`](src/research/main.py): Implementation or supporting configuration.
- [`src/research/agent.py`](src/research/agent.py): Implementation or supporting configuration.
- [`requirements.txt`](requirements.txt): Implementation or supporting configuration.
- [`src/research/__init__.py`](src/research/__init__.py): Implementation or supporting configuration.
- [`tests/test_agent.py`](tests/test_agent.py): Executable checks and regression examples.
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml): GitHub Actions job definitions.
- [`README.md`](README.md): Project explanations or operating notes.

[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) contains the component diagram and the implementation walkthrough.

## 3. Can you walk through `run` and explain the decision it makes?

The main walkthrough here is `run(goal, payload)` in [`src/research/agent.py`](src/research/agent.py#L9).

```python
def run(goal, payload):
    if not isinstance(goal, str) or not goal.strip():
        raise InputError("goal is empty")
    if any(word in goal.lower() for word in WRITES):
        return {"refused": True, "reason": "This agent only reads or plans. It does not write.", "tools": [], "wrote": False, "applied": False}
    notes = payload.get("notes") or []; q = set((payload.get("goal") or goal).lower().split()); result = [n for n in notes if q & set(n.lower().split())]
    return {"refused": False, "tools": TOOLS, "hits": result, "wrote": False, "applied": False}
```

The implementation calls `(payload.get('goal') or goal).lower`, `(payload.get('goal') or goal).lower().split`, `InputError`, `any`, `goal.lower`, `goal.strip`, `isinstance`, `n.lower`, `n.lower().split`. In an interview, trace those calls in execution order using a fixture input.

## 4. What input validation and failure behavior are implemented?

Explicit failure paths include:

- `InputError('goal is empty')` in [`src/research/agent.py`](src/research/agent.py#L11).
- `HTTPException(status_code=422, detail=str(exc))` in [`src/research/main.py`](src/research/main.py#L17).

I would test both the condition that reaches each exception and the caller that translates it. An explicit raise does not mean every malformed input or dependency failure is handled.

## 5. Which test would you use to demonstrate correctness?

[`tests/test_agent.py`](tests/test_agent.py#L7) contains `test_runs_and_refuses_a_write`:

```python
def test_runs_and_refuses_a_write():
    payload = client.post("/agent/run", json={"goal": 'error budget notes', **{'payload': {'notes': ['error budget is 43 minutes', 'cafeteria menu']}}}).json()
    assert payload["refused"] is False
    assert payload["applied"] is False
    assert payload["hits"]
    refused = client.post("/agent/run", json={"goal": 'publish this to twitter'}).json()
    assert refused["refused"] is True
```

This is a concrete regression example from the repository. Its assertions establish that case; they do not establish behavior for every input or under production load.

## 6. What HTTP interface does the code expose?

- `GET /healthz` → `healthz` in [`src/research/main.py`](src/research/main.py#L8).
- `POST /agent/run` → `post_run` in [`src/research/main.py`](src/research/main.py#L13).

These are literal decorators. Application/router prefixes, authentication, and middleware must be checked in the corresponding setup code.

## 7. Where does state live, and what happens with multiple workers?

Module-level containers include `TOOLS` in [`src/research/agent.py`](src/research/agent.py).

These containers belong to a Python process. Inspect which are constant fixtures and which are mutated. Mutable process state needs an explicit shared-storage or synchronization strategy before multiple workers can provide consistent behavior.

## 8. How would another engineer reproduce your walkthrough?

Start from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

These commands follow repository manifests; environment setup and command results still need to be checked on the target machine.

## 9. What does automation verify, and what does it not prove?

Inspect [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for triggers, permissions, and job commands. I would name the checks that those definitions run and show the latest run separately. A workflow definition alone does not establish a successful deployment, security review, or production SLO.

## 10. How would you present this project in a Forward Deployed Engineer interview?

Start with the user and operational problem described in [`README.md`](README.md). Explain one constraint that changes the implementation, show the linked code or example, and walk through a success case and a failure case. Agree on a measurable acceptance criterion before expanding the solution, and leave a handoff with data boundaries and rollback ownership. Any proposed production or business metric should be identified as a target until measured.

## 11. What is the input-to-output contract of `run`?

In [`src/research/agent.py`](src/research/agent.py#L9), `run(goal, payload)` receives the inputs. The function computes these intermediate values:

- `notes = payload.get('notes') or []`
- `q = set((payload.get('goal') or goal).lower().split())`
- `result = [n for n in notes if q & set(n.lower().split())]`

Its result is defined by:

- `{'refused': False, 'tools': TOOLS, 'hits': result, 'wrote': False, 'applied': False}`
- `{'refused': True, 'reason': 'This agent only reads or plans. It does not write.', 'tools': [], 'wrote': False, 'applied': False}`

## 12. Which decision rules or boundary conditions should an interviewer challenge?

The implementation in [`src/research/agent.py`](src/research/agent.py#L9) branches on:

- `not isinstance(goal, str) or not goal.strip()`
- `any((word in goal.lower() for word in WRITES))`

A useful extension is a table-driven test that covers each condition just below, at, and above its boundary where applicable. These expressions are the current rules; changing them changes behavior and should be justified by the project’s acceptance criteria.

## Request flow diagram

The mermaid decision tree for `POST /agent/run` is in [docs/PROCESS_FLOW.md](docs/PROCESS_FLOW.md). Use it in interviews to walk hold/refuse/422 vs a successful lab response without implying a production side effect.

