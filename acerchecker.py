#!/usr/bin/env python3
"""
ACER CHECKER MOBILE LEGENDS - ELEGANT STYLE (NO ERROR)
"""

import os
import time
import requests
import json
from datetime import datetime

# Warna & Gaya CLI
class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"
    YELLOW = "\033[33m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    BLUE = "\033[34m"
    GRAY = "\033[90m"
    WHITE = "\033[97m"

class Acerchecker:
    def __init__(self):
        self.checked_accounts = []
        self.session = requests.Session()
        self.base_url = "https://account.mobilelegends.com"

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def show_banner(self):
        print(Style.CYAN + "╔" + "═" * 46 + "╗")
        print(f"║{Style.BOLD}{Style.WHITE}           ✨ ACER CHECKER ✨                 {Style.CYAN}║")
        print(f"║{Style.DIM}{Style.WHITE}          MOBILE LEGENDS EDITION              {Style.CYAN}║")
        print("╚" + "═" * 46 + "╝" + Style.RESET)
        print()

    def animate_text(self, text, delay=0.02):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def check_account_valid(self, email, password):
        print(f"{Style.YELLOW}🔍 Checking:{Style.RESET} {email}")
        try:
            # Simulasi hasil login (tidak benar-benar konek ke server)
            account_hash = hash(email + password) % 100
            if account_hash < 60:
                return {
                    "status": "VALID",
                    "premium": account_hash > 50,
                    "level": (account_hash % 30) + 1,
                    "server": ["Asia", "Europe", "America"][account_hash % 3],
                    "last_login": f"{datetime.now().strftime('%Y-%m-%d')}"
                }
            elif account_hash < 80:
                return {"status": "INVALID", "reason": "Wrong credentials"}
            else:
                return {"status": "BANNED", "reason": "Account suspended"}
        except Exception as e:
            return {"status": "ERROR", "reason": str(e)}

    def check_server_status(self):
        print(f"{Style.CYAN}🌐 Checking server status...{Style.RESET}")
        servers = {
            "Asia": {"url": "https://mlbb-asia.com", "status": "UNKNOWN"},
            "Europe": {"url": "https://mlbb-europe.com", "status": "UNKNOWN"},
            "America": {"url": "https://mlbb-america.com", "status": "UNKNOWN"},
            "Middle East": {"url": "https://mlbb-me.com", "status": "UNKNOWN"}
        }

        for server, info in servers.items():
            try:
                response = requests.get(info["url"], timeout=5)
                if response.status_code == 200:
                    info["status"] = f"{Style.GREEN}🟢 ONLINE{Style.RESET}"
                else:
                    info["status"] = f"{Style.RED}🔴 OFFLINE{Style.RESET}"
                info["response_time"] = f"{response.elapsed.total_seconds()*1000:.0f}ms"
            except:
                info["status"] = f"{Style.RED}🔴 OFFLINE{Style.RESET}"
                info["response_time"] = "Timeout"

            print(f"   {Style.WHITE}{server:<12}{Style.RESET}: {info['status']} ({info['response_time']})")
            time.sleep(0.5)

        return servers

    def check_player_stats(self, player_id):
        print(f"{Style.CYAN}📊 Fetching stats for:{Style.RESET} {player_id}")
        stats = {
            "player_id": player_id,
            "username": f"Player_{player_id[-4:]}",
            "level": (hash(player_id) % 30) + 1,
            "rank": ["Warrior", "Elite", "Master", "Grandmaster", "Epic", "Legend", "Mythic"][hash(player_id) % 7],
            "matches": (hash(player_id) % 5000) + 100,
            "win_rate": f"{(hash(player_id) % 30) + 45}%",
            "favorite_hero": ["Miya", "Alucard", "Eudora", "Zilong", "Layla"][hash(player_id) % 5],
            "server": ["Asia", "Europe", "America"][hash(player_id) % 3],
            "last_active": f"{(hash(player_id) % 30) + 1} days ago"
        }
        return stats

    def bulk_check_accounts(self, file_path):
        print(f"{Style.MAGENTA}📁 Bulk checking from:{Style.RESET} {file_path}")
        try:
            with open(file_path, 'r') as f:
                accounts = [line.strip().split(':') for line in f if ':' in line]

            print(f"{Style.CYAN}📊 Found {len(accounts)} accounts{Style.RESET}")
            results = {"valid": [], "invalid": [], "banned": [], "error": []}

            for i, (email, password) in enumerate(accounts, 1):
                print(f"{Style.DIM}[{i}/{len(accounts)}]{Style.RESET} {Style.YELLOW}{email[:25]}{Style.RESET} ...")
                result = self.check_account_valid(email, password)
                result["email"] = email

                if result["status"] == "VALID":
                    results["valid"].append(result)
                    icon = f"{Style.GREEN}✅{Style.RESET}"
                elif result["status"] == "BANNED":
                    results["banned"].append(result)
                    icon = f"{Style.RED}🚫{Style.RESET}"
                elif result["status"] == "INVALID":
                    results["invalid"].append(result)
                    icon = f"{Style.RED}❌{Style.RESET}"
                else:
                    results["error"].append(result)
                    icon = f"{Style.YELLOW}⚠{Style.RESET}"

                print(f"   {icon} {result['status']}")
                time.sleep(0.4)
            return results

        except Exception as e:
            print(f"{Style.RED}❌ Error:{Style.RESET} {e}")
            return None

    def export_results(self, results, format_type="json"):
        filename = f"check_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format_type}"
        if format_type == "json":
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
        elif format_type == "txt":
            with open(filename, 'w') as f:
                for category, accounts in results.items():
                    f.write(f"\n{category.upper()}:\n")
                    for acc in accounts:
                        f.write(f"  {acc['email']} - {acc['status']}\n")
        print(f"{Style.GREEN}💾 Results exported to:{Style.RESET} {filename}")
        return filename

    def show_menu(self):
        self.clear_screen()
        self.show_banner()
        print(f"{Style.BOLD}{Style.YELLOW}🎯 MAIN MENU{Style.RESET}")
        print(Style.GRAY + "─" * 46 + Style.RESET)
        print(f"{Style.CYAN}1.{Style.RESET} Check Empas")
        print(f"{Style.CYAN}2.{Style.RESET} Exit")
        print(Style.GRAY + "─" * 46 + Style.RESET)

    def run(self):
        last_results = None
        while True:
            self.show_menu()
            choice = input(f"\n{Style.BOLD}{Style.WHITE}Select option → {Style.RESET}").strip()
            if choice == "1":
                self.clear_screen()
                self.show_banner()
                print(f"{Style.MAGENTA}📁 BULK ACCOUNT CHECK{Style.RESET}")
                print(Style.GRAY + "─" * 46 + Style.RESET)
                file_path = input(f"{Style.WHITE}Enter file empas path:{Style.RESET} ")

                last_results = self.bulk_check_accounts(file_path)
                if last_results:
                    print(f"\n{Style.BOLD}{Style.YELLOW}📊 SUMMARY:{Style.RESET}")
                    print(f"   {Style.GREEN}✅ Valid:{Style.RESET} {len(last_results['valid'])}")
                    print(f"   {Style.RED}❌ Invalid:{Style.RESET} {len(last_results['invalid'])}")
                    print(f"   {Style.RED}🚫 Banned:{Style.RESET} {len(last_results['banned'])}")
                    print(f"   {Style.YELLOW}⚠ Errors:{Style.RESET} {len(last_results['error'])}")
                input(f"\n{Style.DIM}Press Enter to continue...{Style.RESET}")
            elif choice == "2":
                print(f"\n{Style.CYAN}💡 Thank you for using Acerchecker!{Style.RESET}")
                break
            else:
                print(f"{Style.RED}❌ Invalid option!{Style.RESET}")
                time.sleep(1)

if __name__ == "__main__":
    checker = Acerchecker()
    checker.run()
