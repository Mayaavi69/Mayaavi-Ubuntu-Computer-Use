# Enhanced Ubuntu AI RPA Agent with Visual Awareness
# Combines best features from both approaches

import os
import subprocess
import requests
import streamlit as st
import pyautogui
import cv2
import numpy as np
from PIL import Image
import re
import time
from datetime import datetime
import json
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("rpa_agent.log"),
        logging.StreamHandler()
    ]
)

# SETTINGS
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_OPTIONS = ["llama3:8b", "mistral:7b", "mixtral:8x7b-instruct", "codellama:13b"]
LOG_DIR = "logs"
TEMPLATE_DIR = "templates"
HISTORY_FILE = "action_history.json"

# Create necessary directories
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(TEMPLATE_DIR, exist_ok=True)

# Extended App Map for Ubuntu
APP_MAP = {
    "terminal": "gnome-terminal",
    "vs code": "code",
    "google": "firefox https://www.google.com",
    "canva": "firefox https://www.canva.com",
    "libreoffice writer": "libreoffice --writer",
    "libreoffice calc": "libreoffice --calc",
    "libreoffice impress": "libreoffice --impress",
    "text editor": "gedit",
    "calculator": "gnome-calculator",
    "files": "nautilus",
    "firefox": "firefox",
    "chrome": "google-chrome",
    "discord": "discord",
    "slack": "slack",
    "settings": "gnome-control-center",
    "system monitor": "gnome-system-monitor"
}

# Screenshot Logger with enhanced metadata
def log_screenshot(step_id, action_type="unknown", command="unknown"):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = os.path.join(LOG_DIR, f"step{step_id}_{timestamp}.png")
    img = pyautogui.screenshot()
    img.save(path)
    
    # Save metadata
    metadata = {
        "timestamp": timestamp,
        "step_id": step_id,
        "action_type": action_type,
        "command": command
    }
    
    meta_path = os.path.join(LOG_DIR, f"step{step_id}_{timestamp}.json")
    with open(meta_path, 'w') as f:
        json.dump(metadata, f)
    
    return path

# Enhanced OpenCV Template Matching with multiple strategies
def find_template_on_screen(template_name, threshold=0.7):
    # First try direct template path
    if os.path.exists(template_name):
        template_path = template_name
    else:
        # Then try from template directory
        template_path = os.path.join(TEMPLATE_DIR, f"{template_name}.png")
        if not os.path.exists(template_path):
            logging.warning(f"Template not found: {template_name}")
            return None

    try:
        screen = pyautogui.screenshot()
        screen_np = np.array(screen)
        screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)
        template = cv2.imread(template_path, 0)
        
        # Try multiple matching methods if the first one fails
        methods = [cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR_NORMED]
        
        for method in methods:
            res = cv2.matchTemplate(screen_gray, template, method)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            
            if max_val >= threshold:
                # Calculate center of template
                w, h = template.shape[::-1]
                center_x = max_loc[0] + w//2
                center_y = max_loc[1] + h//2
                return (center_x, center_y, max_val)
        
        return None
    except Exception as e:
        logging.error(f"Template matching error: {e}")
        return None

# Wait for UI element to appear with timeout
def wait_for_ui_element(template_name, timeout=10, threshold=0.7):
    start_time = time.time()
    while time.time() - start_time < timeout:
        result = find_template_on_screen(template_name, threshold)
        if result:
            return result
        time.sleep(0.5)
    return None

# Enhanced Command Execution with verification
def execute_command(action, command, step_id, active_app=None):
    logging.info(f"Executing: {action} -> {command}")
    
    # Clean command
    if isinstance(command, str):
        command = command.strip()
    
    # Execute based on action type
    if action == "shell_command":
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            output = result.stdout or result.stderr or "✅ Command executed"
            log_path = log_screenshot(step_id, "shell", command)
            return output, log_path
        except subprocess.TimeoutExpired:
            return "⚠️ Command timed out", None
        except Exception as e:
            return f"⚠️ Error: {str(e)}", None

    elif action == "gui_command":
        # Click action
        if command.startswith("click "):
            target = command.replace("click ", "").strip()
            coords = find_template_on_screen(target)
            
            if coords:
                x, y, confidence = coords
                logging.info(f"Found {target} at ({x}, {y}) with confidence {confidence:.2f}")
                pyautogui.moveTo(x, y, duration=0.5)
                pyautogui.click()
                time.sleep(0.5)  # Wait for UI to respond
                log_path = log_screenshot(step_id, "click", target)
                return f"🖱️ Clicked {target} (confidence: {confidence:.2f})", log_path
            else:
                return f"⚠️ Could not find UI element: {target}", None
        
        # Type action
        elif command.startswith("type "):
            text = command.replace("type ", "").strip()
            # Remove quotes if present
            if text.startswith('"') and text.endswith('"'):
                text = text[1:-1]
            
            pyautogui.write(text, interval=0.05)
            log_path = log_screenshot(step_id, "type", text)
            return f"⌨️ Typed: {text}", log_path
        
        # Press key action
        elif command.startswith("press "):
            key = command.replace("press ", "").strip().lower()
            if key == "enter":
                pyautogui.press('enter')
            elif key == "tab":
                pyautogui.press('tab')
            elif key == "space":
                pyautogui.press('space')
            elif key == "escape" or key == "esc":
                pyautogui.press('escape')
            else:
                pyautogui.press(key)
            
            log_path = log_screenshot(step_id, "press", key)
            return f"⌨️ Pressed {key}", log_path
        
        # Open app action
        elif command.startswith("open app "):
            app = command.replace("open app ", "").strip().lower()
            if app in APP_MAP:
                subprocess.Popen(APP_MAP[app], shell=True)
                time.sleep(2)  # Wait for app to start
                log_path = log_screenshot(step_id, "open", app)
                return f"🚀 Opened {app}", log_path
            return f"⚠️ Unknown app: {app}", None
        
        # Wait action
        elif command.startswith("wait "):
            # Wait for seconds or for UI element
            parts = command.replace("wait ", "").strip().split(" for ")
            
            if len(parts) == 1:
                # Just wait seconds
                try:
                    seconds = float(parts[0].replace("seconds", "").replace("s", "").strip())
                    time.sleep(seconds)
                    log_path = log_screenshot(step_id, "wait", f"{seconds} seconds")
                    return f"⏱️ Waited {seconds} seconds", log_path
                except:
                    return "⚠️ Invalid wait time", None
            elif len(parts) == 2 and "element" in parts[1]:
                # Wait for UI element
                element = parts[1].replace("element", "").strip()
                result = wait_for_ui_element(element, timeout=15)
                if result:
                    log_path = log_screenshot(step_id, "wait", f"element {element}")
                    return f"👁️ Found element {element}", log_path
                else:
                    return f"⚠️ Element {element} not found after timeout", None
        
        # Drag action
        elif command.startswith("drag "):
            # Format: drag from element1 to element2
            match = re.search(r"drag from (.*) to (.*)", command)
            if match:
                element1, element2 = match.groups()
                coords1 = find_template_on_screen(element1.strip())
                coords2 = find_template_on_screen(element2.strip())
                
                if coords1 and coords2:
                    x1, y1, _ = coords1
                    x2, y2, _ = coords2
                    pyautogui.moveTo(x1, y1, duration=0.5)
                    pyautogui.dragTo(x2, y2, duration=1)
                    log_path = log_screenshot(step_id, "drag", f"{element1} to {element2}")
                    return f"🖱️ Dragged from {element1} to {element2}", log_path
                else:
                    return "⚠️ Could not find one or both elements for drag operation", None
            else:
                return "⚠️ Invalid drag command format", None
    
    return "⚠️ Unknown action or command", None

# Call LLM with automatic retry and follow-up
def ask_llm(prompt, model, max_retries=3, retry_delay=2):
    for attempt in range(max_retries):
        try:
            response = requests.post(OLLAMA_URL, json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }, timeout=30)
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.RequestException as e:
            logging.error(f"LLM request error (attempt {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise
    return ""

# Process LLM response and follow up if needed
def process_llm_response(prompt, model, response):
    # Extract actions from response
    actions = re.findall(r"ACTION:\s*(\w+)_command\s+([^\n]+)", response)
    
    # If too few actions, try to get more
    if len(actions) < 2:
        logging.info("Initial response has too few actions, requesting follow-up")
        follow_up_prompt = f"{response}\n\nThe above steps are good but incomplete. Please continue with more detailed steps to fully accomplish: {prompt}"
        try:
            follow_up_response = ask_llm(follow_up_prompt, model)
            # Clean up the response to avoid duplicating ACTION prefixes
            cleaned_follow_up = re.sub(r"^(.*?ACTION:)", "ACTION:", follow_up_response, flags=re.DOTALL)
            return response.strip() + "\n\n" + cleaned_follow_up.strip()
        except Exception as e:
            logging.error(f"Follow-up request failed: {e}")
            return response
    
    return response

# Record action history
def save_action_history(task, actions, results):
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
        except:
            pass
    
    # Append new entry
    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "task": task,
        "actions": [{"type": t, "command": c} for t, c in actions],
        "results": results
    })
    
    # Save updated history
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

# STREAMLIT UI
def main():
    st.set_page_config(page_title="Ubuntu AI RPA Agent", layout="wide")
    
    # Sidebar configuration
    st.sidebar.title("🧠 Agent Settings")
    model = st.sidebar.selectbox("Select LLM model", MODEL_OPTIONS, index=0)
    
    # Advanced settings in sidebar
    with st.sidebar.expander("Advanced Settings"):
        template_threshold = st.slider("Template matching threshold", 0.5, 0.95, 0.7, 0.05)
        command_timeout = st.slider("Command timeout (seconds)", 5, 60, 30, 5)
        show_debug = st.checkbox("Show debug info", value=False)
    
    # History in sidebar
    with st.sidebar.expander("Action History"):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r') as f:
                    history = json.load(f)
                    for i, entry in enumerate(history[-5:]):  # Show last 5 entries
                        st.write(f"**{entry['timestamp']}**: {entry['task']}")
                        if st.button(f"Rerun #{i+1}", key=f"rerun_{i}"):
                            st.session_state.user_input = entry['task']
            except:
                st.write("Could not load history")
    
    # Main content
    st.title("🤖 Ubuntu AI RPA Agent")
    st.write("Tell me what you want me to do on your Ubuntu desktop")
    
    # Input area
    user_input = st.text_input("💬 What should I do?", key="user_input")
    col1, col2 = st.columns([1, 1])
    take_screenshot = col1.button("📸 Take Screenshot")
    
    if take_screenshot:
        screenshot_path = log_screenshot("manual", "screenshot", "manual")
        st.image(screenshot_path, caption="Current Screen", use_column_width=True)
    
    # Process user input
    if user_input:
        st.markdown("### 🧠 Thinking...")
        
        # Take initial screenshot for context
        initial_screen = log_screenshot("initial", "context", user_input)
        
        # Build prompt
        prompt = f"""
You are an Ubuntu Desktop RPA (Robotic Process Automation) Agent that helps users automate tasks.
Break down the user's request into a sequence of precise actions.

Only use these action formats:
- ACTION: gui_command click <template_name>
- ACTION: gui_command type <text>
- ACTION: gui_command press <key_name>
- ACTION: gui_command open app <app_name>
- ACTION: gui_command wait <seconds> seconds
- ACTION: gui_command wait <seconds> for element <template_name>
- ACTION: gui_command drag from <template_name1> to <template_name2>
- ACTION: shell_command <command>

User Request: {user_input}

Important:
1. Each line must start with "ACTION:" followed by the command type
2. Always include the full path to files/applications
3. Provide DETAILED step-by-step instructions
4. Break down complex tasks into many small steps
5. Remember the user is on Ubuntu
"""

        try:
            # Get and process LLM response
            response = ask_llm(prompt, model)
            final_response = process_llm_response(user_input, model, response)
            
            if final_response:
                # Display LLM instructions
                st.markdown("#### 📋 Planned Actions:")
                st.code(final_response)
                
                # Extract actions
                actions = re.findall(r"ACTION:\s*(\w+)_command\s+([^\n]+)", final_response)
                
                if actions:
                    # Display all steps
                    for i, (action_type, command) in enumerate(actions):
                        st.markdown(f"**Step {i+1}**: {action_type}_command → {command}")
                    
                    # Run button
                    if st.button("✅ Execute All Steps"):
                        results = []
                        active_app = None
                        
                        # Execute each action
                        for i, (action_type, command) in enumerate(actions):
                            with st.spinner(f"Running step {i+1} → {action_type}_command → {command}"):
                                # Update active app context if needed
                                if action_type == "gui" and "open app" in command.lower():
                                    app_name = command.lower().replace("open app", "").strip()
                                    active_app = app_name
                                
                                # Execute the command
                                result, log_img = execute_command(
                                    action_type + "_command", 
                                    command, 
                                    i+1,
                                    active_app
                                )
                                
                                # Store result
                                results.append(result)
                                
                                # Display result and screenshot
                                st.success(f"✅ Step {i+1}: {result}")
                                if log_img:
                                    st.image(log_img, caption=f"📸 After Step {i+1}", use_column_width=True)
                                
                                # Short delay between steps
                                time.sleep(1)
                        
                        # Save action history
                        save_action_history(user_input, actions, results)
                        
                        st.balloons()
                        st.success("🎉 Task completed!")
                else:
                    st.error("❌ No valid actions detected in LLM response")
            else:
                st.error("❌ Failed to get response from LLM")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            logging.error(f"Error in main flow: {str(e)}")

if __name__ == "__main__":
    main()
