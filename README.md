# UK VAT Number Discovery – Research & Proof of Concept

## 1. Project Overview

This project investigates whether a reliable UK VAT number dataset can be built for approximately 40,000 suppliers using publicly available information and official verification services.

The main objective is to discover missing VAT numbers, verify potential matches and assess the feasibility of maintaining an accurate dataset over time.

The project combines manual research, source evaluation and a Python-based proof of concept using the HMRC VAT Check API.

**Key principle: Accuracy is more important than coverage.** An incorrectly assigned VAT number can be more damaging than a missing one.

## 2. Understanding the Problem

The starting point is the supplier record, not the VAT number.

A supplier record, a legal company and a VAT registration are not necessarily the same entity. Suppliers may be incorporated companies, sole traders or other types of businesses.

The problem involves two distinct stages:

- **Discovery:** Finding a potential VAT number associated with a supplier.
- **Verification and entity resolution:** Confirming that the number is registered and belongs to the correct legal entity.

HMRC can validate a supplied VAT number, but its checking service does not provide a general search by company name.

A missing result must not automatically be interpreted as evidence that a company is not VAT registered.

## 3. Research and Data Sources

Several sources and approaches were investigated.

### 3.1 Company Websites

Some companies publish their VAT numbers in legal notices, company registration details or supplier information pages.

Examples investigated:

- [Rolls-Royce – Legal Information](https://www.rolls-royce.com/site-services/legal-information.aspx)
- [AstraZeneca UK – Legal Notice](https://www.astrazeneca.co.uk/legal-notice-and-terms-of-use)
- [Edwards Vacuum – Supplier Information](https://www.edwardsvacuum.com/en-uk/supplier-info-emea#accordion-3d61e4b1e7-item-b154f83027)
- [GBG – Business Terms](https://www.gbgplc.com/legal-and-regulatory/business-terms-and-intellectual-property/#terms)
- [HP UK – Company Registration Details](https://www.hp.com/gb-en/company-registration-details.html)

Company websites can provide useful discovery evidence, but VAT numbers are not consistently published.

### 3.2 Google Search

Manual searches using exact company names and VAT-related keywords can identify potential VAT numbers in websites, PDFs and other public documents.

However, search results are not a structured or complete source. Similar company names can also create entity-matching risks.

### 3.3 VAT-Lookup

[VAT-Lookup](https://www.vat-lookup.co.uk/) was investigated as a third-party source for discovering VAT numbers using company names.

It may help identify candidates, but its coverage, reliability and update frequency need further evaluation.

A missing result only means that the company was not found in that particular dataset.

### 3.4 HMRC VAT Checker

[HMRC VAT Checker](https://www.tax.service.gov.uk/check-vat-number/enter-vat-details) provides official validation of supplied VAT numbers.

It is useful for verification, but it does not solve the initial discovery problem.

### 3.5 Companies House

[Companies House](https://www.gov.uk/government/organisations/companies-house) provides official company information and can help identify the correct legal entity.

However, it is not a complete source of company VAT numbers.

## 4. Experiments and Findings

### 4.1 Manual Research

Manual searches demonstrated that VAT numbers can sometimes be discovered through company websites, search engines and third-party databases.

However, availability varies between companies and no single source provides complete coverage.

### 4.2 Automated HMRC Checker Testing

A Python browser automation experiment was used to investigate automated VAT validation through the public HMRC checker.

During testing, HTTP 429 (Too Many Requests) responses were encountered.

This demonstrated that repeated automated requests to the public checker are subject to restrictions. Browser automation should not be assumed to be suitable for large-scale validation.

### 4.3 Checksum Enumeration

UK VAT numbers generally contain nine digits and include a checksum mechanism.

I considered whether generating possible numbers, filtering them through the checksum and submitting candidates to HMRC could be used to discover registrations.

I rejected this as a practical discovery strategy because:

- A checksum only checks mathematical validity, not registration status.
- A very large number of possible combinations would remain.
- HMRC may impose request limits.
- A valid number does not identify the supplier it belongs to.
- Similar company names create a risk of incorrect associations.

Most importantly, this approach does not directly solve the problem of finding VAT numbers for the specific 40,000 suppliers.

Checksum validation is more appropriate as a preliminary quality filter for numbers discovered through other sources.

## 5. Proof of Concept – Python and HMRC API

A Python proof of concept was developed to investigate the HMRC VAT Number Check API.

The implementation includes:

- Authentication using HMRC API credentials.
- Individual VAT number checks.
- Multiple VAT number checks.
- CSV input and output.
- Result cleaning and categorisation.
- Environment variables for keeping credentials separate from source code.

### 5.1 Project Structure

```text
uk-vat-research/
│
├── discovery/
├── verification/
│   ├── api_check.py
│   ├── check_for_one.py
│   └── check_for_all.py
│
├── processing/
├── data/
│   └── vat_numbers.txt
│
├── results/
│   ├── vat_checks.csv
│   ├── vat_results.csv
│   └── vat_results_clean.csv
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### 5.2 Sandbox vs Production

The HMRC Sandbox was used to test the API authentication and request workflow.

Sandbox responses use simulated test data and cannot be treated as confirmation of real-world VAT registrations.

Production access and appropriate credentials are required to validate real VAT registrations through the API.

### 5.3 Quantitative Results – VAT Number Verification

A total of **50 VAT number verification attempts** were recorded during the experiment.

| Result | Count | Percentage |
|---|---:|---:|
| VALID | 23 | 46.0% |
| NOT_FOUND | 10 | 20.0% |
| RATE_LIMITED | 17 | 34.0% |
| **Total** | **50** | **100%** |

Out of the 50 attempts, 33 returned a conclusive response, while 17 were rate-limited.

Among the 33 conclusive responses:

- 23 (69.7%) returned valid VAT registration details.
- 10 (30.3%) returned no result.

**Interpretation and limitations:**

- The 23 VALID responses demonstrate that the verification process returned VAT registration details for those candidate numbers.
- A VALID response does not, by itself, prove that the VAT number belongs to the intended supplier. Entity-level name and address matching is still required.
- NOT_FOUND should not automatically be interpreted as proof that a company is not VAT-registered.
- RATE_LIMITED responses were treated as inconclusive rather than invalid.
- This was a limited technical experiment, not a statistically representative sample of the 40,000 suppliers.
- These figures should therefore not be interpreted as expected VAT discovery coverage or overall precision.

The results highlight two separate challenges: obtaining a verification response reliably and correctly associating a VAT registration with the intended supplier.

### 5.4 Interpreting Results

The results must distinguish between:

- **VALID:** The checker returned valid VAT registration details for the supplied number.
- **NOT_FOUND:** The supplied number was not found in the checker.
- **RATE_LIMITED:** The request was restricted.
- **TECHNICAL_ERROR:** The request could not be completed successfully.
- **UNVERIFIED:** The candidate has not received a successful verification.

A successful VAT validation does not automatically prove that the number belongs to the intended supplier. The registered business name and address must also be compared with supplier records.

The 50-record experiment and the API Sandbox integration test should be interpreted separately: the Sandbox demonstrated the authentication and request workflow, while Sandbox responses do not establish real-world registration status.

## 6. Data Quality and Maintenance

Companies continuously register and deregister for VAT. Therefore, the dataset should preserve both current status and historical observations.

I would separate company information from VAT registration information.

### 6.1 Suggested Data Model

**Companies**

| company_id | company_name | company_number |
|---|---|---|
| 001 | ABC Manufacturing Ltd | 12345678 |
| 002 | XYZ Supplies Ltd | 87654321 |

**VAT Registrations**

| company_id | vat_number | status |
|---|---|---|
| 001 | GB123456789 | ACTIVE |
| 002 | GB987654321 | DEREGISTERED |

Suggested statuses:

- `ACTIVE` – registration confirmed as active.
- `DEREGISTERED` – registration confirmed as cancelled.
- `UNKNOWN` – current status is not known.
- `UNVERIFIED` – candidate discovered but not verified.
- `REVIEW_REQUIRED` – conflicting information requires investigation.

A separate VAT status history table should store the VAT number, observed status and date of each check.

This preserves historical observations instead of simply overwriting previous information.

### 6.2 Refresh Strategy

Not all suppliers require the same verification frequency.

I would prioritise:

- Suppliers with frequent monthly invoices.
- VAT numbers with previous status changes.
- Suppliers with conflicting information.
- Records that have not been checked recently.

A failed request or HTTP 429 response must never be interpreted as deregistration. It means verification could not be completed.

### 6.3 Data Quality Monitoring

The system should identify potential anomalies, including:

- The same VAT number associated with multiple unrelated companies.
- Significant differences between supplier and HMRC business names.
- Address mismatches.
- VAT numbers discovered only through weak or unverified sources.
- Repeated verification failures.

## 7. Scalability and Commercial Considerations

Scaling the proof of concept to approximately 40,000 suppliers would require additional resources and controls.

Potential requirements include:

- HMRC Production API access.
- Automated website crawling where permitted.
- PDF extraction and document processing.
- A central database with historical records.
- Monitoring and retry mechanisms.
- Human review for ambiguous company-to-VAT matches.
- Source-level quality monitoring.

Potential bottlenecks include source coverage, API access limits, entity resolution and manual review requirements.

Before using any source commercially, I would assess its terms of use, permitted automated access, copyright and database rights, data provenance, update frequency, stability and cost.

Public accessibility does not automatically imply permission for commercial reuse.

A production pilot should measure processing time, discovery yield, verification success rate, manual-review workload and cost per supplier before committing to a full 40,000-supplier rollout.

## 8. Preferred Sources and Recommendations

| Source | Main purpose | Assessment |
|---|---|---|
| Companies House | Legal entity identification | Preferred |
| HMRC VAT Check API | VAT verification | Preferred |
| Supplier-provided invoices and documents | Candidate discovery | Preferred |
| Company websites | Candidate discovery | Useful, subject to rights |
| VAT-Lookup | Candidate discovery | Requires further evaluation |
| Google Search | Manual research | Useful for research, not assumed suitable for automated production scraping |
| Commercial directories and marketplaces | Candidate discovery | Requires licensing and access review |

I would use multiple discovery sources and rely on HMRC for official VAT verification.

## 9. How to Run

### Requirements

Python 3 and the dependencies listed in `requirements.txt` are required.

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

### Environment Variables

Create a local `.env` file in the project root:

```env
HMRC_CLIENT_ID=your_client_id
HMRC_CLIENT_SECRET=your_client_secret
```

The `.env` file is excluded from Git using `.gitignore`.

Never commit real API credentials to the repository.

### Run the API Check

```bash
python verification/api_check.py
```

The current implementation uses the HMRC Sandbox endpoint.

Real VAT validation through the API requires appropriate HMRC Production access and credentials.

## 10. Limitations and Future Improvements

This project is a research exercise and proof of concept, not a complete UK VAT reference dataset.

The main limitations are:

- No single complete open source of UK VAT registrations was identified.
- Company websites publish VAT information inconsistently.
- Third-party datasets require further coverage and licensing assessment.
- Sandbox API results do not establish real-world registration status.
- Production API access is required for real VAT verification through the API.
- Completeness and recall cannot be reliably measured without a representative sample with known ground truth.
- Entity resolution remains a significant source of potential false positives.
- The limited 50-attempt experiment does not establish expected discovery coverage or precision for the target supplier population.

Future work would include:

1. Obtaining HMRC Production API access.
2. Testing a representative sample of suppliers.
3. Measuring discovery rates and verified match precision.
4. Automating permitted website and document discovery.
5. Introducing human review for ambiguous matches.
6. Implementing scheduled refreshes and historical status tracking.
7. Estimating operational costs using measured processing and review times.

## 11. Conclusion

The research suggests that a UK VAT dataset can be built by combining multiple discovery sources with official HMRC verification.

However, no single source provides complete coverage, and discovering a valid VAT number is not the same as proving that it belongs to a particular supplier.

I would recommend prioritising accuracy over coverage, retaining source provenance and verification history, and treating uncertain matches as unverified rather than making unsupported associations.

The most reliable approach is a multi-source discovery process supported by official HMRC validation and robust entity resolution.

## 12. Additional Research Directions

### Bulk Web Corpora

An alternative to crawling individual company websites would be to investigate existing web corpora or commercial web indexes.

These could potentially reduce crawling costs by allowing searches across already-collected pages and documents.

However, coverage, freshness, access costs and commercial reuse rights would need to be evaluated before relying on such data in production.

### Adjacent Identifiers

I would also investigate whether VAT numbers can be discovered through relationships with other company identifiers.

For example, company registration numbers, legal entity names and registered addresses can help establish identity across different sources.

However, these identifiers should not be assumed to directly reveal a VAT number. Their main value may be improving entity resolution and reducing incorrect matches.

### International Expansion

The UK discovery problem should not automatically be assumed to apply to other countries.

Before expanding into Germany or another European market, I would investigate:

- Whether VAT numbers are publicly searchable by company name.
- Whether official registries provide bulk access.
- Whether verification services support automated checks.
- Whether the same legal entity matching problems exist.

I would prioritise countries where both discovery and official verification are accessible, rather than simply replicating the UK pipeline everywhere.