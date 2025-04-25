# IVIX Crypto Scraping Project

This project contains two main components:
1. Crypto Watchlist Scraper (supports both HTML and API parsing modes)
2. Price Pulse Scraper

## Project Structure

```
IVIX/
├── crypto_watchlist/
│   ├── __init__.py
│   ├── api_parser.py
│   ├── crypto.log
│   ├── csv_tools.py
│   ├── html_parse.py
│   ├── main.py
│   ├── Makefile
│   ├── requirements.txt
│   └── schemas.py
└── price_pulse/
    ├── .env.example
    ├── config.py
    ├── main.py
    ├── Makefile
    └── requirements.txt
```

## Installation

### 1. Crypto Watchlist Scraper

#### Prerequisites
- Python 3.x
- Make (for automatic installation - Unix systems only)

#### Using Makefile (Unix/Linux/Mac)
The Makefile automatically handles virtual environment creation and dependency installation:
```bash
cd crypto_watchlist
make up  # This will install dependencies and run the script
```

#### Manual Installation (All Platforms)
If you prefer manual setup or are on Windows:
1. Navigate to the crypto_watchlist directory:
   ```bash
   cd crypto_watchlist
   ```

2. Create and activate virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

### 2. Price Pulse Scraper

#### Prerequisites
- Python 3.x
- Make (for automatic installation - Unix systems only)

#### Using Makefile (Unix/Linux/Mac)
The Makefile automatically handles virtual environment creation and dependency installation:
```bash
cd price_pulse
make up  # This will install dependencies and run the script
```

#### Manual Installation (All Platforms)
If you prefer manual setup or are on Windows:
1. Navigate to the price_pulse directory:
   ```bash
   cd price_pulse
   ```

2. Create and activate virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Copy the example environment file:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` file with your configuration

## Running the Applications

### Crypto Watchlist Scraper

The scraper supports two parsing modes:
- **HTML mode**: Parses data from HTML pages
- **API mode**: Retrieves data via API endpoints

#### Using the Makefile (recommended - Unix only):
```bash
make up  # Runs with defaults: PARSE_TYPE=html, PAGES=5
```

#### Makefile Arguments:
- First argument: PARSE_TYPE (optional) - "html" or "api" (default: "html")
- Second argument: PAGES (optional) - number of pages to parse (default: 5)

The Makefile automatically:
- Creates a virtual environment
- Installs dependencies
- Runs the script

#### Manual Execution:
```bash
# Run with default values
python3 main.py

# Run with specific parse type and pages
python3 main.py html 5  # HTML mode, 5 pages
python3 main.py api 10  # API mode, 10 pages
```

#### Command-line Arguments:
- First argument parse type (optional) - "html" or "api" (default: "html")
- Second argument pages to parse (optional) - number of pages to parse (default: 5)

#### Output:
- HTML mode: Creates `crypto_watchlist_html.csv`
- API mode: Creates `crypto_watchlist_api.csv`

### Price Pulse Scraper

#### Using the Makefile (recommended - Unix only):
```bash
make up  # Automatically installs dependencies and runs the script
```

#### Manual Execution:
```bash
python3 main.py
```

## Performance

### Crypto Watchlist Scraper Performance Comparison

#### HTML Mode
- Total pages parsed: 5
- Total execution time: 41.53 seconds
- Average time per page: 8.31 seconds
- Total coins parsed: 500

#### API Mode
- Total pages parsed: 5
- Total execution time: 0.46 seconds
- Average time per page: 0.09 seconds
- Total coins parsed: 500

### Performance Comparison

The API mode is significantly faster than the HTML mode:
- API mode: ~0.09 seconds per page
- HTML mode: ~8.31 seconds per page
- The API mode is approximately 90x faster than the HTML mode

## Features

### Crypto Watchlist Scraper
- **Dual Mode Operation**: Supports both HTML and API parsing methods in the same application
- **Automatic Installation**: Makefile handles virtual environment and dependencies (Unix systems)
- **Configurable Parameters**: Choose parsing mode and number of pages via command-line arguments
- **CSV Output**: Separate CSV files for each parsing mode
- **Data Validation**: Schema validation for parsed data
- **CSV Tools**: Utility functions for data handling

### Price Pulse Scraper
- **API-based**: Fast data retrieval via API endpoints
- **Automatic Installation**: Makefile handles setup (Unix systems)
- **Environment Configuration**: Uses `.env` file for configuration
- **Efficient Processing**: Optimized for speed
