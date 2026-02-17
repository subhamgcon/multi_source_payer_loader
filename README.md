# Multi-Source Payer Loader

## Project Overview

This project implements a production-ready Python utility that
dynamically loads claim data into payer-specific target tables based on
command-line input parameters.

The script supports: - Loading data from CSV files - Handling manual
input (list of dictionaries) - Applying payer-specific transformations -
Object-Oriented design with method overriding - Clean command-line
execution using argparse

------------------------------------------------------------------------

## Architecture Overview

CLI Input\
→ Data Preparation (Function Overloading)\
→ Data Transformation (Pandas)\
→ Loader Class (OOP + Method Overriding)\
→ Target Table Resolution

------------------------------------------------------------------------

## Technologies Used

-   Python 3.x
-   Pandas
-   argparse
-   functools.singledispatch
-   Object-Oriented Programming (Inheritance & Overriding)

------------------------------------------------------------------------

## Project Structure

multi_source_payer_loader/ │ ├── payer_loader.py ├── anthem_data.csv ├──
cigna_data.csv ├── requirements.txt └── README.md

------------------------------------------------------------------------

## Setup Instructions

1.  Create Virtual Environment (Recommended)

python -m venv venv\
venv`\Scripts`{=tex}`\activate  `{=tex}

2.  Install Dependencies

pip install -r requirements.txt

requirements.txt should contain:

pandas

------------------------------------------------------------------------

## Execution Instructions

### Case A: Load Data from CSV

Anthem Example:

python payer_loader.py --source "./anthem_data.csv" --payer anthem

Cigna Example:

python payer_loader.py --source "./cigna_data.csv" --payer cigna

------------------------------------------------------------------------

### Case B: Manual Input (Simulated)

python payer_loader.py --payer manual

This triggers the overloaded function to handle a list of dictionaries
directly.

------------------------------------------------------------------------

## Key Implementation Concepts

1.  Argument Parser\
    Uses argparse to dynamically pass:

-   --source → file path\
-   --payer → target payer (anthem, cigna, manual)

2.  Function Overloading (Simulated)\
    Implemented using @singledispatch.

-   If input is a string → Reads CSV file\
-   If input is a list → Converts to Pandas DataFrame

3.  Data Transformation\
    Using Pandas:

-   Adds ingestion_timestamp column\
-   Converts service_date to datetime\
-   Applies payer-specific business rule (Anthem adjustment example)

4.  OOP & Method Overriding\

-   BaseLoader defines interface (load method)\
-   PayerLoader inherits BaseLoader\
-   load() method is overridden to dynamically resolve target table

------------------------------------------------------------------------

## Production-Ready Features

-   No hardcoded payer logic inside main flow\
-   Modular function design\
-   Clean separation of data preparation, transformation, and loading\
-   Extensible architecture for adding new payers\
-   CLI-compatible for scheduling & automation

------------------------------------------------------------------------

## How to Extend

-   Connect loader to actual Snowflake database\
-   Add logging instead of print statements\
-   Add input validation layer\
-   Add unit testing\
-   Convert into deployable package

------------------------------------------------------------------------

## Author

Subham Ghosh\
Data Engineering Assignment Submission
