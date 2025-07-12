# Central storage for all hospital doctor data.
DOCTORS = {
    "Cardiology": [
        {"name": "Dr. Arjun Sharma", "photo": "doctor_male.png", "details": "MD, FACC | 15 years exp.\nAIIMS, New Delhi", "availability": "Available", "email": "a.sharma@hospital.com", "timings": "Mon-Fri, 9:00 AM - 1:00 PM", "holidays": "Sat, Sun", "fees": "₹2500"},
        {"name": "Dr. Priya Patel", "photo": "doctor_female.png", "details": "MBBS, MRCP | 12 years exp.\nKMC, Manipal", "availability": "Unavailable", "email": "p.patel@hospital.com", "timings": "Tue-Sat, 11:00 AM - 4:00 PM", "holidays": "Mon, Sun", "fees": "₹2200"}
    ],
    "Orthopedics": [
        {"name": "Dr. Vikram Singh", "photo": "doctor_male.png", "details": "MS (Ortho) | 20 years exp.\nPGIMER, Chandigarh", "availability": "Available", "email": "v.singh@hospital.com", "timings": "Mon-Thu, 8:00 AM - 12:00 PM", "holidays": "Fri, Sat, Sun", "fees": "₹3000"},
        {"name": "Dr. Sunita Rao", "photo": "doctor_female.png", "details": "DNB (Ortho) | 10 years exp.\nApollo, Chennai", "availability": "Available", "email": "s.rao@hospital.com", "timings": "Mon-Fri, 2:00 PM - 6:00 PM", "holidays": "Sat, Sun", "fees": "₹2800"}
    ],
    "Dermatology": [
        {"name": "Dr. Rohan Mehra", "photo": "doctor_male.png", "details": "MBBS, MD | 9 years exp.\nSt. John's, Bengaluru", "availability": "Unavailable", "email": "r.mehra@hospital.com", "timings": "Tue-Sat, 10:00 AM - 1:00 PM", "holidays": "Sun, Mon", "fees": "₹1700"},
        {"name": "Dr. Aisha Khan", "photo": "doctor_female.png", "details": "MD | 8 years exp.\nCMC, Vellore", "availability": "Available", "email": "a.khan@hospital.com", "timings": "Mon-Fri, 10 AM - 2 PM", "holidays": "Sat, Sun", "fees": "₹1800"}
    ],
    "Neurology": [
        {"name": "Dr. Rohan Joshi", "photo": "doctor_male.png", "details": "MD, DM | 18 years exp.\nNIMHANS, Bengaluru", "availability": "Unavailable", "email": "r.joshi@hospital.com", "timings": "Tue, Thu, 1 PM - 5 PM", "holidays": "Sat, Sun, Mon", "fees": "₹2800"},
        {"name": "Dr. Anika Reddy", "photo": "doctor_female.png", "details": "MD, DM | 16 years exp.\nSCTIMST, Trivandrum", "availability": "Available", "email": "a.reddy@hospital.com", "timings": "Mon, Wed, Fri, 9 AM - 12 PM", "holidays": "Sat, Sun", "fees": "₹3200"}
    ],
    "Gynecology": [
        {"name": "Dr. Sameer Verma", "photo": "doctor_male.png", "details": "MBBS, MS | 11 years exp.\nKasturba Medical College", "availability": "Unavailable", "email": "s.verma@hospital.com", "timings": "Mon-Fri, 3 PM - 7 PM", "holidays": "Sat, Sun", "fees": "₹1900"},
        {"name": "Dr. Meera Desai", "photo": "doctor_female.png", "details": "MBBS, DGO | 14 years exp.\nGrant Medical College, Mumbai", "availability": "Available", "email": "m.desai@hospital.com", "timings": "Mon-Sat, 11 AM - 3 PM", "holidays": "Sun", "fees": "₹2000"}
    ],
    "General Physician": [
        {"name": "Dr. Anand Kumar", "photo": "doctor_male.png", "details": "MBBS, MD | 10 years exp.\nMAMC, New Delhi", "availability": "Available", "email": "a.kumar@hospital.com", "timings": "Mon-Fri, 9:00 AM - 5:00 PM", "holidays": "Sat, Sun", "fees": "₹1500"},
        {"name": "Dr. Sunita Reddy", "photo": "doctor_female.png", "details": "MD | 12 years exp.\nJIPMER, Puducherry", "availability": "Available", "email": "s.reddy@hospital.com", "timings": "Mon, Wed, Fri, 2:00 PM - 6:00 PM", "holidays": "Sat, Sun", "fees": "₹1600"}
    ]
}

# A flat list of all doctors, used for the check-in screen
ALL_DOCTORS = [doctor for specialty_doctors in DOCTORS.values() for doctor in specialty_doctors]