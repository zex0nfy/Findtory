# Findtory

🎯 **Findtory** — Finds any directory from a website using a fast, threaded brute-force approach with wordlists. Inspired by tools like `gobuster` and `dirsearch`, but made to be more user-friendly and customizable.

---

## 🧩 Features

* 🚀 Fast multithreaded directory brute-force
* 🧾 Save output results to file
* 🛠️ Custom file extensions and status codes
* 📦 Built-in wordlist ready (optional setup)
* 🔍 Progress bar (tqdm) to monitor scan status
* 🎨 Colored output for easy visual filtering

---

## 📦 Installation

### 🔧 Install from source:

```bash
git clone https://github.com/zex0nfy/Findtory.git
cd findtory
pip install -r requirements.txt
python setup.py install
```

### 📦 Or install with pip locally (editable mode):

```bash
pip install -e .
```

---

## 🚀 Usage

```bash
findtory <url> -w <wordlist> [options]
```

### ✅ Example:

```bash
findtory https://example.com -w wordlists/common.txt -e php,html -t 30 -c 200,403 -o result.txt
```

### 🔧 Options:

| Argument             | Description                                       |
| -------------------- | ------------------------------------------------- |
| `url`                | Base target URL                                   |
| `-w`, `--wordlist`   | Path to your wordlist file                        |
| `-e`, `--extensions` | Optional file extensions to try (comma-separated) |
| `-t`, `--threads`    | Number of concurrent threads (default: 10)        |
| `-c`, `--codes`      | Filter status codes (e.g. 200,301,403)            |
| `-o`, `--output`     | Save discovered paths to a file                   |
| `--timeout`          | Timeout for each request (default: 5 seconds)     |

---

## 📁 Wordlists (Optional)

You can pre-load some great wordlists into the `wordlists/` folder. Examples:

* `common.txt` — quick & general
* `raft-medium-directories.txt` — medium coverage
* `raft-large-directories.txt` — comprehensive scan
* `content-bf.txt` — content-related directories
* `dirbrute.txt` — smaller but focused

### 📥 Auto-download wordlists

Run this to grab from GitHub:

```bash
bash scripts/download-wordlists.sh
```

---

## 🧪 Requirements

* Python 3.6+
* Modules: `requests`, `colorama`, `tqdm`

These are auto-installed with:

```bash
pip install -r requirements.txt
```

---

Happy hunting with **Findtory**! 🕵️‍♂️
