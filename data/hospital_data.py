# Central storage for all hospital doctor data.
DOCTORS = {
    "Cardiology": [
        {"name": "Dr. Arjun Sharma", "name_hi": "डॉ. अर्जुन शर्मा", "photo": "doctor_male.png", "details": "MD, FACC | 15 years exp.\nAIIMS, New Delhi", "details_hi": "एमडी, एफएसीसी | 15 साल का अनुभव\nएम्स, नई दिल्ली", "availability": "Available", "email": "a.sharma@hospital.com", "timings": "Mon-Fri, 9:00 AM - 1:00 PM", "holidays": ["sat", "sun"], "fees": "₹2500"},
        {"name": "Dr. Priya Patel", "name_hi": "डॉ. प्रिया पटेल", "photo": "doctor_female.png", "details": "MBBS, MRCP | 12 years exp.\nKMC, Manipal", "details_hi": "एमबीबीएस, एमआरसीपी | 12 साल का अनुभव\nकेएमसी, मणिपाल", "availability": "Unavailable", "email": "p.patel@hospital.com", "timings": "Tue-Sat, 11:00 AM - 4:00 PM", "holidays": ["mon", "sun"], "fees": "₹2200"}
    ],
    "Orthopedics": [
        {"name": "Dr. Vikram Singh", "name_hi": "डॉ. विक्रम सिंह", "photo": "doctor_male.png", "details": "MS (Ortho) | 20 years exp.\nPGIMER, Chandigarh", "details_hi": "एमएस (ऑर्थो) | 20 साल का अनुभव\nपीजीआईएमईआर, चंडीगढ़", "availability": "Available", "email": "v.singh@hospital.com", "timings": "Mon-Thu, 8:00 AM - 12:00 PM", "holidays": ["fri", "sat", "sun"], "fees": "₹3000"},
        {"name": "Dr. Sunita Rao", "name_hi": "डॉ. सुनीता राव", "photo": "doctor_female.png", "details": "DNB (Ortho) | 10 years exp.\nApollo, Chennai", "details_hi": "डीएनबी (ऑर्थो) | 10 साल का अनुभव\nअपोलो, चेन्नई", "availability": "Available", "email": "s.rao@hospital.com", "timings": "Mon-Fri, 2:00 PM - 6:00 PM", "holidays": ["sat", "sun"], "fees": "₹2800"}
    ],
    "Dermatology": [
        {"name": "Dr. Rohan Mehra", "name_hi": "डॉ. रोहन मेहरा", "photo": "doctor_male.png", "details": "MBBS, MD | 9 years exp.\nSt. John's, Bengaluru", "details_hi": "एमबीबीएस, एमडी | 9 साल का अनुभव\nसेंट जॉन्स, बेंगलुरु", "availability": "Unavailable", "email": "r.mehra@hospital.com", "timings": "Tue-Sat, 10:00 AM - 1:00 PM", "holidays": ["sun", "mon"], "fees": "₹1700"},
        {"name": "Dr. Aisha Khan", "name_hi": "डॉ. आयशा खान", "photo": "doctor_female.png", "details": "MD | 8 years exp.\nCMC, Vellore", "details_hi": "एमडी | 8 साल का अनुभव\nसीएमसी, वेल्लोर", "availability": "Available", "email": "a.khan@hospital.com", "timings": "Mon-Fri, 10 AM - 2 PM", "holidays": ["sat", "sun"], "fees": "₹1800"}
    ],
    "Neurology": [
        {"name": "Dr. Rohan Joshi", "name_hi": "डॉ. रोहन जोशी", "photo": "doctor_male.png", "details": "MD, DM | 18 years exp.\nNIMHANS, Bengaluru", "details_hi": "एमडी, डीएम | 18 साल का अनुभव\nनिमहंस, बेंगलुरु", "availability": "Unavailable", "email": "r.joshi@hospital.com", "timings": "Tue, Thu, 1 PM - 5 PM", "holidays": ["sat", "sun", "mon"], "fees": "₹2800"},
        {"name": "Dr. Anika Reddy", "name_hi": "डॉ. अनिका रेड्डी", "photo": "doctor_female.png", "details": "MD, DM | 16 years exp.\nSCTIMST, Trivandrum", "details_hi": "एमडी, डीएम | 16 साल का अनुभव\nएससीटीआईएमएसटी, त्रिवेंद्रम", "availability": "Available", "email": "a.reddy@hospital.com", "timings": "Mon, Wed, Fri, 9 AM - 12 PM", "holidays": ["sat", "sun"], "fees": "₹3200"}
    ],
    "Gynecology": [
        {"name": "Dr. Sameer Verma", "name_hi": "डॉ. समीर वर्मा", "photo": "doctor_male.png", "details": "MBBS, MS | 11 years exp.\nKasturba Medical College", "details_hi": "एमबीबीएस, एमएस | 11 साल का अनुभव\nकस्तूरबा मेडिकल कॉलेज", "availability": "Unavailable", "email": "s.verma@hospital.com", "timings": "Mon-Fri, 3 PM - 7 PM", "holidays": ["sat", "sun"], "fees": "₹1900"},
        {"name": "Dr. Meera Desai", "name_hi": "डॉ. मीरा देसाई", "photo": "doctor_female.png", "details": "MBBS, DGO | 14 years exp.\nGrant Medical College, Mumbai", "details_hi": "एमबीबीएस, डीजीओ | 14 साल का अनुभव\nग्रांट मेडिकल कॉलेज, मुंबई", "availability": "Available", "email": "m.desai@hospital.com", "timings": "Mon-Sat, 11 AM - 3 PM", "holidays": ["sun"], "fees": "₹2000"}
    ],
    "General Physician": [
        {"name": "Dr. Anand Kumar", "name_hi": "डॉ. आनंद कुमार", "photo": "doctor_male.png", "details": "MBBS, MD | 10 years exp.\nMAMC, New Delhi", "details_hi": "एमबीबीएस, एमडी | 10 साल का अनुभव\nएमएएमसी, नई दिल्ली", "availability": "Available", "email": "a.kumar@hospital.com", "timings": "Mon-Fri, 9:00 AM - 5:00 PM", "holidays": ["sat", "sun"], "fees": "₹1500"},
        {"name": "Dr. Sunita Reddy", "name_hi": "डॉ. सुनीता रेड्डी", "photo": "doctor_female.png", "details": "MD | 12 years exp.\nJIPMER, Puducherry", "details_hi": "एमडी | 12 साल का अनुभव\nजिपमेर, पुडुचेरी", "availability": "Available", "email": "s.reddy@hospital.com", "timings": "Mon, Wed, Fri, 2:00 PM - 6:00 PM", "holidays": ["sat", "sun"], "fees": "₹1600"}
    ]
}

# A flat list of all doctors, used for the check-in screen
ALL_DOCTORS = [doctor for specialty_doctors in DOCTORS.values() for doctor in specialty_doctors]