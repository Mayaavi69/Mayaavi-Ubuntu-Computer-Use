# Ubuntu AI RPA Agent - Mayaavi

An advanced Robotic Process Automation (RPA) agent for Ubuntu that uses local LLMs via Ollama to control your desktop, automating repetitive tasks through natural language commands.

## Features

- 🧠 Uses local LLM models (via Ollama) for task interpretation
- 🔍 Computer vision-based UI element detection with OpenCV
- ⌨️ Keyboard and mouse automation with PyAutoGUI
- 📊 Visual execution logs with screenshots
- 🖥️ Ubuntu OS app support (Terminal, VS Code, LibreOffice, etc.)
- 🔄 Automatic follow-up for complex tasks
- 📝 Action history for reusing previous commands

## Requirements

- Ubuntu Linux
- Python 3.8+
- GPU with 8+ GB VRAM (recommended)
- [Ollama](https://ollama.ai) installed with LLM models (llama3, mistral, etc.)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ubuntu-ai-rpa-agent.git
   cd ubuntu-ai-rpa-agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Ollama and download a compatible model:
   ```bash
   # Install Ollama (see https://ollama.ai for instructions)
   # Then pull a model:
   ollama pull llama3:8b
   ```

## Usage

1. Start the Ollama server in a terminal:
   ```bash
   ollama serve
   ```

2. In another terminal, launch the RPA agent:
   ```bash
   streamlit run rpa_agent.py
   ```

3. Enter natural language commands in the web interface to automate tasks.

Examples:
- "Open Firefox, go to google.com, search for ubuntu tutorials"
- "Open terminal, create a new directory called 'test-project', navigate to it and initialize a git repository"
- "Open LibreOffice Writer and create a new document with the title 'Meeting Notes'"

## Creating Templates

For the agent to recognize UI elements, you need to create template images:

1. Take screenshots of UI elements you want to interact with
2. Crop them to contain just the element
3. Save in the `templates/` folder with descriptive names (e.g., `firefox_address_bar.png`)

## Troubleshooting

- **LLM Connection Issues**: Make sure Ollama is running (`ollama serve`)
- **UI Element Not Found**: Check if your template images match what's on screen
- **Action Failed**: Try breaking down the task into smaller steps

## License

MIT License
