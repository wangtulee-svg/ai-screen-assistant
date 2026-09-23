"""
src/ai_solver_v2.py
AI Solver ທີ່ປັບປຸງແລ້ວ - ຮອງຮັບຫຼາຍຫົວຂໍ້
"""

import re
import json
import os
from typing import Dict, List, Optional


class AISolverV2:
    """AI Solver ທີ່ປັບປຸງແລ້ວ"""
    
    def __init__(self):
        """ຕັ້ງຄ່າ"""
        # ຂໍ້ມູນຄວາມຮູ້ທີ່ຂະຫຍາຍອອກ
        self.knowledge_base = {
            # ເມືອງຫຼວງ
            "capital": {
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
                "korea": "Seoul",
                "south korea": "Seoul",
                "singapore": "Singapore",
                "malaysia": "Kuala Lumpur",
                "indonesia": "Jakarta",
                "philippines": "Manila",
                "myanmar": "Naypyidaw",
                "egypt": "Cairo",
                "south africa": "Pretoria"
            },
            
            # ດາວເຄາະ
            "planet": {
                "red planet": "Mars",
                "largest planet": "Jupiter",
                "smallest planet": "Mercury",
                "closest to sun": "Mercury",
                "farthest from sun": "Neptune",
                "hottest planet": "Venus",
                "coldest planet": "Neptune",
                "blue planet": "Earth",
                "ringed planet": "Saturn"
            },
            
            # ວິທະຍາສາດ
            "science": {
                "h2o": "Water",
                "co2": "Carbon Dioxide",
                "o2": "Oxygen",
                "n2": "Nitrogen",
                "nacl": "Sodium Chloride (Salt)",
                "au": "Gold",
                "ag": "Silver",
                "fe": "Iron",
                "cu": "Copper",
                "speed of light": "299,792,458 m/s",
                "gravity": "9.8 m/s²",
                "boiling point of water": "100°C (212°F)",
                "freezing point of water": "0°C (32°F)"
            },
            
            # ຄະນິດສາດ
            "math": {
                "pi": "3.14159",
                "e": "2.71828",
                "golden ratio": "1.61803",
                "square root of 2": "1.41421"
            },
            
            # ຄອມພິວເຕີ
            "programming": {
                "python": "A high-level programming language",
                "java": "A popular OOP programming language",
                "javascript": "A web programming language",
                "c++": "A powerful systems programming language",
                "html": "HyperText Markup Language",
                "css": "Cascading Style Sheets",
                "sql": "Structured Query Language",
                "api": "Application Programming Interface",
                "cpu": "Central Processing Unit",
                "ram": "Random Access Memory",
                "rom": "Read-Only Memory",
                "gpu": "Graphics Processing Unit",
                "os": "Operating System",
                "dbms": "Database Management System",
                "url": "Uniform Resource Locator",
                "http": "HyperText Transfer Protocol",
                "https": "HTTP Secure",
                "dns": "Domain Name System",
                "ip": "Internet Protocol"
            }
        }
        
        # ຂໍ້ມູນຄວາມຮູ້ສະເພາະວິຊາ
        self.subject_knowledge = {
            "database": {
                "primary key": "A field that uniquely identifies each record in a table",
                "foreign key": "A field that references a primary key in another table",
                "normalization": "The process of organizing data to reduce redundancy",
                "sql": "Structured Query Language for managing databases",
                "dbms": "Database Management System"
            },
            "network": {
                "lan": "Local Area Network",
                "wan": "Wide Area Network",
                "ip": "Internet Protocol",
                "dns": "Domain Name System",
                "http": "HyperText Transfer Protocol"
            }
        }
    
    def solve_mcq(self, question: str, options: List[str]) -> Dict:
        """ແກ້ MCQ"""
        question_lower = question.lower()
        
        # 1. ກວດຫາເມືອງຫຼວງ
        if "capital" in question_lower:
            for country, capital in self.knowledge_base["capital"].items():
                if country in question_lower:
                    # ຊອກຫາໃນ options
                    for opt in options:
                        if capital.lower() in opt.lower():
                            return {
                                "answer": opt,
                                "confidence": 0.95,
                                "explanation": f"The capital of {country.title()} is {capital}"
                            }
                    return {
                        "answer": capital,
                        "confidence": 0.9,
                        "explanation": f"The capital of {country.title()} is {capital}"
                    }
        
        # 2. ກວດຫາດາວເຄາະ
        if "planet" in question_lower:
            for key, value in self.knowledge_base["planet"].items():
                if key in question_lower:
                    for opt in options:
                        if value.lower() in opt.lower():
                            return {
                                "answer": opt,
                                "confidence": 0.9,
                                "explanation": f"The {key} is {value}"
                            }
        
        # 3. ກວດຫາຄະນິດສາດ
        math_result = self._solve_math(question)
        if math_result:
            for opt in options:
                if math_result.lower() in opt.lower():
                    return {
                        "answer": opt,
                        "confidence": 0.95,
                        "explanation": f"Calculated result: {math_result}"
                    }
        
        # 4. ກວດຫາໃນ Knowledge Base
        for category, items in self.knowledge_base.items():
            for key, value in items.items():
                if key in question_lower:
                    for opt in options:
                        if value.lower() in opt.lower():
                            return {
                                "answer": opt,
                                "confidence": 0.85,
                                "explanation": f"{key.title()}: {value}"
                            }
        
        # 5. ຖ້າບໍ່ພົບ, ເລືອກອັນທີ່ຍາວທີ່ສຸດ (ມັກຈະຖືກ)
        if options:
            longest = max(options, key=len)
            return {
                "answer": longest,
                "confidence": 0.3,
                "explanation": "No confident match, selecting the most detailed option"
            }
        
        return {
            "answer": "Unknown",
            "confidence": 0.0,
            "explanation": "Could not determine answer"
        }
    
    def _solve_math(self, question: str) -> Optional[str]:
        """ແກ້ໂຈດຄະນິດສາດ"""
        # ລຶບຂໍ້ຄວາມທີ່ບໍ່ຈຳເປັນ
        question = question.lower()
        question = re.sub(r'what is|calculate|solve|=', '', question)
        question = question.strip()
        
        # ກວດຫາສົມຜົນງ່າຍ
        match = re.search(r'(\d+)\s*([+\-*/])\s*(\d+)', question)
        if match:
            a = int(match.group(1))
            op = match.group(2)
            b = int(match.group(3))
            
            if op == '+': result = a + b
            elif op == '-': result = a - b
            elif op == '*': result = a * b
            elif op == '/':
                if b == 0:
                    return "undefined"
                result = a / b
                if result.is_integer():
                    result = int(result)
            else:
                return None
            
            return str(result)
        
        return None


def test_solver_v2():
    """ທົດສອບ AI Solver V2"""
    
    print("=" * 60)
    print("🧪 ທົດສອບ AI Solver V2")
    print("=" * 60)
    
    solver = AISolverV2()
    
    test_cases = [
        {
            "question": "What is the capital of France?",
            "options": ["London", "Paris", "Berlin", "Madrid"]
        },
        {
            "question": "What is the capital of Japan?",
            "options": ["Seoul", "Tokyo", "Beijing", "Bangkok"]
        },
        {
            "question": "What is 25 + 17?",
            "options": ["40", "42", "45", "48"]
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "options": ["Venus", "Mars", "Jupiter", "Saturn"]
        },
        {
            "question": "What is the capital of Laos?",
            "options": ["Bangkok", "Hanoi", "Vientiane", "Phnom Penh"]
        },
        {
            "question": "What is 100 / 4?",
            "options": ["20", "25", "30", "40"]
        },
        {
            "question": "What is H2O?",
            "options": ["Gold", "Water", "Salt", "Oxygen"]
        },
        {
            "question": "What does CPU stand for?",
            "options": ["Central Processing Unit", "Computer Personal Unit", "Central Program Unit", "Control Processing Unit"]
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'=' * 60}")
        print(f"ທົດສອບທີ {i}")
        print(f"{'=' * 60}")
        print(f"📝 ຄຳຖາມ: {test['question']}")
        print(f"📋 ຕົວເລືອກ: {test['options']}")
        
        result = solver.solve_mcq(test['question'], test['options'])
        
        print(f"\n✅ ຄຳຕອບ: {result['answer']}")
        print(f"📊 ຄວາມໝັ້ນໃຈ: {result['confidence'] * 100}%")
        print(f"💡 {result['explanation']}")
    
    print("\n" + "=" * 60)
    print("✅ ການທົດສອບສຳເລັດ!")


if __name__ == "__main__":
    test_solver_v2()