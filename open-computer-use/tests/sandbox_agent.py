from os_computer_use.sandbox_agent import SandboxAgent


# This is a mock sandbox that returns a static screenshot and terminal output
class MockSandbox:
    def __init__(self):
        self.timeout = 60
        self.commands = self

    def screenshot(self):
        with open("./tests/test_screenshot.png", "rb") as f:
            return f.read()

    def run(self, command, timeout=None, background=False):
        class MockResult:
            def __init__(self):
                self.stdout = f"Mock stdout for command: {command}"
                self.stderr = ""

        return MockResult()

    def set_timeout(self, timeout):
        self.timeout = timeout


if __name__ == "__main__":
    # Create an instance of SandboxAgent with the mock sandbox
    agent = SandboxAgent(MockSandbox(), save_logs=False)

    # Test the agent with a sample instruction
    # This will verify that the model providers are working correctly.
    test_instruction = "Open the Firefox browser"
    print("\nRunning test with instruction:", test_instruction)
    agent.run(test_instruction)
