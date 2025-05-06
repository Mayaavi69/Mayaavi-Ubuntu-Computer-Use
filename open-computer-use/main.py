from os_computer_use.streaming import Sandbox
from os_computer_use.browser import Browser
from os_computer_use.sandbox_agent import SandboxAgent
from os_computer_use.logging import Logger
import asyncio
import argparse
import os
from dotenv import load_dotenv

logger = Logger()
load_dotenv()
os.environ["E2B_API_KEY"] = os.getenv("E2B_API_KEY")

async def start(user_input=None, output_dir=None):
    sandbox = None

    try:
        sandbox = Sandbox()
        await asyncio.sleep(5)  # Wait for boot

        # ✅ FFmpeg skipped due to timeouts

        agent = SandboxAgent(sandbox, output_dir)

        print("Starting the VNC server...")
        sandbox.stream.start()
        vnc_url = sandbox.stream.get_url()

        print("\n✅ VNC Client URL (open in browser):")
        print(vnc_url)

        while True:
            if user_input is None:
                try:
                    user_input = input("USER: ")
                except KeyboardInterrupt:
                    break
            else:
                try:
                    agent.run(user_input)
                    user_input = None
                except KeyboardInterrupt:
                    user_input = None
                except Exception as e:
                    logger.print_colored(f"An error occurred: {e}", "red")
                    user_input = None

    finally:
        if sandbox:
            print("Stopping the sandbox...")
            try:
                sandbox.kill()
            except Exception as e:
                print(f"Error stopping sandbox: {str(e)}")
        print("Skipping VNC client shutdown (browser was never opened).")


def initialize_output_directory(directory_format):
    run_id = 1
    while os.path.exists(directory_format(run_id)):
        run_id += 1
    os.makedirs(directory_format(run_id), exist_ok=True)
    return directory_format(run_id)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, help="User prompt for the agent")
    args = parser.parse_args()

    output_dir = initialize_output_directory(lambda id: f"./output/run_{id}")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start(user_input=args.prompt, output_dir=output_dir))

if __name__ == "__main__":
    main()

