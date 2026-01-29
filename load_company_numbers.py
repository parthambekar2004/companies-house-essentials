import csv

company_numbers = []

with open("jan2026 companieshousedatacleaned.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cn = row.get("CompanyNumber")
        if cn:
            company_numbers.append(cn.strip())

print(f"Loaded {len(company_numbers)} company numbers")
print(company_numbers[:10])  # sanity check
