import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class ScreeningEngine:
    """
    A fuzzy matching screening engine for sanctions & compliance checks.
    """

    def __init__(self, master_list_path):
        """
        Load the master sanctions dataset.
        """
        self.df = pd.read_csv(master_list_path)

        # normalize for matching
        self.df["name_clean"] = self.df["name"].astype(str).str.lower().str.strip()
        self.df["country_clean"] = self.df["country"].astype(str).str.lower().str.strip()
        self.df["address_clean"] = self.df["address"].astype(str).str.lower().str.strip()

    def score_entity(self, input_name, country=None, address=None):
        """
        Fuzzy match score for a single entity.
        """

        input_name_clean = input_name.lower().strip()
        country_clean = country.lower().strip() if country else None
        address_clean = address.lower().strip() if address else None

        results = []

        for _, row in self.df.iterrows():

            # name score
            name_score = fuzz.token_set_ratio(input_name_clean, row["name_clean"])

            # optional country score
            country_score = 0
            if country_clean:
                country_score = fuzz.partial_ratio(country_clean, row["country_clean"])

            # optional address score
            address_score = 0
            if address_clean:
                address_score = fuzz.partial_ratio(address_clean, row["address_clean"])

            # Weighted final score
            final_score = (
                name_score * 0.7 +
                country_score * 0.2 +
                address_score * 0.1
            )

            results.append({
                "input_name": input_name,
                "match_name": row["name"],
                "list_type": row["list_type"],
                "country": row["country"],
                "address": row["address"],
                "name_score": name_score,
                "country_score": country_score,
                "address_score": address_score,
                "final_score": round(final_score, 2)
            })

        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values("final_score", ascending=False)

        return results_df

    def screen(self, input_name, country=None, address=None, threshold=75):
        """
        Main method: screens an entity and returns all matches above threshold.
        """

        results_df = self.score_entity(input_name, country, address)

        hits = results_df[results_df["final_score"] >= threshold]

        if hits.empty:
            return {
                "status": "No Match",
                "details": None
            }

        return {
            "status": "Potential Match",
            "count": len(hits),
            "matches": hits.to_dict(orient="records")
        }
