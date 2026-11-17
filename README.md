# Spaceflight & Biology Data Curator
_**Current Version:** 0.0.14_  
_**License:** MIT License_

## About
This is intended to be an OSDR discovery engine. While looking through the NASA Open Science Data Repository (OSDR) Search, I noticed that when filtering through mission and study data, I could not sort chronologically by the start or end dates of missions, alphabetically with clean normalization, by Principal Investigator/author, or by study scale. To solve this, I started architecting a local Extract, Transform, and Load (ETL) pipeline to transform the raw, nested JSON endpoints into a queryable relational catalog.

This project is a quality-of-life tool for researchers, OSDR Analysis Working Group (AWG) members, and citizen scientists searching for datasets on the Open Science Data Repository. Because OSDR merges decades of legacy archives stored in deeply nested ISA-Tab structures, cross-study sorting and metadata auditing are difficult to perform directly in the browser. By flattening and standardizing these endpoints into a local SQL database, users can:
- **Sort and Filter Locally:** Query studies by alphabetical title (`A-Z`), mission launch/end dates, lead investigator, and dataset size.
- **Audit Metadata Completeness:** Identify studies with missing mission timestamps or incomplete fields before downloading multi-gigabyte raw files.
- **Eliminate Manual JSON Parsing:** Query flattened relational tables using standard SQL instead of writing custom API scraping scripts for every meta-analysis.

## AI Disclosure
All code by contributors may have been generated initially with the assistance of Generative AI. AI will never be used as a substitute for human architectural oversight, data validation, or debugging. Every script, schema, and query in this repository is strictly understood, commented, documented, reviewed, revised, and tested by a human before being committed.

## Installation
### Setup & Execution
#### Windows
TK..
#### Linux
TK..
#### MacOS
TK..
#### UNIX
TK..

## Project Guidelines
To keep the pipeline maintainable, modular, and easy to audit, contributors should follow these core standards:
- **Keep Scope Modular:** Maintain clear separation between Extract, Transform, and Load (idempotent database upserts).
- **Protect Ephemeral & Local Files:** Never commit raw API caches, SQLite database binaries (`.db`), or `.env` credentials to version control. Ensure `.gitignore` rules are respected prior to staging commits.
- **Idempotency First:** All database load operations must use upsert logic so re-running the pipeline never duplicates records.
- **Issue-Driven Changes:** Before submitting a Pull Request for a major schema change or new endpoint integration, open an issue to discuss the proposed transformation logic.
- **Required Coding Standards:** Before committing, ensure that your code complies with the [CODING_STANDARDS.md](CODING_STANDARDS.md) document.

## Code of Conduct
This project adheres to an open, collaborative, and respectful scientific computing environment:
- **Be Constructive:** Provide clear, technical, and respectful feedback during code reviews and issue discussions.
- **Focus on Data Integrity:** Document edge cases and API anomalies transparently rather than hardcoding silent workarounds.
- **Harassment-Free Collaboration:** Unwelcoming language, personal attacks, or dismissive behavior toward contributors of any experience level will not be tolerated.

## Contact
For any questions, comments, bug reports, or suggestions you may have:
- **GitHub Issues:** Open a ticket in the [Issues tab](https://github.com/AJ-Runyon/Spaceflight-and-Biology-Data-Curator/issues) of this repository.
- **Maintainer:** Aaron J. Runyon ([@AJ-Runyon](https://github.com/AJ-Runyon))