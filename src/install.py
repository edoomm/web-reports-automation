"""Installation module."""
import json

from pathlib import Path

def yes_or_no(question: str) -> bool:
    """Get true as default, no when `'n'`."""
    return False if input(question).lower() == 'n' else True


def config() -> None:
    """Install the main config file."""
    with open('config/schema.json', 'r') as schema_file:
        schema = json.load(schema_file)

    print("No config file found. Creating a new one...")

    verbose_q = "Print out logs in console? [Y/n]: "
    schema['verbose'] = yes_or_no(verbose_q)

    browser_q = "Default browser Firefox? 'n' will set Chrome as default [Y/n]: "
    is_firefox = yes_or_no(browser_q) 
    schema['default_browser'] = "firefox" if is_firefox else "chrome"

    if is_firefox:
        schema['firefox_profile_path'] = input('Firefox profile path: ')
    else:
        schema['chrome_userdata_path'] = input('Chrome user data path: ')
        schema['chrome_profile'] = input('Chrome profile to use: ')

    download_path = str(Path.home() / "Downloads")
    downloadp_q = f"Default download path ({download_path})? [Y/n]: "
    if not yes_or_no(downloadp_q):
        download_path = input("Type the desired download path")
    schema['download_path'] = download_path

    with open('config/config.json', 'w') as config_file:
        json.dump(schema, config_file, indent=4)

    print("Created configuration file successfully.")

def e_creds() -> None:
    """Install the Edenred credentials file."""
    print("No credentials found. Creating file...")

    email = input("email: ")
    passw = input("password: ")

    with open("config/e_creds", 'w') as ecreds_file:
        ecreds_file.write(email + "\n")
        ecreds_file.write(passw)

    print("Credentials created successfully.")
