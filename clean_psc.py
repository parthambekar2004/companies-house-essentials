import scrapy
import csv
from datetime import datetime


class CleanPscSpider(scrapy.Spider):
    name = "clean_psc"

    def __init__(self, api_key=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not api_key:
            raise ValueError("api_key is required")

        self.api_key = api_key
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
            url = f"https://api.company-information.service.gov.uk/company/{company_number}/persons-with-significant-control?items_per_page=100"
            yield scrapy.Request(
                url=url,
                headers={
                    "Authorization": self.api_key,
                    "User-Agent": "parth-ch-scraper/1.0"
                },
                meta={"company_number": company_number},
                callback=self.parse
            )

    def parse(self, response):
        data = response.json()
        company_number = response.meta["company_number"]

        for item in data.get("items", []):
            yield {
                "company_number": company_number,
                "psc_id": item.get("links", {}).get("self", "").split("/")[-1],
                "name": item.get("name"),
                "kind": item.get("kind"),
                "natures_of_control": item.get("natures_of_control"),
                "notified_on": item.get("notified_on"),
                "ceased_on": item.get("ceased_on"),
                "snapshot_date": self.snapshot_date
            }