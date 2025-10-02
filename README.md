# fcB2B Client Utilities

This project provides a simple Python client and example script for interacting with **fcB2B Web Services** (Stock Check and related inventory services).

It includes:
- `fcb2b_client.py` → A reusable client class that handles request signing, URL building, and GET requests against an fcB2B endpoint.
- `stock_check.py` → An interactive script that allows you to query stock availability by entering a `SupplierItemSKU`.

The implementation follows the [fcB2B Web Services Overview](docs/fcB2B_Web_Services_Overview.pdf) and [Stock Check Technical Specifications](docs/fcB2B_Web_Services_Stock_Check_Technical_Specifications.pdf).

---

## Requirements

- Python 3.9+
- `requests`
- `pyyaml`

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## Configuration

Configuration is handled via a YAML file. A sample is included:

```
config.yaml.example
```

Before running, **rename this file to `config.yaml`** and update the values:

```yaml
host: "your.fcB2Bserver.com"
apiKey: "yourApiKey"
secretKey: "yourSecretKey"

paths:
  stockcheck: "/your/rest/path/StockCheck"
  # you can add more endpoints here if needed
```

- `host` → The hostname of your fcB2B service (no scheme, just the authority).
- `apiKey` → API key assigned by your trading partner.
- `secretKey` → Shared secret used for request signing.
- `paths` → Map of service endpoints. At minimum, you need a `stockcheck` path.

---

## Usage

### Run Stock Check

To perform stock check requests interactively:

```bash
python stock_check.py
```

You will be prompted for a `SupplierItemSKU`. The script will:
- Uppercase the input SKU
- Generate a unique `GlobalIdentifier`
- Sign the request
- Display the request URL, HTTP status, and a pretty-printed XML response

Example session:

```
Enter SupplierItemSKU for stock check (blank to exit): ABC123
Request URL: https://your.fcB2Bserver.com/...
HTTP Status: 200
--- XML Response ---
<InventoryInquiryResponse>
  ...
</InventoryInquiryResponse>
```

Leave the input blank to exit.

---


