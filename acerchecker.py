#!/usr/bin/env python3
"""
ACER CHECKER MOBILE LEGENDS
"""

import os
import sys
import time
import requests
import json
from datetime import datetime

class Acerchecker:
    def __init__(self):
        self.checked_accounts = []
        self.session = requests.Session()
        self.base_url = "https://account.mobilelegends.com"
        
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_banner(self):
        banner = """
LIGHT_CYAN='\033[1;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${LIGHT_CYAN}╔════════════════════════════════════════════╗${NC}"
echo -e "${LIGHT_CYAN}║ ${YELLOW}>> Acer Checker <<${NC}                             ${LIGHT_CYAN}║${NC}"
echo -e "${LIGHT_CYAN}║ ${YELLOW}>> Mobile Legends Bang Bang <<${NC}                 ${LIGHT_CYAN}║${NC}"
echo -e "${LIGHT_CYAN}╚════════════════════════════════════════════╝${NC}"
echo ""

        """
        print(banner)
    
    def animate_text(self, text, delay=0.03):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def check_account_valid(self, email, password):
        """Check if account credentials are valid"""
        print(f"🔍 Checking: {email}")
        
        # Simulasi API call ke Moonton
        try:
            # Ini placeholder untuk real API call
            # Di real implementation, butuh reverse engineering MLBB API
            
            # Simulasi response berdasarkan hash credentials
            account_hash = hash(email + password) % 100
            
            if account_hash < 60:  # 60% chance valid
                return {
                    "status": "VALID",
                    "premium": account_hash > 80,
                    "level": (account_hash % 30) + 1,
                    "server": ["Asia", "Europe", "America"][account_hash % 3],
                    "last_login": f"{datetime.now().strftime('%Y-%m-%d')}"
                }
            elif account_hash < 80:  # 20% chance invalid
                return {"status": "INVALID", "reason": "Wrong credentials"}
            else:  # 20% chance banned
                return {"status": "BANNED", "reason": "Account suspended"}
                
        except Exception as e:
            return {"status": "ERROR", "reason": str(e)}
    
    def check_server_status(self):
        """Check MLBB server status"""
        print("🌐 Checking server status...")
        
        servers = {
            "Asia": {"url": "https://mlbb-asia.com", "status": "UNKNOWN"},
            "Europe": {"url": "https://mlbb-europe.com", "status": "UNKNOWN"},
            "America": {"url": "https://mlbb-america.com", "status": "UNKNOWN"},
            "Middle East": {"url": "https://mlbb-me.com", "status": "UNKNOWN"}
        }
        
        for server, info in servers.items():
            try:
                response = requests.get(info["url"], timeout=5)
                info["status"] = "🟢 ONLINE" if response.status_code == 200 else "🔴 OFFLINE"
                info["response_time"] = f"{response.elapsed.total_seconds()*1000:.0f}ms"
            except:
                info["status"] = "🔴 OFFLINE"
                info["response_time"] = "Timeout"
            
            print(f"   {server}: {info['status']} ({info['response_time']})")
            time.sleep(0.5)
        
        return servers
    
    def check_player_stats(self, player_id):
        """Get player statistics"""
        print(f"📊 Fetching stats for: {player_id}")
        
        # Simulasi player data
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
        """Bulk check accounts from file"""
        print(f"📁 Bulk checking from: {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                accounts = [line.strip().split(':') for line in f if ':' in line]
            
            print(f"📊 Found {len(accounts)} accounts")
            
            results = {"valid": [], "invalid": [], "banned": [], "error": []}
            
            for i, (email, password) in enumerate(accounts, 1):
                print(f"[{i}/{len(accounts)}] Checking: {email[:20]}...")
                
                result = self.check_account_valid(email, password)
                result["email"] = email
                
                if result["status"] == "VALID":
                    results["valid"].append(result)
                    status_icon = "✅️"
                elif result["status"] == "BANNED":
                    results["banned"].append(result) 
                    status_icon = "🚫"
                else:
                    results["invalid"].append(result)
                    status_icon = "❌️"
                
                print(f"   {status_icon} {result['status']}")
                time.sleep(0.5)  # Rate limiting
            
            return results
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def export_results(self, results, format_type="json"):
        """Export results to file"""
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
        
        print(f"💾 Results exported to: {filename}")
        return filename
    
    def show_menu(self):
        """Show main menu"""
        self.clear_screen()
        self.show_banner()
        
        menu_items = [
            "1. Check Empas",
            "2. Exits", 
        ]
        
        print("🎯 MAIN MENU")
        print("─" * 40)
        for item in menu_items:
            print(item)
        print("─" * 40)
    
    def run(self):
        """Main application loop"""
        last_results = None
        
        while True:
            self.show_menu()
            choice = input("\nSelect option: ").strip()
            
                
            if choice == "1":
                self.clear_screen()
                self.show_banner()
                print("📁 BULK ACCOUNT CHECK")
                print("─" * 40)
                
                file_path = input("Enter accounts file path: ")
                last_results = self.bulk_check_accounts(file_path)
                
                if last_results:
                    print(f"\n📊 SUMMARY:")
                    print(f"   ✅️ Valid: {len(last_results['valid'])}")
                    print(f"   ❌️ Invalid: {len(last_results['invalid'])}")
                    print(f"   🚫 Banned: {len(last_results['banned'])}")
                    print(f"   ⚠️ Errors: {len(last_results['error'])}")
                
                input("\nPress Enter to continue...")
                
                
            elif choice == "2":
                print("\n Thank you for using Acerchecker")
                break
                
            else:
                print("❌ Invalid option!")
                time.sleep(1)

if __name__ == "__main__":
    checker = Acerchecker()
    checker.run()
