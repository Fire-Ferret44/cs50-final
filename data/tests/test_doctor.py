"""
Tests the doctor class manually.
"""

from utility.doctor import Doctor

def manual_doctor_test():
    doc = Doctor(name="Dr. Ead", experience_level="junior")
    doc.add_leave_date(["2025-06-25", "2025-06-26"])
    doc.set_preferences({"prefer_distribution_weekend": "sat"})
    
    print(doc.name)
    print(doc.experience_level)
    print(doc.leave_dates)
    print(doc.preferences)

if __name__ == "__main__":
    manual_doctor_test()