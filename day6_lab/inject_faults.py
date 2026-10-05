"""Day 6: deterministic fault injection tests for tool-call guards."""
import json
from robust_agent import handle_tool_call

class FakeFunction:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class FakeCall:
    """Looks like one entry of message.tool_calls."""
    def __init__(self, name, arguments, call_id="call_test"):
        self.id = call_id
        self.type = "function"
        self.function = FakeFunction(name, arguments)

FAULTS = [
    ("a good call", FakeCall("get_course_fee", '{"course_code": "AI202"}')),
    ("invalid JSON", FakeCall("get_course_fee", '{"course_code": "AI202"')),
    ("unknown tool", FakeCall("send_email", '{"to": "accounts@college.edu"}')),
    ("missing required", FakeCall("get_course_fee", "{}")),
    ("wrong type", FakeCall("get_course_fee", '{"course_code": 101}')),
    (
        "value outside the enum",
        FakeCall(
            "get_course_fee",
            '{"course_code": "CS101", "semester": "summer"}',
        ),
    ),
    (
        "invented extra argument",
        FakeCall(
            "get_course_fee",
            '{"course_code": "CS101", "year": 2026}',
        ),
    ),
    (
        "unknown course code",
        FakeCall("get_course_fee", '{"course_code": "ME404"}'),
    ),
    (
        "unsafe expression",
        FakeCall(
            "calculator",
            json.dumps({"expression": "__import__('os').system('ls')"}),
        ),
    ),
    ("empty arguments string", FakeCall("calculator", "")),
    # Student-added faults:
    ("wrong case tool name", FakeCall("GET_COURSE_FEE", '{"course_code": "CS101"}')),
    ("arguments is array", FakeCall("calculator", '["12000 + 18000"]')),
]

if __name__ == "__main__":
    print("=" * 82)
    for label, call in FAULTS:
        result = handle_tool_call(call, log=False)
        print(f"{label:<28} -> {result[:90]}")
    print("=" * 82)
    print("Every line above is a STRING. Nothing should raise or crash.")
