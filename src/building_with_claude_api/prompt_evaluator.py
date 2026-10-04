import json
from building_with_claude_api.message_helper import MessageHelper

mh = MessageHelper()

class PromptEvaluator:
    """Runs a prompt against a dataset of test cases and collects the results.

    Uses the module-level `MessageHelper` (`mh`) to talk to Claude. Each output
    is graded by a second Claude call (LLM-as-judge) against a criteria text
    that is shared by every test case.
    """

    def __init__(self):
        pass

    def run_prompt(self, prompt:str) -> str:
        """Send a single prompt to Claude and return its reply.

        Args:
            prompt: The full prompt text, sent as the only user message.

        Returns:
            Claude's text reply (str).
        """

        # Each call starts a fresh conversation, so test cases don't influence
        # one another.
        messages = []
        mh.add_user_message(messages, prompt)
        # Higher limit than the default so long answers aren't cut off before
        # they are graded.
        output = mh.chat(messages, max_tokens=4000)
        return output

    def grade_output(self, test_case: dict, output: str, criteria: str) -> dict:
        """Ask Claude to score an output against the given criteria.

        Args:
            test_case: Dataset entry (dict) with a `"task"` key describing what
                was asked.
            output: The answer text to grade.
            criteria: Text (str) describing what a good output must include.

        Returns:
            The judge's parsed JSON reply (dict) with keys `strengths`,
            `weaknesses`, `reasoning` and `score` (int from 1 to 10).

        Raises:
            ValueError: If the judge's score is not an integer from 1 to 10.
        """
        prompt = f"""You are grading an AI's answer to a task.

        <task>{test_case["task"]}</task>
        <criteria>{criteria}</criteria>
        <answer>{output}</answer>

        Check the answer against each criterion. Give a score from 1 to 10, where 1-3
        means most criteria are missed, 4-7 means some are met, and 8-10 means all or
        nearly all are met. Respond with JSON only:
        {{"strengths": [...], "weaknesses": [...], "reasoning": "...", "score": <integer 1-10>}}
        """

        messages = []
        mh.add_user_message(messages, prompt)
        # Prefill the opening code fence and stop at the closing one, so the
        # reply is just the JSON and can go straight into json.loads.
        mh.add_assistant_message(messages, "```json")
        text = mh.chat(messages, stop_sequences=["```"])

        grade = json.loads(text)
        score = grade["score"]
        if not isinstance(score, int) or not 1 <= score <= 10:
            raise ValueError(f"Judge returned an invalid score: {score!r}")
        return grade

    def run_test_case(self, prompt: str, test_case: dict, criteria: str) -> dict:
        """Run one test case through Claude and grade the result.

        Args:
            prompt: The full prompt text to send for this test case.
            test_case: The dataset entry (dict) the prompt was built from; it is
                returned unchanged alongside the output for later inspection.
            criteria: Text (str) describing what a good output must include,
                used by the judge.

        Returns:
            A dict with keys `output` (Claude's reply), `test_case` (the input
            dict), `score` (int from 1 to 10) and `reasoning` (the judge's
            explanation for the score).
        """
        output = self.run_prompt(prompt)
        grade = self.grade_output(test_case, output, criteria)

        return {
            "output": output,
            "test_case": test_case,
            "score": grade["score"],
            "reasoning": grade["reasoning"]
        }

    def run_eval(self, dataset: list[dict]) -> list[dict]:
        """Run every test case in the dataset and collect the results.

        Args:
            dataset: List of test case dicts. Each must have a `"task"` key
                holding the task description to put in the prompt.
            
        Returns:
            A list of result dicts (see `run_test_case`), in the same order as
            `dataset`.
        """
        results = []

        for test_case in dataset:
            # Wrap the task in a fixed instruction; the same wrapper is used for
            # every case.
            prompt =f"""Please solve the following task: {test_case["task"]}"""
            criteria = test_case["criteria"]
            result = self.run_test_case(prompt, test_case, criteria)
            results.append(result)

        return results

