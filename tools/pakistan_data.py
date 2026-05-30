"""Static Pakistan tourism knowledge base for grounding agent responses."""

TRANSPORT_OPTIONS = {
    "islamabad_to_hunza": {
        "karakoram_highway_bus": {"price_pkr": 1500, "duration_hrs": 18, "operator": "NATCO / Daewoo"},
        "private_car_rental": {"price_pkr": 18000, "duration_hrs": 14, "note": "Best for groups of 4+"},
        "flight_to_gilgit_then_road": {"price_pkr": 12000, "duration_hrs": 3, "airline": "PIA / AirSial", "note": "Flight frequently cancelled — have backup"},
        "shared_coaster": {"price_pkr": 2000, "duration_hrs": 16, "note": "Departs Rawalpindi Pirwadhai Mor"},
    },
    "islamabad_to_lahore": {
        "daewoo_bus": {"price_pkr": 1200, "duration_hrs": 4.5, "operator": "Daewoo Express"},
        "train_green_line": {"price_pkr": 800, "duration_hrs": 5, "operator": "Pakistan Railways"},
        "flight": {"price_pkr": 8000, "duration_hrs": 1, "airline": "AirBlue / PIA"},
        "private_car": {"price_pkr": 10000, "duration_hrs": 3.5},
    },
    "islamabad_to_skardu": {
        "flight_pia": {"price_pkr": 14000, "duration_hrs": 1.5, "note": "Weather dependent — book flexible ticket"},
        "road_via_karakoram": {"price_pkr": 3000, "duration_hrs": 22, "note": "Via Chilas — stunning but long"},
    },
    "islamabad_to_murree": {
        "public_wagon": {"price_pkr": 200, "duration_hrs": 2},
        "private_car": {"price_pkr": 4000, "duration_hrs": 1.5},
    },
    "islamabad_to_swat": {
        "daewoo_bus": {"price_pkr": 900, "duration_hrs": 5},
        "private_car": {"price_pkr": 10000, "duration_hrs": 4},
    },
    "lahore_to_islamabad": {
        "daewoo_bus": {"price_pkr": 1200, "duration_hrs": 4.5},
        "train": {"price_pkr": 800, "duration_hrs": 5},
        "flight": {"price_pkr": 8000, "duration_hrs": 1},
    },
}

ACCOMMODATIONS = {
    "hunza": {
        "luxury": [
            {"name": "Serena Karimabad", "price_pkr_per_night": 25000, "rating": 4.8},
            {"name": "Eagle's Nest Hotel", "price_pkr_per_night": 18000, "rating": 4.7, "note": "Best Karakoram views"},
        ],
        "mid_range": [
            {"name": "Old Hunza Inn", "price_pkr_per_night": 6000, "rating": 4.4},
            {"name": "Hunza Baltit Inn", "price_pkr_per_night": 5500, "rating": 4.3},
        ],
        "budget": [
            {"name": "Hunza Embassy Hotel", "price_pkr_per_night": 2500, "rating": 4.0},
        ],
    },
    "lahore": {
        "luxury": [
            {"name": "Pearl Continental Lahore", "price_pkr_per_night": 35000, "rating": 4.6},
            {"name": "Avari Hotel Lahore", "price_pkr_per_night": 28000, "rating": 4.5},
        ],
        "mid_range": [
            {"name": "Hotel One Gulberg", "price_pkr_per_night": 9000, "rating": 4.3},
            {"name": "Faletti's Hotel (Historic)", "price_pkr_per_night": 12000, "rating": 4.2},
        ],
        "budget": [
            {"name": "Lahore Backpackers", "price_pkr_per_night": 1500, "rating": 4.0},
        ],
    },
    "skardu": {
        "luxury": [
            {"name": "Shangrila Resort", "price_pkr_per_night": 22000, "rating": 4.7, "note": "Lower Kachura Lake"},
        ],
        "mid_range": [
            {"name": "K2 Motel Skardu", "price_pkr_per_night": 7000, "rating": 4.3},
        ],
        "budget": [
            {"name": "Karakoram Guest House", "price_pkr_per_night": 2000, "rating": 3.9},
        ],
    },
    "islamabad": {
        "luxury": [
            {"name": "Serena Hotel Islamabad", "price_pkr_per_night": 40000, "rating": 4.7},
            {"name": "Marriott Islamabad", "price_pkr_per_night": 38000, "rating": 4.6},
        ],
        "mid_range": [
            {"name": "Hotel One F-8", "price_pkr_per_night": 8000, "rating": 4.3},
        ],
        "budget": [
            {"name": "Islamabad Backpackers Inn", "price_pkr_per_night": 2000, "rating": 4.0},
        ],
    },
}

ATTRACTIONS = {
    "hunza": [
        "Baltit Fort (900+ years old — UNESCO tentative list)",
        "Altit Fort (1000+ years old — oldest in Hunza)",
        "Attabad Lake (turquoise glacial lake formed by 2010 landslide)",
        "Rakaposhi Viewpoint (7788m peak visible)",
        "Khunjerab Pass (4693m — China border crossing)",
        "Eagle's Nest viewpoint at sunset",
        "Hopper Glacier day hike",
        "Ganesh Village petroglyphs (Silk Road era carvings)",
    ],
    "lahore": [
        "Lahore Fort (Shahi Qila) — Mughal masterpiece",
        "Badshahi Mosque — 17th century, one of world's largest",
        "Walled City of Lahore — Delhi Gate, Shahi Hammam",
        "Shalimar Gardens — UNESCO World Heritage Site",
        "Wagah Border Ceremony — daily flag lowering ceremony",
        "Anarkali Bazaar — oldest bazaar in South Asia",
        "Data Darbar Shrine of Data Ganj Bakhsh",
        "Lahore Museum ('Wonder House' of Rudyard Kipling)",
        "Minar-e-Pakistan",
    ],
    "skardu": [
        "Shangrila Resort and Lower Kachura Lake",
        "Deosai National Park — second highest plateau on earth",
        "Skardu Fort (Karphocho Fort)",
        "Satpara Lake",
        "Shigar Fort (heritage hotel conversion)",
        "Upper Kachura Lake",
        "K2 Base Camp trek (14+ days — world's most challenging trek)",
        "Manthokha Waterfall",
    ],
    "islamabad": [
        "Faisal Mosque — largest mosque in South Asia",
        "Pakistan Monument",
        "Daman-e-Koh viewpoint",
        "Lok Virsa Museum",
        "Margalla Hills hiking trails (Trail 3, 5, 6)",
        "Taxila Museum — day trip for Gandhara Buddhist civilisation",
        "Rawal Lake",
    ],
}

FOOD_GUIDE = {
    "hunza": {
        "must_try": ["Chapshuro (meat-filled Hunzai bread)", "Diram phitti (apricot porridge)", "Mamtu (Hunzai dumplings)", "Tumuro chai (sea buckthorn berry tea)", "Mulberry wine (non-alcoholic variety)"],
        "restaurants": ["Cafe de Hunza (Karimabad)", "Village Restaurant", "Diran Guest House dining"],
        "tip": "Hunzai cuisine reflects the famous longevity of locals — apricots, mulberries, and buckwheat are staples.",
    },
    "lahore": {
        "must_try": ["Nihari from Waris Nihari (open since 1947)", "Lahori chargha (spiced whole chicken)", "Paye (trotters curry — breakfast)", "Anday wala burger at MM Alam", "Kulfi Faluda at Yousaf Saleem Chowk", "Gol gappay at any roadside stall"],
        "food_streets": ["Fort Road Food Street (Mughal-era ambiance)", "Gawalmandi Food Street", "MM Alam Road (upscale)"],
        "tip": "Lahore is the food capital of Pakistan — never skip a proper Lahori breakfast at a dhaba.",
    },
    "skardu": {
        "must_try": ["Tibetan-influenced thukpa (noodle soup)", "Momo dumplings", "Trout fish from Satpara Lake", "Apricot jam with local bread"],
        "tip": "Skardu cuisine is simpler than Lahore — focus on fresh trout and local bread.",
    },
    "islamabad": {
        "must_try": ["Desi ghee karahi", "Afghan rice palao from Kohsar Market", "Khwaja Moin ud Din's street food at F-7"],
        "areas": ["Melody Market dhaba lane", "F-6 Supermarket cafes", "Karachi Company food street"],
    },
}

SAFETY_INFO = {
    "emergency_numbers": {
        "police": "15",
        "rescue_punjab": "1122",
        "rescue_kpk": "1122",
        "ambulance": "115",
        "edhi_ambulance": "115",
        "tourist_police_lahore": "+92-42-99213000",
        "tourist_helpline_ptdc": "051-9208645",
        "mountain_rescue": "+92-58-111-900-900",
    },
    "safe_zones": ["Islamabad", "Lahore", "Karachi (tourist areas)", "Hunza Valley", "Skardu", "Murree", "Swat Valley (post-2013)"],
    "cultural_norms": [
        "Dress modestly — cover shoulders and knees outside major cities",
        "Remove shoes before entering mosques and shrines",
        "Ask permission before photographing locals, especially women",
        "Fridays: govt offices closed; many restaurants open later",
        "During Ramadan: avoid eating/drinking in public during fasting hours",
        "Accept tea/food when offered — refusal can seem rude",
        "Bargaining is standard in bazaars — start at 50% of asking price",
    ],
    "sim_cards": "Jazz tourist SIM at airport — PKR 500 with 5GB data. Jazz has best northern coverage.",
    "altitude_warning": "Altitude sickness risk above 3000m. Spend 1-2 nights in Gilgit before going higher.",
    "kkh_warning": "Karakoram Highway can close due to landslides. Check NHMP 130 helpline before travel.",
}

SEASON_GUIDE = {
    "spring": {"months": "Mar-May", "best_for": ["Hunza blossoms (late March)", "Chitral", "Swat"], "note": "Cherry blossoms in Hunza are world-class"},
    "summer": {"months": "Jun-Aug", "best_for": ["K2 trekking", "Fairy Meadows", "All northern areas"], "avoid": "KKH in heavy monsoon"},
    "autumn": {"months": "Sep-Nov", "best_for": ["Everywhere — BEST season"], "note": "October: Hunza foliage turns orange/red — most photogenic time of year"},
    "winter": {"months": "Dec-Feb", "best_for": ["Lahore", "Multan", "Murree snow", "Cholistan Desert"], "avoid": "Northern mountain areas — roads blocked"},
}
