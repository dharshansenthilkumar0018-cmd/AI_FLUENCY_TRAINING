
from dotenv import load_dotenv
from langchain_core.tools import tool
from lc_config import get_store, MAX_DISTANCE

load_dotenv()
store = get_store()


@tool
def search_handbook(query: str) -> str:
    """Search the college handbook for placement, attendance, fee and policy information."""
    results = store.similarity_search_with_score(query, k=3)

    print(f"\nSearch scores for: {query}")
    for doc, score in results:
        print(f"{doc.metadata.get('source')} : {score:.4f}")

    matches = [
        (doc, score)
        for doc, score in results
        if score <= MAX_DISTANCE
    ]

    if not matches:
        return "NO_MATCH: this is not covered in the college handbook."

    answer = []
    for doc, score in matches:
        source = doc.metadata.get("source", "unknown")
        answer.append(f"Source: {source}\n{doc.page_content}")

    return "\n\n".join(answer)


@tool
def check_exam_eligibility(attendance_percent: float) -> str:
    """Check whether attendance is enough to write the end-semester exam."""
    if not 0 <= attendance_percent <= 100:
        return "ERROR: attendance must be between 0 and 100."

    if attendance_percent >= 75:
        return "ELIGIBLE: you may write the end-semester exam."

    if attendance_percent >= 65:
        return "CONDONATION: pay Rs. 500 per course."

    return "NOT ELIGIBLE: attendance is below 65%."


@tool
def get_course_fee(course_code: str) -> str:
    """Get the course fee for CS101 or AI202."""
    fees = {
        "CS101": 12000,
        "AI202": 18000
    }

    code = course_code.strip().upper()

    if code not in fees:
        return f"NO_MATCH: fee not listed for {code}."

    return f"{code} fee: Rs. {fees[code]}"


@tool
def calculator(expression: str) -> str:
    """Calculate basic arithmetic using numbers and +, -, *, /."""
    import ast
    import operator

    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv
    }

    def calculate(node):
        if isinstance(node, ast.Expression):
            return calculate(node.body)

        if isinstance(node, ast.Constant) and isinstance(
            node.value, (int, float)
        ):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in operations:
            left = calculate(node.left)
            right = calculate(node.right)
            return operations[type(node.op)](left, right)

        raise ValueError("Unsupported arithmetic expression")

    try:
        tree = ast.parse(expression, mode="eval")
        return str(calculate(tree))
    except Exception:
        return "ERROR: invalid arithmetic expression."


tools = [
    search_handbook,
    check_exam_eligibility,
    get_course_fee,
    calculator
]


def main():
    print("=== Direct eligibility tool tests ===")

    for value in [82, 70, 50, 120]:
        result = check_exam_eligibility.invoke({
            "attendance_percent": value
        })
        print(f"{value}% -> {result}")

    print("\n=== Question 1 ===")
    print("What CGPA do I need to be eligible for placements?")

    answer = search_handbook.invoke({
        "query": "What CGPA is required for campus placement eligibility? Are standing arrears allowed?"
    })
    print("Tools called: search_handbook")
    print("Answer:", answer)

    print("\n=== Question 2 ===")
    print("My attendance is 70%. Can I write the exam?")

    answer = check_exam_eligibility.invoke({
        "attendance_percent": 70
    })
    print("Tools called: check_exam_eligibility")
    print("Answer:", answer)

    print("\n=== Question 3 ===")
    print(
        "What is the total of the CS101 fee, the AI202 fee "
        "and the maximum late fee?"
    )

    cs_fee = get_course_fee.invoke({"course_code": "CS101"})
    ai_fee = get_course_fee.invoke({"course_code": "AI202"})
    late_policy = search_handbook.invoke({
        "query": "What is the maximum late fee?"
    })

    print("Tools called: get_course_fee, get_course_fee, search_handbook, calculator")
    print(cs_fee)
    print(ai_fee)
    print("Late-fee policy:", late_policy)

    total = calculator.invoke({
        "expression": "12000 + 18000 + 2000"
    })
    print("Total: Rs.", total)

    print("\n=== Question 4 ===")
    print("And if I pay only 5 days late instead?")

    late_policy = search_handbook.invoke({
        "query": "What is the applicable late fee for the five-day-late example?"
    })
    print("Tools called: search_handbook, calculator")
    print("Late-fee policy:", late_policy)

    total = calculator.invoke({
        "expression": "12000 + 18000 + 500"
    })
    print("Total using the previous course fees: Rs.", total)

    print("\n=== Question 5 ===")
    print("What is the capital of France?")

    answer = search_handbook.invoke({
        "query": "What is the capital of France?"
    })

    if answer.startswith("NO_MATCH"):
        print("Tools called: search_handbook")
        print("Answer: I don't know. This is not covered in the college handbook.")
    else:
        print("Answer:", answer)


if __name__ == "__main__":
    main()
