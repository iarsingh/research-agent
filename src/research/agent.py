TOOLS = ["search_notes", "cite"]
WRITES = ("publish", "tweet", "email",)


class InputError(ValueError):
    pass


def run(goal, payload):
    if not isinstance(goal, str) or not goal.strip():
        raise InputError("goal is empty")
    if any(word in goal.lower() for word in WRITES):
        return {"refused": True, "reason": "This agent only reads or plans. It does not write.", "tools": [], "wrote": False, "applied": False}
    notes = payload.get("notes") or []; q = set((payload.get("goal") or goal).lower().split()); result = [n for n in notes if q & set(n.lower().split())]
    return {"refused": False, "tools": TOOLS, "hits": result, "wrote": False, "applied": False}
