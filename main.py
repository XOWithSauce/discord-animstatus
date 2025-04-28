import sys
import requests
import time
import asyncio

class Optio:
    def __init__(self, title, description, action=None) -> None:
        self.title = title
        self.description = description
        self.action = action

class Options:
    def __init__(self, options) -> None:
        self.options = options

    def __str__(self):
        result = ""
        for i, option in enumerate(self.options, start=1):
            result += f"{i}. {option.title}: {option.description}\n"
        return result

class DCStatus:
    def __init__(self) -> None:
        self.running = True
        self.url = "https://discord.com/api/v9/users/@me/settings"
        self.auth_token = ""
        self.typing_symbol = "︳"
        self.max_status_width = 20
        self.narrow_nbspace = " ‎" # because regular space is stripped by default from status
        self.base_status = ""
        self.current_status = ""
        
        self.idle_duration = 45
        self.wait_idle = 2.0
        self.wait_active = 2.0

        self.debug = True
        
        self.application_begin = time.time()
        self.application_requests = 0
        self.response_time_delta = 0

        self.options_list = [
            Optio("[ANIM] Type and Idle", "Animates Status like it was being written in realtime.", self.type_and_idle),
            Optio("[ANIM] Scrolling", "Animates Status like a marquee sign, scrolling the text from left to right.", self.scrolling_message),
            Optio("Settings", "Configure your Auth Token, Status message and other parameters.", self.set_settings),
            Optio("Help", "Show the Basic usage info", self.show_help),
            Optio("Exit", "Exit the application.", self.exit_program),
        ]
        self.options = Options(self.options_list)

        self.settings_list = [
            Optio("Status Message", "Set your status message", self.set_status_message),
            Optio("Auth Token", "Set your Discord Auth Token", self.set_auth_token),
            Optio("Set Request Delay", "Set how fast your message updates in seconds", self.set_request_delay),
            Optio("Back", "Back to menu."),
        ]
        self.settings = Options(self.settings_list)
    
    async def change_status(self, msg):
        if self.debug:
            print(msg)
            return
        
        header = {"authorization": self.auth_token}
        jsonData = {
            "status": "online",
            "custom_status": {"text": msg}
        }
        request = requests.patch(self.url, headers=header, json=jsonData)
        self.response_time_delta = request.elapsed.total_seconds()
        if request.status_code != 200:
            app_time = time.time() - self.application_begin
            with open("error_log.txt", "w") as f:
                f.write(f"Exiting after {app_time} seconds\n")
                f.write(f"Total number of requests: {self.application_requests}\n")
                f.write(f"Response status: \n{request.status_code}\n")
                f.write(f"Response content: \n{request.content.decode('utf-8')}\n")
            sys.exit()
        self.application_requests += 1

    # Typing animation
    async def idle_typer(self):
        start_time = time.time()
        while time.time() - start_time <= self.idle_duration:
            status_idle = self.base_status + self.typing_symbol
            await self.change_status(status_idle)
            await asyncio.sleep(self.wait_idle + self.response_time_delta)
            await self.change_status(self.base_status)
            await asyncio.sleep(self.wait_idle + self.response_time_delta)

    async def type_message(self):
        for char in self.base_status:
            self.current_status += char
            for _ in range(2):
                await self.change_status(self.current_status + self.typing_symbol)
                await asyncio.sleep(self.wait_active + self.response_time_delta)
                await self.change_status(self.current_status)
                await asyncio.sleep(self.wait_active + self.response_time_delta)
        self.current_status = ""

    async def type_and_idle(self):
        print("Type & Idle started")
        print("Press CTRL + C to exit the application\n")
        while self.running:
            await self.type_message()
            await self.idle_typer()
            
    # Marquee animation
    async def scrolling_message(self):
        status_length = len(self.base_status)
        pads_max_amnt = self.max_status_width - status_length
        base_status_with_custom_spaces = self.base_status.replace(' ', self.narrow_nbspace)
        if pads_max_amnt > 0:
            status_padded = self.narrow_nbspace * pads_max_amnt + base_status_with_custom_spaces
        else:
            status_padded = self.narrow_nbspace * (self.max_status_width//2) + base_status_with_custom_spaces
        while True:
            status_padded = status_padded[1:] + status_padded[0]
            self.current_status = status_padded[:self.max_status_width]
            await self.change_status(self.current_status)
            await asyncio.sleep(self.wait_active + self.response_time_delta)
            
    # other main menu utils
    async def show_help(self):
        print("\n--- HELP ---")
        print("To start your animated status message follow these steps:")
        print("1. Go to Settings menu and input your desired status message")
        print("2. In the Settings menu input your Auth token")
        print("3. Return to Main Menu and select your animation [ANIM]")
        print("------------")
    
    async def exit_program(self):
        print("Exiting...")
        self.running = False
        
    # settings
    async def set_settings(self):
        in_settings = True
        while in_settings:
            print("\n--- SETTINGS ---")
            print(self.settings)

            choice = input(f"Select an option (1-{len(self.settings_list)}): ").strip()

            if not choice.isdigit() or not (1 <= int(choice) <= len(self.settings_list)):
                print("Invalid choice. Try again.")
                continue
            
            idx = int(choice) - 1
            option = self.settings_list[idx]

            if idx == len(self.settings_list) - 1:
                in_settings = False
                continue

            if option.action:
                await option.action()
                
    async def set_status_message(self):
        self.base_status = input(f"Type your status message: ").strip()

    async def set_auth_token(self):
        self.auth_token = input(f"Paste your auth token: ").strip()

    async def set_request_delay(self):
        print("\nFrequency at which API updates are sent. Mind the rate-limits!")
        delay = input("Delay between requests (seconds) (default 2.0): ").strip()
        delay_float = float(delay)
        if delay_float > 0:
            self.wait_idle = delay_float
            self.wait_active = delay_float
        else:
            print("Failed to set request delay. Delay must be greater than 0.")

    # mainloop
    async def main_loop(self):
        while self.running:
            print("\n--- MENU ---")
            print(self.options)

            choice = input(f"Select an option (1-{len(self.options_list)}): ").strip()

            if not choice.isdigit() or not (1 <= int(choice) <= len(self.options_list)):
                print("Invalid choice. Try again.")
                continue

            option = self.options_list[int(choice) - 1]
            if option.action:
                await option.action()
                

if __name__ == "__main__":
    dc_status = DCStatus()
    asyncio.run(dc_status.main_loop())
