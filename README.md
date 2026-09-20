# PoC-UK-VAT-Identifier-Discovery
Proof of Concept data pipeline for discovering and validating UK VAT numbers using Python, Docker, and the HMRC Developer API.

<img width="1846" height="941" alt="image" src="https://github.com/user-attachments/assets/9a9b42c5-da3a-4f38-9b23-0b9ca193ccee" />


This repository contains a Proof of Concept (PoC) data pipeline designed to discover, extract, and validate UK VAT numbers from corporate websites.

Prerequisites
Docker: The entire execution environment is containerized. You do not need to install Python or any dependencies locally on your host machine.

<img width="1899" height="433" alt="image" src="https://github.com/user-attachments/assets/a0b92906-6aba-4c57-8998-723cdd988dab" />

Project Structure
source/: Contains the Python scripts for discovery, scraping, and HMRC validation.

data/: Contains the .csv data samples.

**Data Flow (The 3 CSV Iterations):**
*   `sample_500_active_companies.csv`: The initial cleaned data sample extracted from the 2GB raw bulk file.
*   `sample_with_domains.csv`: The dataset produced after running the domain discovery module, which also incorporates the two manually injected test cases for scraper validation.
*   `sample_with_extracted_vat.csv`: The final output containing the newly populated column with the VAT numbers extracted via Regex.
Dockerfile & requirements.txt: Docker environment configuration.

Note on Data & Version Control
To adhere to Git best practices, the original 2GB bulk CSV file has been explicitly excluded from this repository via .gitignore. The PoC scripts are configured to run against data/sample_with_domains.csv.

This sample includes carefully selected known-good entities (e.g., Waterstones, British Council) to demonstrate extraction capabilities, architectural limitations, and structural edge-cases. To test the pipeline on the full dataset, simply place the large CSV into the data/ directory and update the target filename in the source scripts.

## Project Structure & Pipeline Flow
The pipeline is broken down into modular, sequential scripts located in the `source/` directory:

*   **`01_data_discovery.py` & `02_extract_sample.py`**: Handles the ingestion of the massive 2GB Companies House dataset. Since files of this size cannot be opened in standard spreadsheet software, I used `pandas` to programmatically chunk, filter (Active companies only), and extract a representative test sample.
*   **`03_domain_discovery.py`**: Attempts to find corporate domains using open-web search APIs (DuckDuckGo), highlighting the limitations of non-deterministic domain mapping.
*   **`04_vat_scraper.py`**: The targeted web crawler using `requests` and `BeautifulSoup` to parse HTML and extract 9-digit VAT identifiers via Regex.
*   **`05_hmrc_validator.py`**: The final verification module querying the HMRC Developer API using Python's standard `json` library.

**Dependency Strategy:**
Core data manipulation and DOM parsing rely on `pandas` and `beautifulsoup4` (managed via `requirements.txt`). However, to keep the Docker image lightweight, standard operations (like Regex matching and JSON parsing) strictly utilize Python's built-in standard libraries.

How to Run
1. Build the Docker Image
Open your terminal in the root directory of the project and run the following command to build the environment:
docker build -t veridion-env .
2. Execute the Pipeline Scripts
You can run each module individually inside the container using the commands below. The volume mount (-v) ensures the scripts can read from your local data/ folder.

Run the VAT Scraper:
docker run -it --rm -v "${PWD}:/app" veridion-env python source/04_vat_scraper.py

<img width="1750" height="944" alt="image" src="https://github.com/user-attachments/assets/806e5155-f30f-42cb-9841-a93b5027f763" />

Run the HMRC API Validator (Final Verification):
docker run -it --rm -v "${PWD}:/app" veridion-env python source/05_hmrc_validator.py

<img width="1779" height="919" alt="image" src="https://github.com/user-attachments/assets/a9ec9571-e863-4fc3-95a2-4821415a190c" />

Methodology & Debate Topics
For a comprehensive breakdown of the domain discovery limits, anti-bot observations, validation strategy, and answers to the Debate Topics, please refer to the attached document: Ceausu Eugen-Stefan VAT Identifier Discovery assessment_solve.docx.
