# Generate Tracking logic

Generate Tracking compares a **Raw scanner workbook/sheet** against a **Master tracking workbook/sheet**. The Master workbook is required because the tab must decide which current Raw findings are already tracked and which findings are new.

---

## 1. Required inputs

Generate Tracking requires all of these values before the Run button is enabled:

- Master Excel file.
- Master sheet.
- Raw scanner Excel file.
- Raw sheet.
- Output `.xlsx` path.

The workflow is intentionally not optional-master logic. If the Master file/sheet is missing, the tab must not run.

---

## 2. Main workflow sequence

The tab executes this sequence:

1. Validate selected Master file/sheet, Raw file/sheet, and output path.
2. Parse the Raw file.
3. Parse the Master file.
4. Compare Raw rows against Master rows with `classify_new_old(raw_df, master_df)`.
5. Split Raw findings into:
   - `new_df`: Raw rows not found in Master.
   - `old_df`: Raw rows found in Master.
6. Build `unique_df` from all Raw/Total findings.
7. Write the output workbook.

In short:

```text
Raw scanner data + Master tracking data
  ↓
Compare by Name + Host/Image + Port + CVE
  ↓
Total / New / Old / Unique workbook output
```

---

## 3. Output workbook sheets

Generate Tracking writes these workbook sheets:

| Sheet | Meaning |
|---|---|
| `Dashboard` | Summary/dashboard sheet. |
| `Total Vulnerabilities` | All vulnerabilities from the Raw file. |
| `New Vulnerabilities` | Raw vulnerabilities that are not matched in Master. |
| `Old Vulnerabilities` | Raw vulnerabilities that are matched in Master. |
| `Unique Vulnerabilities` | Aggregated version of Total Vulnerabilities. |
| `Disposition` | Disposition/reference sheet. |

The required DataFrame-to-sheet routing is:

| DataFrame | Output sheet | Meaning |
|---|---|---|
| `total_df` | `Total Vulnerabilities` | All parsed Raw findings. |
| `new_df` | `New Vulnerabilities` | Raw findings not matched in Master. |
| `old_df` | `Old Vulnerabilities` | Raw findings matched in Master. |
| `unique_df` | `Unique Vulnerabilities` | Aggregated Raw/Total findings. |

---

## 4. Comparison key

Raw and Master rows are compared with a composite key built from these logical fields:

- `Name`
- `Host / Image`
- `Port`
- `CVE`

The comparison logic supports scanner-specific aliases:

```python
_KEY_ALIASES = {
    "Name": ("Name", "Title", "Vulnerability", "Plugin Name"),
    "Host / Image": ("Host / Image", "Host", "IP", "DNS", "Hostname", "Image"),
    "Port": ("Port", "Service Port", "TCP Port", "UDP Port"),
    "CVE": ("CVE", "CVE ID", "CVE IDs", "CVEs", "Vulnerability ID"),
}
```

This lets the same tab compare normalized template rows and 3UK + Qualys rows. For example, 3UK + Qualys rows can compare:

```text
Title + IP + Port + CVE ID
```

against template-style rows:

```text
Name + Host / Image + Port + CVE
```

---

## 5. Total Vulnerabilities

`Total Vulnerabilities` means:

> All vulnerability rows from the Raw file.

It is not only New. It is not only Old. It is the full parsed Raw scanner data.

For non-3UK + Qualys selections, Raw data is parsed into the universal template columns, so:

```python
total_df = raw_df
```

For 3UK + Qualys selections, Raw and Master are first parsed in the Qualys Total format for comparison. Before workbook output, Raw data is mapped into the universal template layout:

```python
total_df = build_3uk_qualys_template_sheet_df(raw_df)
```

The 3UK + Qualys raw parser still understands these Qualys Total columns:

```python
THREE_UK_QUALYS_TOTAL_COLUMNS = [
    "IP",
    "Network",
    "DNS",
    "NetBIOS",
    "Tracking Method",
    "OS",
    "IP Status",
    "QID",
    "Title",
    "Vuln Status",
    "Type",
    "Severity",
    "Port",
    "Protocol",
    "FQDN",
    "SSL",
    "First Detected",
    "Last Detected",
    "Times Detected",
    "Date Last Fixed",
    "CVE ID",
    "Vendor Reference",
    "Bugtraq ID",
    "CVSS",
    "Criticality",
    "CVSS Base",
    "CVSS Temporal",
    "Product",
    "CVSS Environment",
    "CVSS3",
    "CVSS3 Base",
    "CVSS3 Temporal",
    "Threat",
    "Impact",
    "Solution",
    "Exploitability",
    "Associated Malware",
    "Results",
    "PCI Vuln",
    "Ticket State",
    "Instance",
    "Category",
]
```

However, the current Generate Tracking output writes Total/New/Old/Unique vulnerability sheets in the universal template layout.

---

## 6. New Vulnerabilities

`New Vulnerabilities` means:

> Raw vulnerabilities that do not match anything in the Master tracking sheet.

In simple terms:

```text
Raw row not found in Master = New Vulnerability
```

The comparison function builds keys from Raw and Master. If a Raw key does not exist in the Master key set, that Raw row becomes part of `new_df`.

For 3UK + Qualys, `new_df` is converted into universal template columns before writing. For non-3UK + Qualys, the parser already returns template columns.

---

## 7. Old Vulnerabilities

`Old Vulnerabilities` means:

> Raw vulnerabilities that do match the Master tracking sheet.

In simple terms:

```text
Raw row found in Master = Old Vulnerability
```

Old does not mean every row from the Master file. Old means the current Raw vulnerability is already present/tracked in Master.

For 3UK + Qualys, `old_df` is converted into universal template columns before writing. For non-3UK + Qualys, the parser already returns template columns.

---

## 8. Unique Vulnerabilities

`Unique Vulnerabilities` means:

> A grouped/aggregated version of Total Vulnerabilities.

It is built from all Raw vulnerabilities, not only New and not only Old.

For non-3UK + Qualys selections:

```python
unique_df = aggregate_unique(raw_df)
```

The generic unique logic groups by:

- `Name`
- `CVE`
- `Host / Image`

Repeated values are merged with comma-separated de-duplication. For example, repeated ports can become:

```text
80, 443, 8080
```

For 3UK + Qualys selections:

```python
unique_df = build_3uk_qualys_unique_sheet_df(raw_df)
```

That builder maps Qualys rows into template columns, groups equivalent findings, and returns the universal template layout.

---

## 9. Universal template columns

The Generate Tracking vulnerability output sheets use these universal template columns:

```text
Scanner ID
CVE
CVSS v2.0 Base Score
Risk
Host / Image
Protocol
Port
Name
Synopsis
Description
Solution
See Also
Plugin Output
CVSS v3.0 Base Score
CVSS v3.0 Temporal Score
Release Remediation Plan
Release Remediation Date
Expert Severity
Expert Score
Remediation Reference ID
Disposition
VAMS (PSL comments)
MSS Comments
```

Current output behavior:

| Sheet | Layout |
|---|---|
| `Total Vulnerabilities` | Universal template columns. |
| `New Vulnerabilities` | Universal template columns. |
| `Old Vulnerabilities` | Universal template columns. |
| `Unique Vulnerabilities` | Universal template columns. |

---

## 10. 3UK + Qualys mapping

For 3UK + Qualys:

1. Raw and Master are first read in Qualys Total format with `build_3uk_qualys_total_sheet_df()`.
2. Raw and Master are compared using alias-aware keys.
3. `total_df`, `new_df`, and `old_df` are mapped into the universal template layout with `build_3uk_qualys_template_sheet_df()`.
4. `unique_df` is built from Raw data with `build_3uk_qualys_unique_sheet_df()`.
5. The workbook writer writes the template-layout output sheets.

Important current behavior:

```python
total_df = build_3uk_qualys_template_sheet_df(raw_df)
new_df = build_3uk_qualys_template_sheet_df(new_df)
old_df = build_3uk_qualys_template_sheet_df(old_df)
unique_df = build_3uk_qualys_unique_sheet_df(raw_df)
```

The Qualys-to-template mapper converts fields like:

| Qualys field | Template field |
|---|---|
| `QID` | `Scanner ID` |
| `CVE ID` | `CVE` |
| `CVSS Base` | `CVSS v2.0 Base Score` |
| `Criticality` | `Risk` |
| `IP` | `Host / Image` |
| `Title` | `Name` |
| `Impact` | `Synopsis` / `Description` |
| `Vendor Reference` | `See Also` |
| `Results` | `Plugin Output` |
| `CVSS3 Base` | `CVSS v3.0 Base Score` |

The mapper also preserves VAMS fields when those fields already exist in the source data.

---

## 11. Non-3UK + Qualys flow

For every other project/scanner selection:

1. Raw is parsed directly through the normal scanner parser.
2. Master is parsed through the normal scanner parser.
3. Raw and Master are normalized to template columns.
4. `classify_new_old(raw_df, master_df)` splits Raw into New and Old.
5. `aggregate_unique(raw_df)` builds Unique from all Raw/Total data.
6. All vulnerability output sheets are written in template layout.

---

## 12. Example

Assume Master has these tracked vulnerabilities:

| Name | Host / Image | Port | CVE |
|---|---|---:|---|
| Apache Vuln | `10.0.0.1` | 443 | `CVE-1111` |
| OpenSSL Vuln | `10.0.0.2` | 443 | `CVE-2222` |

Raw has these current scan vulnerabilities:

| Name | Host / Image | Port | CVE |
|---|---|---:|---|
| Apache Vuln | `10.0.0.1` | 443 | `CVE-1111` |
| Nginx Vuln | `10.0.0.3` | 80 | `CVE-3333` |
| OpenSSL Vuln | `10.0.0.2` | 443 | `CVE-2222` |

The output will be:

| Output sheet | Rows |
|---|---|
| `Total Vulnerabilities` | Apache Vuln, Nginx Vuln, OpenSSL Vuln |
| `New Vulnerabilities` | Nginx Vuln |
| `Old Vulnerabilities` | Apache Vuln, OpenSSL Vuln |
| `Unique Vulnerabilities` | Aggregated Raw/Total rows |

If Raw has duplicate equivalent findings, Unique merges repeated values with comma-separated de-duplication.

---

## 13. One-line summary

Generate Tracking takes all Raw vulnerabilities as Total, compares each Raw row against the required Master tracking sheet, puts unmatched Raw rows into New, matched Raw rows into Old, aggregates all Raw rows into Unique, and writes all vulnerability output sheets in the universal template layout.
