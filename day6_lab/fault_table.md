# Day 6 Observation Sheet

## Fault table

| Injected fault | Message returned | Did the run continue? |
|---|---|---|
| Invalid JSON | Run `python inject_faults.py` and paste output | Y/N |
| Unknown tool | Run `python inject_faults.py` and paste output | Y/N |
| Missing required | Run `python inject_faults.py` and paste output | Y/N |
| Wrong type | Run `python inject_faults.py` and paste output | Y/N |
| Value outside enum | Run `python inject_faults.py` and paste output | Y/N |
| Invented extra argument | Run `python inject_faults.py` and paste output | Y/N |
| Unsafe expression | Run `python inject_faults.py` and paste output | Y/N |
| Your own fault 1 | Wrong-case tool name | Y/N |
| Your own fault 2 | Arguments is a JSON array | Y/N |

## Agent behaviour

Run `python robust_agent.py` and record:
- Total fee for CS101 and AI202 with 10% scholarship:
- Is DS303 more expensive than CS101?
- Fee for ME404:
- One-line welcome message:
- Did any reply contain two parallel tool calls?
- Did `finish_reason = length` occur?

## Structured outputs

Run `python structured_demo.py` and record:
- No constraint:
- JSON mode:
- Schema mode (strict):
