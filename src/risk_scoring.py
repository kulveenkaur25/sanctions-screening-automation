import pandas as pd
from fuzzywuzzy import fuzz
from screening_engine import ScreeningEngine

class RiskScoringEngine:
    """
    Combines screening match score + KYC red flags + geographic risk
    into a final unified risk score.
    """

    def __init__(self, master_list_path, kyc_flags_path=None):
        self.screen_engine = ScreeningEngine(master_list_path)

        # Load KYC red flags (optional)
        if kyc_flags_path:
            try:
                self.kyc_df = pd.read_csv(kyc_flags_path)
            except:
                self.kyc_df = pd.DataFrame()
        else:
            self.kyc_df = pd.DataFrame()

        # Geographic risk mapping
        self.geo_risk = {
            "iran": 100,
            "iraq": 90,
            "syria": 90,
            "russia": 85,
            "pakistan": 70,
            "afghanistan": 80,
            "china": 60,
            "uae": 40,
            "india": 30,
            "usa": 20
        }

    def get_geo_risk(self, country):
        if not country:
            return 0
        c = country.lower().strip()
        return self.geo_risk.get(c, 20)  # default low-risk

    def risk_level(self, score):
        if score >= 80: return "HIGH"
        if score >= 50: return "MEDIUM"
        return "LOW"

    def score_entity(self, name, country=None, address=None):
        """
        Full risk scoring pipeline:
        1. Sanctions screening match
        2. Country risk
        3. KYC Red flags
        """

        # 1. Sanctions matching
        screening_result = self.screen_engine.screen(name, country, address)
        match_score = 0
        matched_list_type = None

        if screening_result["status"] == "Potential Match":
            match_score = screening_result["matches"][0]["final_score"]
            matched_list_type = screening_result["matches"][0]["list_type"]

        # 2. Geographic risk
        geo_score = self.get_geo_risk(country)

        # 3. KYC Red Flags (placeholder: 10 points if any)
        kyc_score = 10 if not self.kyc_df.empty else 0

        # Weighted final score
        final_score = (
            match_score * 0.5 +
            geo_score * 0.3 +
            kyc_score * 0.2
        )

        final_score = round(final_score, 2)
        level = self.risk_level(final_score)

        return {
            "name": name,
            "country": country,
            "match_score": match_score,
            "geo_risk_score": geo_score,
            "kyc_score": kyc_score,
            "final_score": final_score,
            "risk_level": level,
            "matched_list": matched_list_type
        }
