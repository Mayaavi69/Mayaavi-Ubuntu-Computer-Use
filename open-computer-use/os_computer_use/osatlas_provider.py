from gradio_client import Client, handle_file
from os_computer_use.logging import logger
from os_computer_use.grounding import extract_bbox_midpoint

import os


OSATLAS_HUGGINGFACE_SOURCE = "maxiw/OS-ATLAS"
OSATLAS_HUGGINGFACE_MODEL = "OS-Copilot/OS-Atlas-Base-7B"
OSATLAS_HUGGINGFACE_API = "/run_example"

HF_TOKEN = os.getenv("HF_TOKEN")


class OSAtlasProvider:
    """
    The OS-Atlas provider is used to make calls to OS-Atlas.
    """

    def __init__(self):
        self.client = Client(OSATLAS_HUGGINGFACE_SOURCE, hf_token=HF_TOKEN)

    def call(self, prompt, image_data):
        result = self.client.predict(
            image=handle_file(image_data),
            text_input=prompt + "\nReturn the response in the form of a bbox",
            model_id=OSATLAS_HUGGINGFACE_MODEL,
            api_name=OSATLAS_HUGGINGFACE_API,
        )
        position = extract_bbox_midpoint(result[1])
        image_url = result[2]
        logger.log(f"bbox {image_url}", "gray")
        return position
