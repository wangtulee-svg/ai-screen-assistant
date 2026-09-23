"""
src/ai_solver.py
AI Solver ສຳລັບຕອບຄຳຖາມ
"""

import re
from typing import Dict, List, Optional
import random


class AISolver:
    """AI Solver ສຳລັບຕອບຄຳຖາມ"""
    
    def __init__(self):
        """ຕັ້ງຄ່າ"""
        # ຂໍ້ມູນຄວາມຮູ້ພື້ນຖານ (ສາມາດເພີ່ມໄດ້)
        self.knowledge_base = {
            "capital": {
                "laos": "Vientiane",
                "france": "Paris",
                "japan": "Tokyo",
                "thailand": "Bangkok",
                "vietnam": "Hanoi",
                "cambodia": "Phnom Penh",
                "china": "Beijing",
                "usa": "Washington D.C.",
                "uk": "London",
                "germany": "Berlin"
            },
            "planet": {
                "red planet": "Mars",
                "largest": "Jupiter",
                "smallest": "Mercury",
                "closest to sun": "Mercury",
                "farthest": "Neptune"
            },
            "math": {
                "2+2": "4",
                "5+3": "8",
                "10-3": "7",
                "6*6": "36",
                "12/4": "3"
            },
            "programming": {
                "python": "A high-level programming language",
                "java": "A popular programming language",
                "c++": "A powerful programming language"
            }
        }
    
    def solve_mcq(self, question: str, options: List[str]) -> Dict:
        """
        ແກ້ MCQ ໂດຍໃຊ້ Knowledge Base
        
        Args:
            question: ຄຳຖາມ
            options: ລາຍຊື່ຕົວເລືອກ
        
        Returns:
            Dict: {
                "answer": str,
                "confidence": float,
                "explanation": str
            }
        """
        question_lower = question.lower()
        
        # ຊອກຫາຄຳຕອບຈາກ Knowledge Base
        answer = None
        confidence = 0.0
        explanation = ""
        
        # 1. ກວດຫາຄຳຖາມກ່ຽວກັບເມືອງຫຼວງ
        if "capital" in question_lower or "ເມືອງຫຼວງ" in question:
            for country, capital in self.knowledge_base["capital"].items():
                if country in question_lower or country in question:
                    answer = capital
                    confidence = 0.9
                    explanation = f"{country.capitalize()} has capital {capital}"
                    break
        
        # 2. ກວດຫາຄຳຖາມກ່ຽວກັບດາວເຄາະ
        if "planet" in question_lower or "ດາວ" in question:
            for key, value in self.knowledge_base["planet"].items():
                if key in question_lower or key in question:
                    answer = value
                    confidence = 0.85
                    explanation = f"The {key} is {value}"
                    break
        
        # 3. ກວດຫາສົມຜົນຄະນິດສາດ
        math_match = re.search(r'(\d+)\s*([+\-*/])\s*(\d+)', question)
        if math_match:
            a = int(math_match.group(1))
            op = math_match.group(2)
            b = int(math_match.group(3))
            
            if op == '+': result = a + b
            elif op == '-': result = a - b
            elif op == '*': result = a * b
            elif op == '/': 
                result = a / b if b != 0 else "undefined"
            else: result = "unknown"
            
            answer = str(result)
            confidence = 0.95
            explanation = f"{a} {op} {b} = {result}"
        
        # 4. ຖ້າຍັງບໍ່ພົບ, ລອງຊອກຫາໃນ options
        if answer is None and options:
            for opt in options:
                opt_lower = opt.lower()
                for key, value in self.knowledge_base["capital"].items():
                    if key in question_lower and value.lower() in opt_lower:
                        answer = opt
                        confidence = 0.7
                        explanation = f"Found match: {value}"
                        break
                if answer:
                    break
        
        # 5. ຖ້າຍັງບໍ່ພົບ, ເລືອກສຸ່ມ
        if answer is None and options:
            answer = random.choice(options)
            confidence = 0.2
            explanation = "No confident match found, making random guess"
        
        return {
            "answer": answer,
            "confidence": confidence,
            "explanation": explanation
        }
    
    def get_answer(self, question: str, options: List[str] = None) -> Dict:
        """
        ຕອບຄຳຖາມ
        
        Args:
            question: ຄຳຖາມ
            options: ຕົວເລືອກ (ຖ້າມີ)
        
        Returns:
            Dict: {
                "answer": str,
                "confidence": float,
                "explanation": str
            }
        """
        if options:
            return self.solve_mcq(question, options)
        
        # ຄຳຖາມທົ່ວໄປ (ບໍ່ມີຕົວເລືອກ)
        question_lower = question.lower()
        
        # ຊອກຫາໃນ Knowledge Base
        for category, items in self.knowledge_base.items():
            for key, value in items.items():
                if key in question_lower:
                    return {
                        "answer": value,
                        "confidence": 0.8,
                        "explanation": f"Based on knowledge base: {key}"
                    }
        
        return {
            "answer": "I don't have enough information to answer this question.",
            "confidence": 0.0,
            "explanation": "No matching knowledge found"
        }


def test_solver():
    """ທົດສອບ AI Solver"""
    
    print("=" * 60)
    print("🧪 ທົດສອບ AI Solver")
    print("=" * 60)
    
    solver = AISolver()
    
    test_cases = [
        {
            "question": "What is the capital of France?",
            "options": ["London", "Paris", "Berlin", "Madrid"]
        },
        {
            "question": "What is 2 + 2?",
            "options": ["3", "4", "5", "6"]
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "options": ["Venus", "Mars", "Jupiter", "Saturn"]
        },
        {
            "question": "What is the capital of Laos?",
            "options": ["Bangkok", "Hanoi", "Vientiane", "Phnom Penh"]
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'=' * 60}")
        print(f"ທົດສອບທີ {i}")
        print(f"{'=' * 60}")
        print(f"ຄຳຖາມ: {test['question']}")
        print(f"ຕົວເລືອກ: {test['options']}")
        
        result = solver.solve_mcq(test['question'], test['options'])
        print(f"\n📝 ຄຳຕອບ: {result['answer']}")
        print(f"📊 ຄວາມໝັ້ນໃຈ: {result['confidence'] * 100}%")
        print(f"💡 ຄຳອະທິບາຍ: {result['explanation']}")
    
    print("\n" + "=" * 60)
    print("✅ ການທົດສອບສຳເລັດ!")


if __name__ == "__main__":
    test_solver()