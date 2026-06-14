"""Tests for Regulations Review Committee complaint parsing."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.regulations_review_committee.complaint_parser import (
    ComplaintRecord,
    parse_complaint_subject,
    extract_challenged_regulation,
    extract_complaint_grounds,
    extract_committee_recommendation,
    parse_complaints_from_text,
)
from scripts.regulations_review_committee.regulation_cross_reference import (
    SecondaryLegislationKey,
    map_to_legislation_key,
    lookup_nz_legislation,
    build_correlation_index,
    CorrelationEntry,
)


class ComplaintRecordTest(unittest.TestCase):
    """ComplaintRecord dataclass tests."""

    def test_minimal_record(self):
        r = ComplaintRecord(subject="Complaint 2023/42")
        self.assertEqual(r.subject, "Complaint 2023/42")
        self.assertIsNone(r.challenged_regulation)
        self.assertIsNone(r.grounds)
        self.assertIsNone(r.recommendation)

    def test_full_record(self):
        r = ComplaintRecord(
            subject="Complaint 2023/42",
            challenged_regulation="SR 2023/150",
            grounds="Regulation exceeds statutory authority",
            recommendation="Regulation revoked",
        )
        self.assertEqual(r.subject, "Complaint 2023/42")
        self.assertEqual(r.challenged_regulation, "SR 2023/150")
        self.assertEqual(r.grounds, "Regulation exceeds statutory authority")
        self.assertEqual(r.recommendation, "Regulation revoked")

    def test_to_dict(self):
        r = ComplaintRecord(
            subject="Complaint 2023/42",
            challenged_regulation="SR 2023/150",
            grounds="Ultra vires the empowering Act",
            recommendation="Recommendation to revoke",
        )
        d = r.to_dict()
        self.assertEqual(d["subject"], "Complaint 2023/42")
        self.assertEqual(d["challenged_regulation"], "SR 2023/150")
        self.assertEqual(d["grounds"], "Ultra vires the empowering Act")
        self.assertEqual(d["recommendation"], "Recommendation to revoke")

    def test_to_dict_omits_none_fields(self):
        r = ComplaintRecord(subject="Complaint 2024/01")
        d = r.to_dict()
        self.assertIn("subject", d)
        self.assertNotIn("challenged_regulation", d)
        self.assertNotIn("grounds", d)
        self.assertNotIn("recommendation", d)

    def test_repr(self):
        r = ComplaintRecord(subject="Complaint 2023/42")
        self.assertIn("Complaint 2023/42", repr(r))


class ParseComplaintSubjectTest(unittest.TestCase):
    """Tests for parse_complaint_subject."""

    def test_full_complaint_reference(self):
        text = "Complaint 2023/42 — ABC Regulations 2023"
        subject = parse_complaint_subject(text)
        self.assertIsNotNone(subject)
        self.assertIn("2023/42", subject)

    def test_complaint_with_hyphen(self):
        text = "complaint 2024/15 - Review of XYZ Rules"
        subject = parse_complaint_subject(text)
        self.assertIsNotNone(subject)
        self.assertIn("2024/15", subject)

    def test_complaint_number_only(self):
        text = "2023/42"
        subject = parse_complaint_subject(text)
        self.assertEqual(subject, "Complaint 2023/42")

    def test_case_insensitive(self):
        text = "COMPLAINT 2022/08 CONCERNING FOO REGS"
        subject = parse_complaint_subject(text)
        self.assertIsNotNone(subject)
        self.assertIn("2022/08", subject)

    def test_returns_none_for_no_match(self):
        self.assertIsNone(parse_complaint_subject("General discussion item"))
        self.assertIsNone(parse_complaint_subject(""))
        self.assertIsNone(parse_complaint_subject(None))

    def test_with_hash_symbol(self):
        text = "Complaint #2023/42"
        subject = parse_complaint_subject(text)
        self.assertIsNotNone(subject)
        self.assertIn("2023/42", subject)

    def test_with_number_keyword(self):
        text = "Complaint number 2023/42"
        subject = parse_complaint_subject(text)
        self.assertIsNotNone(subject)
        self.assertIn("2023/42", subject)

    def test_with_no_keyword_number(self):
        text = "Complaint no. 2023/42"
        subject = parse_complaint_subject(text)
        self.assertIsNotNone(subject)
        self.assertIn("2023/42", subject)

    def test_handles_year_only_no_match(self):
        text = "The committee met in 2023 to discuss regulations."
        self.assertIsNone(parse_complaint_subject(text))


class ExtractChallengedRegulationTest(unittest.TestCase):
    """Tests for extract_challenged_regulation."""

    def test_standard_sr_format(self):
        text = "The complaint concerns SR 2023/150, the ABC Regulations 2023."
        reg = extract_challenged_regulation(text)
        self.assertEqual(reg, "SR 2023/150")

    def test_li_format(self):
        text = "This submission challenges LI 2024/56."
        reg = extract_challenged_regulation(text)
        self.assertEqual(reg, "LI 2024/56")

    def test_nzli_format(self):
        text = "Regulation NZLI 2023/100 is under review."
        reg = extract_challenged_regulation(text)
        self.assertEqual(reg, "NZLI 2023/100")

    def test_sl_format(self):
        text = "Secondary legislation SL 2024/12 was examined."
        reg = extract_challenged_regulation(text)
        self.assertEqual(reg, "SL 2024/12")

    def test_year_slash_number_format(self):
        text = "The committee considered 2023/150 regulations."
        reg = extract_challenged_regulation(text)
        self.assertEqual(reg, "SR 2023/150")

    def test_named_regulation(self):
        text = "The ABC Regulations 2023 were challenged on procedural grounds."
        reg = extract_challenged_regulation(text)
        self.assertEqual(reg, "ABC Regulations 2023")

    def test_named_regulation_variant(self):
        text = "XYZ Rules 2024 are the subject of complaint."
        reg = extract_challenged_regulation(text)
        self.assertEqual(reg, "XYZ Rules 2024")

    def test_named_instrument(self):
        text = "The Civil Aviation (Safety) Order 2023 was examined."
        reg = extract_challenged_regulation(text)
        self.assertIsNotNone(reg)
        self.assertIn("2023", reg)

    def test_statutory_instrument(self):
        text = "Statutory instrument 2024/33 was found non-compliant."
        reg = extract_challenged_regulation(text)
        self.assertEqual(reg, "SI 2024/33")

    def test_returns_none_when_no_regulation(self):
        self.assertIsNone(extract_challenged_regulation("General discussion only."))
        self.assertIsNone(extract_challenged_regulation(""))
        self.assertIsNone(extract_challenged_regulation(None))


class ExtractComplaintGroundsTest(unittest.TestCase):
    """Tests for extract_complaint_grounds."""

    def test_ultra_vires_grounds(self):
        text = (
            "Grounds: The regulation is ultra vires the empowering Act. "
            "It exceeds the statutory authority delegated by Parliament."
        )
        grounds = extract_complaint_grounds(text)
        self.assertIsNotNone(grounds)
        self.assertIn("ultra vires", grounds.lower())

    def test_procedural_unfairness(self):
        text = "The grounds of complaint are procedural unfairness in the making of the instrument."
        grounds = extract_complaint_grounds(text)
        self.assertIsNotNone(grounds)
        self.assertIn("procedural", grounds.lower())

    def test_inconsistent_with_acts(self):
        text = (
            "Grounds for complaint: The regulation is inconsistent with "
            "the purposes of the principal Act."
        )
        grounds = extract_complaint_grounds(text)
        self.assertIsNotNone(grounds)
        self.assertIn("inconsistent", grounds.lower())

    def test_regulatory_impact_not_considered(self):
        text = "Grounds — regulatory impact statement not prepared."
        grounds = extract_complaint_grounds(text)
        self.assertIsNotNone(grounds)
        self.assertIn("regulatory impact", grounds.lower())

    def test_defective_consultation(self):
        text = "The complaint is grounded in defective consultation processes."
        grounds = extract_complaint_grounds(text)
        self.assertIsNotNone(grounds)
        self.assertIn("consultation", grounds.lower())

    def test_returns_none_when_no_grounds(self):
        self.assertIsNone(extract_complaint_grounds("Just a description."))
        self.assertIsNone(extract_complaint_grounds(""))
        self.assertIsNone(extract_complaint_grounds(None))


class ExtractCommitteeRecommendationTest(unittest.TestCase):
    """Tests for extract_committee_recommendation."""

    def test_recommendation_revoke(self):
        text = "The committee recommends that the regulation be revoked."
        rec = extract_committee_recommendation(text)
        self.assertIsNotNone(rec)
        self.assertIn("revoke", rec.lower())

    def test_recommendation_amend(self):
        text = "Recommendation: The instrument should be amended."
        rec = extract_committee_recommendation(text)
        self.assertIsNotNone(rec)
        self.assertIn("amend", rec.lower())

    def test_recommendation_no_action(self):
        text = "The committee recommends no further action."
        rec = extract_committee_recommendation(text)
        self.assertIsNotNone(rec)
        self.assertIn("no further action", rec.lower())

    def test_recommendation_bring_to_attention(self):
        text = "Committee recommends bringing the matter to the attention of the House."
        rec = extract_committee_recommendation(text)
        self.assertIsNotNone(rec)
        self.assertIn("attention", rec.lower())

    def test_recommendation_invalidate(self):
        text = "Recommendation: The regulation be invalidated."
        rec = extract_committee_recommendation(text)
        self.assertIsNotNone(rec)
        self.assertIn("invalid", rec.lower())

    def test_returns_none_when_no_recommendation(self):
        self.assertIsNone(extract_committee_recommendation("Summary of discussion."))
        self.assertIsNone(extract_committee_recommendation(""))
        self.assertIsNone(extract_committee_recommendation(None))


class ParseComplaintsFromTextTest(unittest.TestCase):
    """Tests for parse_complaints_from_text — the top-level orchestrator."""

    FULL_SAMPLE = (
        "Consideration of Complaints\n"
        "\n"
        "Complaint 2023/42 — ABC Regulations 2023\n"
        "The committee considered complaint 2023/42 regarding the ABC Regulations 2023 "
        "(SR 2023/150). "
        "Grounds: The regulation exceeds the statutory authority delegated under "
        "the parent Act and was made without proper consultation. "
        "The committee recommends that the regulation be revoked.\n"
        "\n"
        "Complaint 2024/15 — XYZ Rules 2024\n"
        "The committee also considered complaint 2024/15 concerning the XYZ Rules 2024 "
        "(LI 2024/56). "
        "Grounds for complaint: The instrument is procedurally defective "
        "and inconsistent with the purposes of the empowering Act. "
        "Recommendation: The instrument should be amended to align with "
        "the statutory framework.\n"
    )

    def test_parses_all_complaints(self):
        records = parse_complaints_from_text(self.FULL_SAMPLE)
        self.assertEqual(len(records), 2)

    def test_first_complaint_fields(self):
        records = parse_complaints_from_text(self.FULL_SAMPLE)
        r = records[0]
        self.assertEqual(r.subject, "Complaint 2023/42")
        self.assertEqual(r.challenged_regulation, "SR 2023/150")
        self.assertIsNotNone(r.grounds)
        self.assertIn("exceeds the statutory authority", r.grounds.lower())
        self.assertIsNotNone(r.recommendation)
        self.assertIn("revoke", r.recommendation.lower())

    def test_second_complaint_fields(self):
        records = parse_complaints_from_text(self.FULL_SAMPLE)
        r = records[1]
        self.assertEqual(r.subject, "Complaint 2024/15")
        self.assertEqual(r.challenged_regulation, "LI 2024/56")
        self.assertIsNotNone(r.grounds)
        self.assertIn("procedurally defective", r.grounds.lower())
        self.assertIsNotNone(r.recommendation)
        self.assertIn("amend", r.recommendation.lower())

    def test_empty_text_returns_empty_list(self):
        self.assertEqual(parse_complaints_from_text(""), [])
        self.assertEqual(parse_complaints_from_text(None), [])

    def test_text_without_complaints_returns_empty(self):
        text = "The committee discussed general regulatory matters."
        self.assertEqual(parse_complaints_from_text(text), [])

    def test_single_complaint(self):
        text = (
            "Complaint 2025/01 - DEF Instrument 2025\n"
            "The committee examined complaint 2025/01. "
            "Grounds: The instrument has an unclear legal effect. "
            "Recommendation: No further action."
        )
        records = parse_complaints_from_text(text)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].subject, "Complaint 2025/01")
        self.assertIn("unclear legal effect", records[0].grounds.lower())
        self.assertIn("no further action", records[0].recommendation.lower())


if __name__ == "__main__":
    unittest.main()
