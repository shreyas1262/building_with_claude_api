from building_with_claude_api.message_helper import MessageHelper

mh = MessageHelper()

class PromptEvaluator:
    """Runs a prompt against a dataset of test cases and collects the results.

    Uses the module-level `MessageHelper` (`mh`) to talk to Claude. Grading is
    not implemented yet, so every test case currently gets a placeholder score.
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
        output = mh.chat(messages)
        return output

    def run_test_case(self, prompt: str, test_case: dict) -> dict:
        """Run one test case through Claude and package the result with a score.

        Args:
            prompt: The full prompt text to send for this test case.
            test_case: The dataset entry (dict) the prompt was built from; it is
                returned unchanged alongside the output for later inspection.

        Returns:
            A dict with keys `output` (Claude's reply), `test_case` (the input
            dict) and `score` (currently a hardcoded placeholder of 10).
        """
        output = self.run_prompt(prompt)

        # TODO - Grading
        # Placeholder: every case gets the same score until grading is built.
        score = 10

        return {
            "output": output,
            "test_case": test_case,
            "score": score
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
            result = self.run_test_case(prompt, test_case)
            results.append(result)
        
        return results
    
