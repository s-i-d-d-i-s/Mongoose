# Mongoose
Mongoose is a powerful command-line interface (CLI) tool designed to simplify the complex process of calculating capital gains tax, dividends, and interest. It provides a comprehensive, detailed report in the currency of your choice, making it easy to hand off to a professional tax consultant.

# How It Works
Mongoose follows a simple, three-step process to transform your raw broker data into a clean, professional tax report.

## 1. Initialization
When you first start Mongoose, it automatically performs a one-time setup process. This includes fetching critical external data, such as historical foreign exchange (Forex) rates, that are essential for accurate calculations in your chosen currency.

## 2. Normalization & Data Cleanup
This is where the magic happens. Mongoose takes the raw transaction data from your various brokers and performs a crucial normalization step. An intelligent algorithm processes this data, converting it into a standardized format that the tool can understand. This process also includes a cleanup routine to correct common data inconsistencies and errors, ensuring the highest level of accuracy for your report. It's important to note that the data needed and the normalization process are very different for each broker. We provide specific instructions on how to get the exact data Mongoose needs to function correctly.

## 3. Capital Gains Calculation & Reporting
Once the data is clean and normalized, Mongoose runs a sophisticated algorithm over the dataset. It precisely calculates capital gains, tracks dividends, and logs interest income. The final output is a single, detailed report that you can present directly to your tax consultant, saving you countless hours of manual work.

# Features
- Multi-Currency Support: Calculate taxes in your preferred currency.

- Automated Forex Fetching: Mongoose handles the retrieval of historical exchange rates for you.

- Data-Agnostic Input: The normalization engine is designed to handle data from a variety of sources.

- Professional-Grade Reports: The generated report is comprehensive and includes all necessary details for tax professionals.

- CLI-Based: Use it directly from your terminal for speed and efficiency.

# Getting Started

## 1. Initialize Mongoose and fetch necessary data.

```
python mongoose.py init
```


## 2 Import your broker data and normalize it.

```
python mongoose.py normalize --broker ["IBKR"/"T212"] --file [path_to_file]
```
This would generate a `normalized/IBKR.json` or `normalized/T212.json` in the root folder.

## 3. Generate your final tax report.

```
python mongoose.py generate --report tax_report.pdf --currency USD
```
This would generate a report based on all the files in the `normalized` folder.

## Supported Brokers
Mongoose is continually adding support for more brokers. Currently, the normalization engine is compatible with data from:

1. Interactive Brokers (Code: IBKR)
2. Trading 212 (Code: T212)

If you'd like to see a new broker supported, please open an issue on the repository!