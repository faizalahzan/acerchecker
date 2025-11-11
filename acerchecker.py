#!/usr/bin/env python3
"""
ACER CHECKER MOBILE LEGENDS (Styled Version)
"""

import os
import time
import json
import requests
from datetime import datetime

class Acerchecker:
    def __init__(self):
        self.checked_accounts = []
        self.session = requests.Session()
        self.base_url = "https://account.mobilelegends.com"

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_banner(self):
        banner = """
╔════════════════════════════════════════════╗
║              [bold cyan]Acer Checker[/bold cyan] - [bold yellow]Mobile Legends[/bold yellow]              ║
╚════════════════════════════════════════════╝
        """
        console.print(Panel.fit(banner, border_style="bright_blue"))

    def check_account_valid(self, email, password):
        """Simulasi pengecekan akun"""
        account_hash = hash(email + password) % 100

        if account_hash < 60:
            return {
                "status": "VALID",
                "premium": account_hash > 80,
                "level": (account_hash % 30) + 1,
                "server": ["Asia", "Europe", "America"][account_hash % 3],
                "last_login": f"{datetime.now().strftime('%Y-%m-%d')}"
            }
        elif account_hash < 80:
            return {"status": "INVALID", "reason": "Wrong credentials"}
        else:
            return {"status": "BANNED", "reason": "Account suspended"}

    def bulk_check_accounts(self, file_path):
        """Bulk check dari file"""
        try:
            with open(file_path, 'r') as f:
                accounts = [line.strip().split(':') for line in f if ':' in line]

            console.print(f"\n📁 Ditemukan [bold cyan]{len(accounts)}[/bold cyan] akun\n")
            results = {"valid": [], "invalid": [], "banned": [], "error": []}

            for (email, password) in track(accounts, description="🔍 Checking accounts..."):
                result = self.check_account_valid(email, password)
                result["email"] = email

                if result["status"] == "VALID":
                    results["valid"].append(result)
                elif result["status"] == "BANNED":
                    results["banned"].append(result)
                else:
                    results["invalid"].append(result)

                time.sleep(0.3)

            return results
        except Exception as e:
            console.print(f"[bold red]❌ Error:[/bold red] {e}")
            return None

    def export_results(self, results):
        """Simpan hasil"""
        filename = f"check_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        console.print(f"\n💾 [bold green]Hasil disimpan ke:[/bold green] {filename}")

    def show_summary(self, results):
        """Tampilkan hasil dalam tabel"""
        table = Table(title="📊 Hasil Pemeriksaan Akun", border_style="bright_yellow")
        table.add_column("Status", justify="center", style="bold")
        table.add_column("Jumlah", justify="center")

        table.add_row("✅ VALID", str(len(results["valid"])))
        table.add_row("❌ INVALID", str(len(results["invalid"])))
        table.add_row("🚫 BANNED", str(len(results["banned"])))
        table.add_row("⚠️ ERROR", str(len(results["error"])))

        console.print(table)

    def show_menu(self):
        """Menu utama"""
        self.clear_screen()
        self.show_banner()
        console.print("[bold cyan]🎯 MENU UTAMA[/bold cyan]\n")
        console.print("1. 🔍 Cek Empas")
        console.print("2. 🚪 Keluar")

    def run(self):
        """Main app loop"""
        while True:
            self.show_menu()
            choice = Prompt.ask("\nPilih opsi", choices=["1", "2"])

            if choice == "1":
                self.clear_screen()
                self.show_banner()
                file_path = Prompt.ask("📂 Masukkan path file akun (format email:pass)")
                results = self.bulk_check_accounts(file_path)

                if results:
                    self.show_summary(results)
                    self.export_results(results)
                input("\nTekan [Enter] untuk kembali...")

            elif choice == "2":
                console.print("\n[bold green]Terima kasih telah menggunakan Acerchecker! 👋[/bold green]\n")
                break


if __name__ == "__main__":
    Acerchecker().run()
