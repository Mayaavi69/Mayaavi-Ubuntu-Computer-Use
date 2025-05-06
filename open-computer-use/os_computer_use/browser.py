import time
import threading
from multiprocessing import Process, Queue
import webview


class Browser:
    def __init__(self):
        self.width = 1024
        self.height = 768
        self.window_frame_height = 29  # Additional px for window border
        self.command_queue = Queue()
        self.webview_process = None
        self.is_running = False

    def open(self, url, width=None, height=None):
        """
        Open a browser window with the given URL

        Args:
            url (str): The URL to open
            width (int, optional): Window width
            height (int, optional): Window height
        """
        if self.is_running:
            print("Browser window is already running")
            return

        self.width = width or self.width
        self.height = height or self.height

        print(f"URL: {url}")

        # Start webview in separate process
        self.webview_process = Process(
            target=self._create_window,
            args=(url, self.width, self.height, self.command_queue),
        )
        self.webview_process.start()
        self.is_running = True

    def close(self):
        """Close the browser window"""
        if not self.is_running:
            print("No browser window is running")
            return

        self.command_queue.put("close")
        if self.webview_process:
            self.webview_process.join()
            self.webview_process = None
        self.is_running = False

    @staticmethod
    def _create_window(url, width, height, command_queue):
        """Create a webview window in a separate process"""

        def check_queue():
            while True:
                if not command_queue.empty():
                    command = command_queue.get()
                    if command == "close":
                        window.destroy()
                        break
                time.sleep(1)  # Check every second

        window_frame_height = 29
        window = webview.create_window(
            "Browser Window", url, width=width, height=height + window_frame_height
        )

        # Start queue checking in a separate thread
        t = threading.Thread(target=check_queue)
        t.daemon = True
        t.start()

        webview.start()
