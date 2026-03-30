import os
import sys
import json
import win32api
import win32con
import ctypes

# Windows console colors (only red and white)
class Colors:
    @staticmethod
    def init():
        try:
            Colors.kernel32 = ctypes.windll.kernel32
            Colors.stdout_handle = Colors.kernel32.GetStdHandle(-11)
            Colors.enabled = True
        except:
            Colors.enabled = False
    
    @staticmethod
    def set(color):
        if Colors.enabled:
            Colors.kernel32.SetConsoleTextAttribute(Colors.stdout_handle, color)
    
    @staticmethod
    def red():
        Colors.set(12)
    @staticmethod
    def white():
        Colors.set(7)
    @staticmethod
    def reset():
        Colors.set(7)

Colors.init()

def clear_screen():
    """Clear console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print main header"""
    clear_screen()
    print_white("=" * 60)
    print_red("     Screen Resolution Switcher")
    print_white("=" * 60)
    print_white("")

def print_red(text):
    Colors.red()
    print(text)
    Colors.reset()

def print_white(text):
    Colors.white()
    print(text)
    Colors.reset()

def print_error(text):
    Colors.red()
    print(f"[ERROR] {text}")
    Colors.reset()

DM_PELSWIDTH = 0x00080000
DM_PELSHEIGHT = 0x00100000
DM_DISPLAYFREQUENCY = 0x00400000
DM_BITSPERPEL = 0x00040000

CDS_TEST = 0x00000002
CDS_UPDATEREGISTRY = 0x00000001
DISP_CHANGE_SUCCESSFUL = 0

def has_console():
    try:
        return ctypes.windll.kernel32.GetConsoleWindow() != 0
    except:
        return False

def safe_input(prompt):
    if not has_console():
        return ""
    try:
        return input(prompt)
    except:
        return ""

def wait_for_enter():
    if has_console():
        try:
            input("Press Enter to exit...")
        except:
            pass

class ResolutionManager:
    def __init__(self):
        self.app_name = "ResolutionSwitcher"
        self.config_dir = os.path.join(os.environ['APPDATA'], self.app_name)
        self.config_file = os.path.join(self.config_dir, 'config.json')
        self.state_file = os.path.join(self.config_dir, 'state.txt')
        self.ensure_config_dir()
        
    def ensure_config_dir(self):
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
    
    def get_available_modes(self):
        modes = []
        i = 0
        try:
            while True:
                dm = win32api.EnumDisplaySettings(None, i)
                mode = {
                    'width': dm.PelsWidth,
                    'height': dm.PelsHeight,
                    'frequency': dm.DisplayFrequency,
                    'bits': dm.BitsPerPel
                }
                if mode not in modes:
                    modes.append(mode)
                i += 1
        except:
            pass
        
        grouped = {}
        for mode in modes:
            key = f"{mode['width']}x{mode['height']}"
            if key not in grouped:
                grouped[key] = []
            if mode['frequency'] not in grouped[key]:
                grouped[key].append(mode['frequency'])
        
        for key in grouped:
            grouped[key].sort()
        
        return grouped
    
    def display_available_modes(self, grouped_modes):
        print_white("=" * 60)
        print_white("     Available resolutions on your system")
        print_white("=" * 60)
        
        resolutions = list(grouped_modes.keys())
        resolutions.sort(key=lambda x: (int(x.split('x')[1]), int(x.split('x')[0])), reverse=True)
        
        for i, res in enumerate(resolutions, 1):
            freqs = grouped_modes[res]
            freq_str = ", ".join([f"{f}Hz" for f in freqs])
            print_red(f"  {i:2}. {res:15} - {freq_str}")
        
        print_white("=" * 60)
        return resolutions
    
    def select_resolution(self, grouped_modes, resolutions, preset_num):
        print_red(f"\n--- Preset {preset_num} ---")
        
        while True:
            try:
                choice = safe_input(f"Select resolution (1-{len(resolutions)}): ")
                if not choice:
                    raise KeyboardInterrupt
                idx = int(choice) - 1
                if 0 <= idx < len(resolutions):
                    selected_res = resolutions[idx]
                    break
                else:
                    print_error(f"Please enter a number between 1 and {len(resolutions)}")
            except ValueError:
                print_error("Please enter a valid number")
            except KeyboardInterrupt:
                print_white("\n[CANCELLED] Operation cancelled")
                raise
        
        available_freqs = grouped_modes[selected_res]
        
        # Clear screen before showing frequencies
        clear_screen()
        print_white("=" * 60)
        print_white("     Available resolutions on your system")
        print_white("=" * 60)
        
        # Show resolutions again
        for i, res in enumerate(resolutions, 1):
            freqs = grouped_modes[res]
            freq_str = ", ".join([f"{f}Hz" for f in freqs])
            if res == selected_res:
                print_red(f"  {i:2}. {res:15} - {freq_str}  <-- SELECTED")
            else:
                print_red(f"  {i:2}. {res:15} - {freq_str}")
        
        print_white("=" * 60)
        
        if len(available_freqs) == 1:
            selected_freq = available_freqs[0]
            print_white(f"Only one frequency available: {selected_freq}Hz")
        else:
            print_white(f"\nAvailable frequencies for {selected_res}:")
            for i, freq in enumerate(available_freqs, 1):
                print_white(f"  {i}. {freq}Hz")
            
            while True:
                try:
                    choice = safe_input(f"\nSelect frequency (1-{len(available_freqs)}): ")
                    if not choice:
                        raise KeyboardInterrupt
                    idx = int(choice) - 1
                    if 0 <= idx < len(available_freqs):
                        selected_freq = available_freqs[idx]
                        break
                    else:
                        print_error(f"Please enter a number between 1 and {len(available_freqs)}")
                except ValueError:
                    print_error("Please enter a valid number")
                except KeyboardInterrupt:
                    print_white("\n[CANCELLED] Operation cancelled")
                    raise
        
        width, height = map(int, selected_res.split('x'))
        
        print_red(f"\n[SELECTED] Preset {preset_num}: {width}x{height} @ {selected_freq}Hz")
        
        return {
            'width': width,
            'height': height,
            'frequency': selected_freq,
            'bits': 32
        }
    
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return None
        return None
    
    def save_config(self, config):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
    
    def create_config(self):
        try:
            print_header()
            
            print_white("[SCAN] Scanning available display modes...")
            grouped_modes = self.get_available_modes()
            
            if not grouped_modes:
                print_error("Could not detect any display modes!")
                return None
            
            resolutions = self.display_available_modes(grouped_modes)
            
            preset1 = self.select_resolution(grouped_modes, resolutions, 1)
            preset2 = self.select_resolution(grouped_modes, resolutions, 2)
            
            config = {
                "presets": {
                    "1": preset1,
                    "2": preset2
                },
                "current": "1"
            }
            
            self.save_config(config)
            
            print_white("\n" + "=" * 60)
            print_white("[OK] Configuration saved!")
            print_white(f"      {self.config_file}")
            print_white("=" * 60)
            
            return config
        except KeyboardInterrupt:
            print_white("\n[INFO] Setup cancelled. No changes saved.")
            return None
    
    def reconfigure(self):
        try:
            print_header()
            
            print_white("What do you want to reconfigure?")
            print_white("  1. Preset 1 only")
            print_white("  2. Preset 2 only")
            print_white("  3. Both presets")
            print_white("  4. Cancel")
            
            choice = safe_input("\nSelect option (1-4): ")
            
            if not choice or choice == "4":
                print_white("[CANCELLED] No changes made.")
                return
            
            config = self.load_config()
            if config is None:
                print_error("No configuration found!")
                return
            
            print_header()
            
            print_white("[SCAN] Scanning available display modes...")
            grouped_modes = self.get_available_modes()
            resolutions = self.display_available_modes(grouped_modes)
            
            if choice == "1":
                config["presets"]["1"] = self.select_resolution(grouped_modes, resolutions, 1)
            elif choice == "2":
                config["presets"]["2"] = self.select_resolution(grouped_modes, resolutions, 2)
            elif choice == "3":
                config["presets"]["1"] = self.select_resolution(grouped_modes, resolutions, 1)
                # Clear screen before second preset
                print_header()
                print_white("[SCAN] Scanning available display modes...")
                grouped_modes = self.get_available_modes()
                resolutions = self.display_available_modes(grouped_modes)
                config["presets"]["2"] = self.select_resolution(grouped_modes, resolutions, 2)
            else:
                print_error("Invalid option!")
                return
            
            self.save_config(config)
            print_white("\n[OK] Configuration updated successfully!")
        except KeyboardInterrupt:
            print_white("\n[CANCELLED] Reconfiguration cancelled.")
    
    def get_current_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return f.read().strip()
            except:
                return "1"
        return "1"
    
    def save_state(self, state):
        with open(self.state_file, 'w') as f:
            f.write(state)
    
    def set_resolution(self, width, height, frequency, bits=32):
        try:
            print_white(f"[TESTING] Mode {width}x{height} @ {frequency}Hz...")
            
            dm = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
            dm.PelsWidth = width
            dm.PelsHeight = height
            dm.DisplayFrequency = frequency
            dm.BitsPerPel = bits
            dm.Fields = DM_PELSWIDTH | DM_PELSHEIGHT | DM_DISPLAYFREQUENCY | DM_BITSPERPEL
            
            result = win32api.ChangeDisplaySettings(dm, CDS_TEST)
            
            if result != DISP_CHANGE_SUCCESSFUL:
                if result == -2:
                    print_error(f"Mode {width}x{height} @ {frequency}Hz is not supported!")
                else:
                    print_error(f"Test failed with code: {result}")
                return False
            
            result = win32api.ChangeDisplaySettings(dm, CDS_UPDATEREGISTRY)
            
            if result == DISP_CHANGE_SUCCESSFUL:
                print_white(f"[OK] Resolution changed to {width}x{height} @ {frequency}Hz")
                return True
            else:
                print_error(f"Failed to apply settings. Code: {result}")
                return False
                
        except Exception as e:
            print_error(f"{e}")
            return False
    
    def get_current_resolution(self):
        try:
            dm = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
            return f"{dm.PelsWidth}x{dm.PelsHeight} @ {dm.DisplayFrequency}Hz"
        except:
            return "Unknown"
    
    def switch(self):
        try:
            config = self.load_config()
            
            if config is None:
                print_white("[INFO] No configuration found. Starting setup...")
                config = self.create_config()
                if config is None:
                    print_error("Failed to create configuration!")
                    return False
            
            current_state = self.get_current_state()
            
            if current_state == "1":
                next_preset = "2"
            else:
                next_preset = "1"
            
            preset = config["presets"][next_preset]
            width = preset["width"]
            height = preset["height"]
            frequency = preset["frequency"]
            bits = preset.get("bits", 32)
            
            # Clear screen before showing switch info
            clear_screen()
            print_white("=" * 60)
            print_red("     Screen Resolution Switcher")
            print_white("=" * 60)
            print_white(f"Current: {self.get_current_resolution()}")
            print_white("")
            print_red(f"[SWITCH] Preset {next_preset}: {width}x{height} @ {frequency}Hz")
            print_white("")
            
            if self.set_resolution(width, height, frequency, bits):
                self.save_state(next_preset)
                print_white("\n[SUCCESS] Switch completed!")
                return True
            else:
                print_error("\nUnable to switch resolution!")
                return False
        except KeyboardInterrupt:
            print_white("\n[INFO] Switch cancelled")
            return False
    
    def show_presets(self):
        config = self.load_config()
        
        if config is None:
            print_white("\n[INFO] No configuration found.")
            print_white("[INFO] Run the script to create one.")
            return
        
        clear_screen()
        print_red("\n" + "=" * 60)
        print_red("     Current presets")
        print_red("=" * 60)
        
        for key, preset in config["presets"].items():
            print_red(f"\nPreset {key}:")
            print_red(f"  Resolution: {preset['width']}x{preset['height']}")
            print_red(f"  Refresh rate: {preset['frequency']}Hz")
            print_red(f"  Color depth: {preset.get('bits', 32)}bit")
        
        current = self.get_current_state()
        print_red(f"\n[ACTIVE] Current preset: {current}")
        print_red("=" * 60)

def main():
    try:
        manager = ResolutionManager()
        
        print_header()
        
        # Check if config exists
        config = manager.load_config()
        if config is None:
            print_white("[INFO] No configuration found. Starting setup...")
            manager.create_config()
            print_header()
        
        # Show menu
        print_white("What do you want to do?")
        print_white("  - Press ENTER to switch resolution")
        print_white("  - Type 'change' to edit configuration")
        print_white("  - Type 'show' to view current presets")
        print_white("  - Type 'exit' to quit")
        print_white("")
        
        user_input = safe_input("> ").strip().lower()
        
        if user_input == "change":
            manager.reconfigure()
        elif user_input == "show":
            manager.show_presets()
        elif user_input == "exit":
            print_white("\n[INFO] Exiting...")
            return
        else:
            manager.switch()
        
        wait_for_enter()
            
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        wait_for_enter()

if __name__ == "__main__":
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            main()
        else:
            print_white("\n[INFO] Requesting administrator privileges...")
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
    except Exception as e:
        print_error(f"Failed to launch: {e}")
        wait_for_enter()