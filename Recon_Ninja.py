import os
import shutil
import subprocess
from colorama import Fore, Style, init
import argparse

# Initialize colorama
init(autoreset=True)

# Required tools
TOOLS = ["subfinder", "httpx", "waybackurls", "gau", "gf", "nuclei", "katana"]

# Check for required tools
def check_tools():
    missing = [tool for tool in TOOLS if not shutil.which(tool)]
    if missing:
        print(f"{Fore.RED}[-] Missing required tools: {', '.join(missing)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Please install the missing tools before running the script.{Style.RESET_ALL}")
        exit(1)

# Run shell command
def run_command(command, desc):
    print()
    print(f"{Fore.YELLOW}[+] {desc}{Style.RESET_ALL}")
    subprocess.run(command, shell=True)

# Get non-empty lines from file
def get_output_lines(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    return []

# Format count for color-coded summary
def format_count(label, count):
    color = Fore.GREEN if count > 0 else Fore.RED
    return f" - {label}: {color}{count}{Style.RESET_ALL}"

# Recon function
def run_recon(domain, template_path, output_path):
    output_path = output_path or "output"
    full_dir = os.path.join(output_path, domain)
    os.makedirs(full_dir, exist_ok=True)

    subs_file     = os.path.join(full_dir, "subs.txt")
    live_file     = os.path.join(full_dir, "livehosts.txt")
    js_file       = os.path.join(full_dir, "js.txt")
    wayback_file  = os.path.join(full_dir, "wayback.txt")
    param_file    = os.path.join(full_dir, "params.txt")
    xss_file      = os.path.join(full_dir, "xss.txt")
    sqli_file     = os.path.join(full_dir, "sqli.txt")
    lfi_file      = os.path.join(full_dir, "lfi.txt")
    redirect_file = os.path.join(full_dir, "redirect.txt")
    nuclei_file   = os.path.join(full_dir, "nuclei.txt")
    summary_file  = os.path.join(full_dir, "summary.txt")

    # Banner
    print(f"\n{Fore.CYAN}[ Advance_Recon v1.0 ] - Automated Bug Bounty Recon Tool")
    print(f"{Fore.GREEN}Author: Varun Sulakhe\n")
    print(f"[+] Recon started for: {domain}\n")

    # Commands
    run_command(f"subfinder -d {domain} -silent | tee {subs_file}", "Running Subfinder...\n")
    run_command(f"cat {subs_file} | httpx -silent | tee {live_file}", "Running Httpx...\n")
    run_command(f"cat {subs_file} | waybackurls | tee {wayback_file}", "Extracting URLs from Wayback...\n")
    run_command(f"cat {live_file} | katana -jc -d 5 | grep '.js$' | tee {js_file}", "Extracting JS files using Katana...\n")
    run_command(f"gau --subs {domain} | sed 's/=.*/=/' | tee {param_file}", "Running gau...\n")
    run_command(rf"cat {param_file} | gf xss | sort -u | tee {xss_file}", "Filtering URLs for potential XSS endpoints...\n") 
    run_command(f"cat {param_file} | gf sqli | sort -u | tee {sqli_file}", "Filtering URLs for potential SQLi endpoints...\n")
    run_command(f"cat {param_file} | gf lfi | sort -u | tee {lfi_file}", "Filtering URLs for potential LFI endpoints...\n") 
    run_command(f"cat {param_file} | grep -Ei 'redirect_url=|next=|url=|target=|rurl=|dest=|destination=|redir=|redirect_uri=|redirect=|out=|view=|loginto=|image_url=|go=|return=|returnTo=|return_to=|checkout_url=|continue=|return_path=|success=|data=|qurl=|login=|logout=|ext=|clickurl=|goto=|rit_url=|forward_url=|forward=|pic=|callback_url=|jump=|jump_url=|clicku=|originUrl=|origin=|Url=|desturl=|u=|page=|u1=|action=|action_url=|sp_url=|service=|recurl=|uri=|q=|link=|src=|tcsrc=|linkAddress=|location=|burl=|request=|backurl=|return_uri=|RedirectUrl=|Redirect=|ReturnUrl=' | sort -u | tee {redirect_file}", "Filtering URLs for potential REDIRECT endpoints...\n")
    run_command(f"nuclei -l {live_file} -t {template_path} | tee {nuclei_file}", "Running Nuclei (All Severities)...\n")

    # Gather results
    summary = {
        "subdomains": get_output_lines(subs_file),
        "live_subdomains": get_output_lines(live_file),
        "js_files": get_output_lines(js_file),
        "wayback_urls": get_output_lines(wayback_file),
        "param_urls": get_output_lines(param_file),
        "xss_urls": get_output_lines(xss_file),
        "sqli_urls": get_output_lines(sqli_file),
        "lfi_urls": get_output_lines(lfi_file),
        "redirect_urls": get_output_lines(redirect_file),
        "nuclei_findings": len(get_output_lines(nuclei_file))
    }

    # Console Summary
    print(f"\n{Fore.GREEN}[✔] Recon completed for: {domain}\n")
    print("[Summary]")
    print(format_count("Total Subdomains Found", len(summary['subdomains'])))
    print(format_count("Live Subdomains (httpx)", len(summary['live_subdomains'])))
    print(format_count("JS Files Extracted (Katana)", len(summary['js_files'])))
    print(format_count("Wayback URLs Extracted", len(summary['wayback_urls'])))
    print(format_count("Gau URLs with Params", len(summary['param_urls'])))
    print(format_count("URLs with XSS", len(summary['xss_urls'])))
    print(format_count("URLs with SQLI", len(summary['sqli_urls'])))
    print(format_count("URLs with LFI", len(summary['lfi_urls'])))
    print(format_count("URLs with REDIRECT", len(summary['redirect_urls'])))
    print(format_count("Nuclei Findings (All)", summary['nuclei_findings']))
    print("-" * 50)

    # Write summary to file (no colors)
    with open(summary_file, "w") as f:
        f.write(f"Recon Summary for: {domain}\n")
        f.write(f"{'-'*40}\n")
        f.write(f"Total Subdomains     : {len(summary['subdomains'])}\n")
        f.write(f"Live Subdomains      : {len(summary['live_subdomains'])}\n")
        f.write(f"JS Files             : {len(summary['js_files'])}\n")
        f.write(f"Wayback URLs         : {len(summary['wayback_urls'])}\n")
        f.write(f"Gau URLs             : {len(summary['param_urls'])}\n")
        f.write(f"XSS URLs             : {len(summary['xss_urls'])}\n")
        f.write(f"SQLI URLs            : {len(summary['sqli_urls'])}\n")
        f.write(f"LFI URLs             : {len(summary['lfi_urls'])}\n")
        f.write(f"REDIRECT URLs        : {len(summary['redirect_urls'])}\n")
        f.write(f"Nuclei Findings      : {summary['nuclei_findings']}\n")

# CLI entry point
def main():
    parser = argparse.ArgumentParser(description="HackRecon - Bug Bounty Recon Tool")
    parser.add_argument("-d", "--domain", required=True, help="Target domain")
    parser.add_argument("-t", "--templates", required=True, help="Path to Nuclei templates")
    parser.add_argument("-o", "--output", required=False, help="Output directory")
    args = parser.parse_args()

    check_tools()
    run_recon(args.domain, args.templates, args.output)

if __name__ == "__main__":
    main()
