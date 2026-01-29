import scrapy
import csv
from datetime import datetime


class CleanOfficerSpider(scrapy.Spider):
    name = "clean_officers"

    def __init__(self, api_key=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not api_key:
            raise ValueError("api_key is required")

        self.api_key = api_key
        self.base_url = "https://api.company-information.service.gov.uk"
        self.snapshot_date = datetime.utcnow().date().isoformat()
        self.company_numbers = self.load_company_numbers()

    def load_company_numbers(self):
        nums = []
        with open("companies.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cn = row.get("CompanyNumber")
                if cn:
                    nums.append(cn.strip())
        return nums

    def start_requests(self):
        for company_number in self.company_numbers:
            url = f"{self.base_url}/company/{company_number}/officers?items_per_page=100"
            yield scrapy.Request(
                url=url,
                headers={
                    "Authorization": self.api_key,
                    "User-Agent": "parth-ch-scraper/1.0"
                },
                meta={"company_number": company_number},
                callback=self.parse_company_officers
            )

    def parse_company_officers(self, response):
        data = response.json()
        company_number = response.meta["company_number"]

        for item in data.get("items", []):
            officer_id = item.get("links", {}).get("officer", {}).get("appointments", "").split("/")[-2]

            yield {
                "record_type": "company_officer",
                "company_number": company_number,
                "officer_id": officer_id,
                "name": item.get("name"),
                "role": item.get("officer_role"),
                "appointed_on": item.get("appointed_on"),
                "resigned_on": item.get("resigned_on"),
                "snapshot_date": self.snapshot_date
            }

            if officer_id:
                url = f"{self.base_url}/officers/{officer_id}/appointments?items_per_page=100"
                yield scrapy.Request(
                    url=url,
                    headers={"Authorization": self.api_key},
                    meta={"officer_id": officer_id},
                    callback=self.parse_appointments
                )

    def parse_appointments(self, response):
        data = response.json()
        officer_id = response.meta["officer_id"]

        for item in data.get("items", []):
            yield {
                "record_type": "officer_appointment",
                "officer_id": officer_id,
                "company_number": item.get("appointed_to", {}).get("company_number"),
                "company_name": item.get("appointed_to", {}).get("company_name"),
                "role": item.get("officer_role"),
                "appointed_on": item.get("appointed_on"),
                "resigned_on": item.get("resigned_on"),
                "snapshot_date": self.snapshot_date
            }