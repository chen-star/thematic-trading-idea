import asyncio
import sys
import os
import contextlib
from io import StringIO

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from google.adk.runners import InMemoryRunner
from agents.agent import app
from agents.email_agent import email_mcp_connection
from evaluation.evaluator import Evaluator, EvaluationResult

TEST_TOPICS = [
    "Mega 7",
    "Renewable Energy Storage",
]


async def run_evaluation():
    topics = TEST_TOPICS

    runner = InMemoryRunner(app=app)
    evaluator = Evaluator()

    print("Starting Evaluation Run...\n", file=sys.stderr)

    results = []

    for topic in topics:
        print(f"Running agent for topic: {topic}", file=sys.stderr)
        query = f"The thematic topic is: '{topic}'. Please execute the task as defined in your system instructions."

        captured_output = StringIO()
        try:
            # Capture stdout
            with contextlib.redirect_stdout(captured_output):
                await runner.run_debug(query)

            output = captured_output.getvalue()
            # Also print to real stdout so user can see progress if they want,
            # or just rely on stderr for progress.
            # Let's print a snippet to stderr.
            print(
                f"Agent finished for {topic}. Output length: {len(output)} chars.",
                file=sys.stderr,
            )

            # Evaluate the output
            print(f"Evaluating {topic}...", file=sys.stderr)
            eval_result = evaluator.evaluate_report(topic, output)
            results.append((topic, eval_result))

            print(f"Score: {eval_result.score}/10", file=sys.stderr)

        except Exception as e:
            print(f"Error running for {topic}: {e}", file=sys.stderr)
            # Use captured output so far if available
            output = captured_output.getvalue()
            if output:
                print(
                    f"Captured output before error:\n{output[:500]}...", file=sys.stderr
                )

            # Append a failed result
            results.append(
                (topic, EvaluationResult(0, f"Error: {e}", "N/A", "N/A", "N/A"))
            )

    # Print Summary
    print("\n" + "=" * 30)
    print("EVALUATION SUMMARY")
    print("=" * 30)
    for topic, result in results:
        status = "PASS" if result.score >= 7 else "FAIL"
        print(f"Topic: {topic}")
        print(f"Status: {status} (Score: {result.score}/10)")
        print(f"Relevance: {result.relevance}")
        print(f"Completeness: {result.completeness}")
        print(f"Actionability: {result.actionability}")
        print(f"Reasoning: {result.reasoning}")
        print("-" * 20)

    # Explicitly close the MCP connection
    await email_mcp_connection.close()


if __name__ == "__main__":
    asyncio.run(run_evaluation())
