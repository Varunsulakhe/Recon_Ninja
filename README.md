# Recon_Ninja

**Author:** Varun Sulakhe
**Version:** 1.0
**Category:** Bug Bounty / Web Reconnaissance / Automated Recon Tool

---

## 🔧 What is Recon_Ninja?

Recon_Ninja is a powerful and modular automated recon tool designed to streamline the bug bounty hunting and web reconnaissance process. It automates essential tasks like subdomain enumeration, JS file discovery, parameter harvesting, and vulnerability filtering (XSS, SQLi, LFI, Open Redirect), while integrating with Nuclei for fast template-based vulnerability detection.

---

## 🌐 Features

* ✅ Subdomain enumeration using **Subfinder**
* ✅ Live host detection using **Httpx**
* ✅ JS file extraction using **Katana**
* ✅ Wayback and gau URL collection
* ✅ URL parameter discovery
* ✅ Filters URLs for potential:

  * XSS
  * SQL Injection
  * Local File Inclusion (LFI)
  * Open Redirects
* ✅ Vulnerability scanning with **Nuclei** templates
* ✅ Generates colorized console summary + detailed text summary

---

## 🚀 Tools Used (Dependencies)

Ensure the following tools are installed and in your `$PATH`:

* [`subfinder`](https://github.com/projectdiscovery/subfinder)
* [`httpx`](https://github.com/projectdiscovery/httpx)
* [`waybackurls`](https://github.com/tomnomnom/waybackurls)
* [`gau`](https://github.com/lc/gau)
* [`katana`](https://github.com/projectdiscovery/katana)
* [`gf`](https://github.com/tomnomnom/gf) + patterns for `xss`, `sqli`, `lfi`
* [`nuclei`](https://github.com/projectdiscovery/nuclei)

> ⚠️ Make sure your Nuclei templates are updated!

---

## 📂 Output

Each run generates a structured directory with:

```
<output-dir>/<target-domain>/
├── subs.txt
├── livehosts.txt
├── js.txt
├── wayback.txt
├── params.txt
├── xss.txt
├── sqli.txt
├── lfi.txt
├── redirect.txt
├── nuclei.txt
└── summary.txt
```

---

## ⚙️ Usage

```bash
python3 recon.py -d <target-domain> -t <path-to-nuclei-templates> [-o output-dir]
```

### Example

```bash
python3 recon.py -d example.com -t ~/nuclei-templates -o results
```

---

## 🎓 Summary Output (Sample)

```
[Summary]
 - Total Subdomains Found    : 42
 - Live Subdomains (httpx)   : 19
 - JS Files Extracted        : 35
 - Wayback URLs Extracted    : 1103
 - Gau URLs with Params      : 953
 - URLs with XSS             : 12
 - URLs with SQLI            : 7
 - URLs with LFI             : 3
 - URLs with REDIRECT        : 4
 - Nuclei Findings (All)     : 58
```

---

## 🔎 TODO (Planned Features)

* [ ] Add threading support for faster execution
* [ ] Integrate secrets detection (e.g. API keys in JS)
* [ ] Beautify & analyze inline JS
* [ ] Add support for headless crawling
* [ ] Export to JSON/CSV format

---

## 📊 Contributing

Pull requests are welcome! If you have suggestions or want to add more features/templates, feel free to fork and submit a PR.

---

## 👺 Disclaimer

This tool is intended for educational and authorized security testing purposes only. Unauthorized scanning or hacking of systems you do not own is illegal.

---

## 📢 License

MIT License - feel free to use and modify with credit.
