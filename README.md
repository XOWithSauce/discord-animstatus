# Discord Animated Status Updater

This Python script allows you to animate your Discord custom status using different styles such as typing simulation or marquee scrolling.

## Features

- **Type and Idle Animation**: Simulates typing your status message in real-time, followed by periodic "idle" animation.
- **Scrolling Animation**: Creates a marquee-style scrolling text effect in your Discord status.
- **Custom Settings**:
  - Set your own status message
  - Input your Discord Authentication Token
  - Configure the request delay time

## Setup

1. Install the required dependencies:
   ```bash
   pip install requests
   ```

2. Obtain your Discord Authorization Token:
   - **Important**: Be careful with your token, it gives full account access.
   - **Note**: Discord normally hides the token after the page fully loads. However, you can reliably retrieve it by using Chrome’s Mobile Emulation feature:
     1. Open [discord.com](https://discord.com) and log in to your account.
     2. Open Chrome Developer Tools (`F12` or `Ctrl+Shift+I`).
     3. Toggle **Device Toolbar** (click the phone/tablet icon or press `Ctrl+Shift+M`) to enable Mobile Emulation.
     5. Go to the **Application** tab.
     6. Under **Local Storage**, select `https://discord.com`.
     7. In the search bar, type `token`.
     8. The token should now be visible directly in the **Key-Value** list without disappearing.
     9. Copy the token from the **Value** field.

3. Run the script:
   ```bash
   python main.py
   ```

## Usage

Upon starting the script, you will be presented with a menu:

- **[ANIM] Type and Idle**: Animate as if you are typing your status.
- **[ANIM] Scrolling**: Animate the status as scrolling text.
- **Settings**: Configure your token, status message, and update delay.
- **Help**: View basic instructions.
- **Exit**: Exit the program.

### Configure your program

1. Navigate to the **Settings** menu.
2. Input your desired **Status Message**.
3. Paste your **Discord Auth Token**.
4. Optionally, adjust the **Request Delay** for slower or faster updates. ( Be mindful! If you input very low request delays your account might get banned or rate-limited)
5. Return to the main menu and select an animation to begin.

## Notes

- **Debug Mode**: When enabled (`self.debug = True`), the script will print status updates instead of sending them to Discord.
- **Error Handling**: If a request fails, the error will be logged into `error_log.txt` and the program will exit.
- **Respect Discord API Rate Limits**: Updating your status too frequently can result in account restrictions.

## Disclaimer

Using your personal Discord account with unauthorized scripts like this may result in actions taken against your account, including but not limited to warnings, restrictions, or permanent bans.

By using this script, you acknowledge that:

- You are fully responsible for any consequences that arise from its use.
- You understand that manually modifying your account's status through the API without official support is considered against Discord’s policies.
- The author of this script is not affiliated with Discord and does not endorse or encourage ToS violations.
- This script is intended for **educational and personal learning purposes only**.

**Use at your own risk.**
