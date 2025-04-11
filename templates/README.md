# UI Element Templates

This directory stores screenshot templates of UI elements that the RPA agent needs to identify on screen.

## How to Create Templates

1. Take a screenshot of your screen (you can use the built-in screenshot tool in the RPA agent)
2. Crop the image to contain ONLY the UI element you want to identify (buttons, input fields, icons, etc.)
3. Save the cropped image in this folder with a descriptive name (e.g., `firefox_address_bar.png`)
4. Use PNG format for best results

## Tips for Good Templates

- **Uniqueness**: Capture elements that are distinctive and not likely to be confused with other parts of the UI
- **Size**: Don't make templates too large or too small (ideally 20-200 pixels in each dimension)
- **Context**: Include just enough surrounding context to make the element unique
- **State**: Capture the element in the state you want to detect (e.g., button unpressed vs. pressed)
- **Color**: Color matters for matching, so ensure your template matches the actual UI theme

## Example Templates to Create

- **Firefox**:
  - `firefox_address_bar.png`
  - `firefox_search_icon.png`
  - `firefox_bookmark_icon.png`

- **Terminal**:
  - `terminal_prompt.png`
  - `terminal_window_title.png`

- **General UI**:
  - `ubuntu_applications_button.png`
  - `desktop_trash_icon.png`
  - `system_menu_icon.png`

## Testing Templates

You can test if your templates work by:
1. Running the RPA agent
2. Taking a screenshot
3. Using the test function to see if the template is detected correctly
