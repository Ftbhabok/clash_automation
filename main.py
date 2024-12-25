import time
import random
import logging
import colorama
from colorama import Fore, Style
import keyboard
from src.attack import Attacker  # Your attack module
from src.resource_collector import ResourceCollector  # Resource collection module
from src.troop_trainer import TroopTrainer  # Troop training module

# Global variable to track the automation state
stop_automation = False


def setup_logging():
    colorama.init()

    class ColorFormatter(logging.Formatter):
        def format(self, record):
            # Save the original log message
            log_message = record.getMessage()

            # Apply color only to the message part (not the timestamp)
            if record.levelname == 'INFO':
                log_message = f"{Fore.GREEN}{log_message}{Style.RESET_ALL}"
            elif record.levelname == 'WARNING':
                log_message = f"{Fore.YELLOW}{log_message}{Style.RESET_ALL}"
            elif record.levelname == 'ERROR':
                log_message = f"{Fore.RED}{log_message}{Style.RESET_ALL}"

            # Format the full log entry with timestamp and level (using default timestamp)
            formatted_message = f"{record.asctime} - {record.levelname} - {log_message}"
            return formatted_message

    # Add timestamp format to logging
    handler = logging.StreamHandler()
    formatter = ColorFormatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[logging.FileHandler('automation.log', encoding='utf-8'), handler],
        format='%(asctime)s'  # Add the asctime formatter here for proper timestamp handling
    )
    logging.info("Logging setup complete.")


def stop_on_q_key(event):
    """
    Callback function to stop automation when 'q' is pressed.
    """
    global stop_automation
    if event.name == 'q':
        stop_automation = True
        print(f"{Fore.RED}\nStopping automation - Q pressed{Style.RESET_ALL}")
        logging.info("Automation stopped by user (Q key)")


def main():
    global stop_automation
    print(f"{Fore.CYAN}Clash of Clans Automation Starting...{Style.RESET_ALL}")
    setup_logging()

    try:
        collector = ResourceCollector()
        trainer = TroopTrainer()

        gold_threshold = 20
        elixir_threshold = 20
        dark_elixir_threshold = 0
        attacker = Attacker(gold_threshold, elixir_threshold, dark_elixir_threshold)

        troops_to_train = [
            ('giant', 15),
            ('archer', 35),
            ('barbarian', 10),
        ]

        print(f"\n{Fore.YELLOW}Make sure you have:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. Game window open and visible{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2. All required screenshots in place{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}3. Correct troop training images{Style.RESET_ALL}")
        print(f"\n{Fore.GREEN}Press 'q' at any time to stop the automation{Style.RESET_ALL}")
        input(f"\nPress Enter to start (then quickly click game window)...")
        time.sleep(3)

        # Hook the keyboard listener for the 'q' key
        keyboard.on_press(stop_on_q_key)

        cycle_count = 1
        while not stop_automation:
            print(f"\n{Fore.CYAN}Starting cycle #{cycle_count}{Style.RESET_ALL}")
            try:
                # Collect resources
                collector.collect_resources()
                time.sleep(random.uniform(0.5, 1.0))

                # Train troops
                trainer.train_troops(troops_to_train)
                time.sleep(random.uniform(0.5, 1.0))

                # Find and attack
                attacker.find_and_attack()

                # Wait for a random delay between cycles
                wait_time = random.uniform(2.0, 3.0)
                print(f"\n{Fore.MAGENTA}Waiting {wait_time:.1f} seconds before next cycle...{Style.RESET_ALL}")
                time.sleep(wait_time)
                cycle_count += 1

            except Exception as e:
                print(f"\n{Fore.RED}Error in cycle #{cycle_count}: {str(e)}{Style.RESET_ALL}")
                logging.error(f"Error in cycle #{cycle_count}: {str(e)}")
                time.sleep(5)
                continue

    except Exception as e:
        print(f"\n{Fore.RED}Error during automation: {str(e)}{Style.RESET_ALL}")
        logging.error(f"Automation error: {str(e)}")

    finally:
        # Unhook the keyboard listener
        keyboard.unhook_all()
        print(f"{Fore.GREEN}Automation has been stopped.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()

