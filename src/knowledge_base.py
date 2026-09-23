"""
src/knowledge_base.py
ຖານຂໍ້ມູນຄວາມຮູ້ - ແກ້ໄຂສຸດທ້າຍ (ບໍ່ລຶບຄຳສັບ)
"""

import re


class KnowledgeBase:
    """ຖານຂໍ້ມູນຄວາມຮູ້"""

    def __init__(self):
        # ============================================================
        # ເມືອງຫຼວງ
        # ============================================================
        self.capitals = {
            "laos": "Vientiane",
            "france": "Paris",
            "japan": "Tokyo",
            "thailand": "Bangkok",
            "vietnam": "Hanoi",
            "cambodia": "Phnom Penh",
            "china": "Beijing",
            "usa": "Washington D.C.",
            "united states": "Washington D.C.",
            "uk": "London",
            "united kingdom": "London",
            "germany": "Berlin",
            "italy": "Rome",
            "spain": "Madrid",
            "russia": "Moscow",
            "india": "New Delhi",
            "australia": "Canberra",
            "canada": "Ottawa",
            "brazil": "Brasilia",
            "south korea": "Seoul",
            "singapore": "Singapore",
            "malaysia": "Kuala Lumpur",
            "indonesia": "Jakarta",
            "philippines": "Manila",
            "myanmar": "Naypyidaw",
            "egypt": "Cairo",
            "south africa": "Pretoria",
        }

        # ============================================================
        # ດາວເຄາະ
        # ============================================================
        self.planets = {
            "red planet": "Mars",
            "largest planet": "Jupiter",
            "smallest planet": "Mercury",
            "closest to sun": "Mercury",
            "farthest from sun": "Neptune",
            "hottest planet": "Venus",
            "coldest planet": "Neptune",
            "blue planet": "Earth",
            "ringed planet": "Saturn",
        }

        # ============================================================
        # ຄະນິດສາດ
        # ============================================================
        self.math_constants = {
            "value of pi": "3.14159",
            "value of e": "2.71828",
            "golden ratio": "1.61803",
        }

        # ============================================================
        # ຟີຊິກ
        # ============================================================
        self.physics = {
            "speed of light": "299,792,458 m/s",
            "speed of sound": "343 m/s",
            "gravity": "9.8 m/s²",
            "gravitational constant": "6.674 × 10⁻¹¹ N·m²/kg²",
            "planck constant": "6.626 × 10⁻³⁴ J·s",
            "avogadro number": "6.022 × 10²³",
            "unit of force": "Newton (N)",
            "unit of energy": "Joule (J)",
            "unit of power": "Watt (W)",
            "unit of electric current": "Ampere (A)",
            "unit of voltage": "Volt (V)",
            "unit of resistance": "Ohm (Ω)",
        }

        # ============================================================
        # ເຄມີ
        # ============================================================
        self.chemistry = {
            # ສູດເຄມີ - ໃສ່ key ທີ່ຊັດເຈນ
            "chemical formula for water": "H2O",
            "formula for water": "H2O",
            "chemical formula for carbon dioxide": "CO2",
            "formula for carbon dioxide": "CO2",
            "chemical formula for salt": "NaCl",
            "formula for salt": "NaCl",
            "chemical formula for oxygen": "O2",
            "chemical formula for nitrogen": "N2",
            "chemical formula for methane": "CH4",
            "chemical formula for glucose": "C6H12O6",
            # ສັນຍະລັກເຄມີ
            "chemical symbol for gold": "Au",
            "chemical symbol for silver": "Ag",
            "chemical symbol for iron": "Fe",
            "chemical symbol for copper": "Cu",
            "chemical symbol for aluminum": "Al",
            "chemical symbol for lead": "Pb",
            "chemical symbol for mercury": "Hg",
            "chemical symbol for zinc": "Zn",
            # ສູດທົ່ວໄປ
            "h2o": "Water",
            "co2": "Carbon Dioxide",
            "o2": "Oxygen",
            "n2": "Nitrogen",
            "nacl": "Sodium Chloride (Salt)",
            "h2so4": "Sulfuric Acid",
            "hcl": "Hydrochloric Acid",
            "naoh": "Sodium Hydroxide",
            "ch4": "Methane",
            "c6h12o6": "Glucose",
            "au": "Gold",
            "ag": "Silver",
            "fe": "Iron",
            "cu": "Copper",
            "al": "Aluminum",
            "pb": "Lead",
            "hg": "Mercury",
            "zn": "Zinc",
            # ຄ່າ pH
            "ph of water": "7 (neutral)",
            "ph of acid": "Less than 7",
            "ph of base": "Greater than 7",
        }

        # ============================================================
        # ຊີວະວິທະຍາ
        # ============================================================
        self.biology = {
            "powerhouse of cell": "Mitochondria",
            "powerhouse of the cell": "Mitochondria",
            "brain of cell": "Nucleus",
            "unit of life": "Cell",
            "dna": "Deoxyribonucleic Acid",
            "rna": "Ribonucleic Acid",
            "atp": "Adenosine Triphosphate",
            "largest organ": "Skin",
            "number of bones in adult": "206",
            "number of chromosomes in human": "46",
            "normal body temperature": "37°C",
        }

        # ============================================================
        # ປະຫວັດສາດ
        # ============================================================
        self.history = {
            "first president of usa": "George Washington",
            "first man on moon": "Neil Armstrong",
            "first man on the moon": "Neil Armstrong",  # ເພີ່ມອັນນີ້
            "first person on moon": "Neil Armstrong",  # ແລະອັນນີ້
            "first person on the moon": "Neil Armstrong",  # ແລະອັນນີ້
            "inventor of telephone": "Alexander Graham Bell",
            "inventor of light bulb": "Thomas Edison",
            "discoverer of gravity": "Isaac Newton",
            "discoverer of penicillin": "Alexander Fleming",
            "father of computer": "Charles Babbage",
            "father of modern physics": "Albert Einstein",
            "founder of microsoft": "Bill Gates",
            "founder of apple": "Steve Jobs",
            "founder of facebook": "Mark Zuckerberg",
            "world war 1": "1914-1918",
            "world war 2": "1939-1945",
        }

        # ============================================================
        # ພາສາອັງກິດ
        # ============================================================
        self.english = {
            "past tense of go": "Went",
            "past tense of eat": "Ate",
            "past tense of see": "Saw",
            "past tense of run": "Ran",
            "past tense of write": "Wrote",
            "plural of child": "Children",
            "plural of mouse": "Mice",
            "plural of foot": "Feet",
            "plural of tooth": "Teeth",
            "opposite of hot": "Cold",
            "opposite of big": "Small",
            "opposite of fast": "Slow",
            "opposite of happy": "Sad",
        }

        # ============================================================
        # ຄອມພິວເຕີ
        # ============================================================
        self.computer = {
            "cpu": "Central Processing Unit",
            "ram": "Random Access Memory",
            "rom": "Read-Only Memory",
            "gpu": "Graphics Processing Unit",
            "operating system": "Operating System",
            "dbms": "Database Management System",
            "url": "Uniform Resource Locator",
            "http": "HyperText Transfer Protocol",
            "https": "HTTP Secure",
            "dns": "Domain Name System",
            "api": "Application Programming Interface",
            "html": "HyperText Markup Language",
            "css": "Cascading Style Sheets",
            "sql": "Structured Query Language",
            "gui": "Graphical User Interface",
            "usb": "Universal Serial Bus",
            "ssd": "Solid State Drive",
            "hdd": "Hard Disk Drive",
            "lan": "Local Area Network",
            "wan": "Wide Area Network",
            "vpn": "Virtual Private Network",
            "ftp": "File Transfer Protocol",
            "tcp": "Transmission Control Protocol",
            "udp": "User Datagram Protocol",
        }

        # ============================================================
        # ທົ່ວໄປ
        # ============================================================
        self.general = {
            "largest ocean": "Pacific Ocean",
            "largest desert": "Antarctic Desert",
            "largest country": "Russia",
            "smallest country": "Vatican City",
            "longest river": "Nile River",
            "highest mountain": "Mount Everest",
            "deepest ocean": "Mariana Trench",
            "largest island": "Greenland",
            "most populated country": "India",
            "currency of japan": "Yen",
            "currency of usa": "US Dollar",
            "currency of laos": "Kip",
            "currency of thailand": "Baht",
            "currency of china": "Yuan",
        }

    def _exact_word_match(self, key: str, text: str) -> bool:
        """
        ກວດວ່າ key ປາກົດໃນ text ແບບຄຳສັບເຕັມ
        ໂດຍໃຊ້ຊ່ອງຫວ່າງເປັນຕົວແບ່ງ
        """
        # ແຍກ text ອອກເປັນຄຳ
        text_lower = text.lower()
        text_lower = re.sub(r"[^\w\s]", " ", text_lower)
        text_words = text_lower.split()

        # ແຍກ key ອອກເປັນຄຳ
        key_words = key.lower().split()

        # ຖ້າ key ມີຄຳດຽວ
        if len(key_words) == 1:
            return key_words[0] in text_words

        # ຖ້າ key ມີຫຼາຍຄຳ - ກວດວ່າຕິດກັນ
        for i in range(len(text_words) - len(key_words) + 1):
            if text_words[i : i + len(key_words)] == key_words:
                return True

        return False

    def search(self, query: str) -> dict:
        """
        ຄົ້ນຫາໃນຖານຂໍ້ມູນ - ໃຊ້ query ດິບ
        """
        # ລຳດັບຄວາມສຳຄັນ
        categories = [
            ("capitals", self.capitals, 0.95),
            ("planets", self.planets, 0.9),
            ("chemistry", self.chemistry, 0.9),
            ("computer", self.computer, 0.95),
            ("physics", self.physics, 0.9),
            ("biology", self.biology, 0.9),
            ("history", self.history, 0.85),
            ("english", self.english, 0.9),
            ("general", self.general, 0.85),
            ("math_constants", self.math_constants, 0.9),
        ]

        # ກວດບໍລິບົດ
        context_map = {
            "capitals": ["capital"],
            "planets": ["planet"],
        }

        for category_name, category_data, confidence in categories:
            # ກວດບໍລິບົດຖ້າຈຳເປັນ
            if category_name in context_map:
                has_context = any(
                    w in query.lower() for w in context_map[category_name]
                )
                if not has_context:
                    continue

            # ຄົ້ນຫາໃນ query ດິບ
            for key, value in category_data.items():
                if self._exact_word_match(key, query):
                    return {
                        "answer": value,
                        "confidence": confidence,
                        "category": category_name,
                        "matched_key": key,
                    }

        return None

    def get_all_keys(self):
        """ສະແດງທຸກຄຳສຳຄັນ"""
        all_keys = []
        all_keys.extend(self.capitals.keys())
        all_keys.extend(self.planets.keys())
        all_keys.extend(self.math_constants.keys())
        all_keys.extend(self.physics.keys())
        all_keys.extend(self.chemistry.keys())
        all_keys.extend(self.biology.keys())
        all_keys.extend(self.history.keys())
        all_keys.extend(self.english.keys())
        all_keys.extend(self.computer.keys())
        all_keys.extend(self.general.keys())
        return all_keys


def test_knowledge_base():
    """ທົດສອບ Knowledge Base"""

    print("=" * 60)
    print("🧪 ທົດສອບ Knowledge Base")
    print("=" * 60)

    kb = KnowledgeBase()

    test_queries = [
        "What is the capital of France?",
        "What is the capital of Japan?",
        "What is the capital of Laos?",
        "Which planet is the Red Planet?",
        "What is H2O?",
        "What does CPU stand for?",
        "What is the speed of light?",
        "What is the largest ocean?",
        "What is the past tense of go?",
        "What is the powerhouse of the cell?",
        "What is the currency of Japan?",
        "What is the pH of water?",
        "Who was the first man on the moon?",
    ]

    for query in test_queries:
        result = kb.search(query)
        print(f"\n📝 {query}")
        if result:
            print(f"   ✅ {result['answer']}")
            print(f"   📊 {result['confidence']*100:.0f}% | {result['category']}")
        else:
            print(f"   ❌ ບໍ່ພົບ")

    print("\n" + "=" * 60)
    print(f"📊 ລວມຄຳສຳຄັນ: {len(kb.get_all_keys())}")
    print("=" * 60)


if __name__ == "__main__":
    test_knowledge_base()
