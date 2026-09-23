"""
src/ai_solver_v4.py
AI Solver V4 - ແກ້ໄຂສຸດທ້າຍ
"""

import sys
import os
import re
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.math_engine import MathEngine
from src.knowledge_base import KnowledgeBase
from src.ai_solver_v2 import AISolverV2


class AISolverV4:
    """AI Solver V4 ທີ່ເກັ່ງທີ່ສຸດ"""
    
    def __init__(self):
        self.math_engine = MathEngine()
        self.knowledge_base = KnowledgeBase()
        self.base_solver = AISolverV2()
        
        print("✅ AI Solver V4 ພ້ອມໃຊ້ງານ!")
        print(f"📚 ຄວາມຮູ້: {len(self.knowledge_base.get_all_keys())} ຄຳສຳຄັນ")
    
    def clean_answer(self, answer: str) -> str:
        """ກັ່ນຕອງຄຳຕອບ"""
        if not answer:
            return answer
        
        answer = answer.strip()
        
        if len(answer) > 1:
            last_char = answer[-1]
            if last_char.lower() in 'abcd' or last_char in '.,;:':
                if answer[-2].isalpha():
                    words = answer.split()
                    if words:
                        last_word = words[-1]
                        if len(last_word) > 1 and last_word[-1].lower() in 'abcd':
                            answer = answer[:-1].strip()
        
        return answer
    
    def classify_question(self, question: str) -> str:
        """
        ຈຳແນກປະເພດຄຳຖາມ - ແກ້ໄຂສຸດທ້າຍ
        """
        q = question.lower()
        
        # 1. ກວດວ່າມີຕົວແປ x ແລະ = (ສົມຜົນ)
        if '=' in q and 'x' in q:
            return "math"
        
        # 2. ກວດວ່າມີສັນຍະລັກຄະນິດສາດ
        if re.search(r'\d+\s*[+\-*/=^%]\s*\d+', q):
            return "math"
        
        # 3. ກວດຄຳສັບຄະນິດສາດ
        math_keywords = [
            'solve', 'calculate', 'equation', 'area', 
            'percent', '%', 'perimeter', 'volume',
            'circumference', 'radius', 'diameter'
        ]
        if any(word in q for word in math_keywords):
            return "math"
        
        # 4. ກວດວ່າເປັນ chemistry
        chem_keywords = ['chemical', 'symbol', 'formula', 'element']
        if any(word in q for word in chem_keywords):
            return "chemistry"
        
        return "knowledge"
    
    def find_in_options(self, answer: str, options: List[str]) -> Optional[str]:
        """ຊອກຫາຄຳຕອບໃນ options"""
        answer_clean = answer.lower().strip()
        
        for opt in options:
            opt_clean = opt.lower().strip()
            
            if answer_clean == opt_clean:
                return opt
            
            if answer_clean in opt_clean or opt_clean in answer_clean:
                return opt
            
            ans_nums = re.findall(r'\d+\.?\d*', answer_clean)
            opt_nums = re.findall(r'\d+\.?\d*', opt_clean)
            
            if ans_nums and opt_nums:
                try:
                    ans_val = float(ans_nums[0])
                    opt_val = float(opt_nums[0])
                    
                    if abs(ans_val - opt_val) < 0.01:
                        return opt
                except ValueError:
                    pass
        
        return None
    
    def solve_mcq(self, question: str, options: List[str]) -> Dict:
        """ແກ້ MCQ"""
        
        q_type = self.classify_question(question)
        
        # ============================================================
        # 1. ຄະນິດສາດ
        # ============================================================
        if q_type == "math":
            math_result = self.math_engine.solve(question)
            
            if math_result:
                answer = self.clean_answer(math_result['answer'])
                matched = self.find_in_options(answer, options)
                
                if matched:
                    return {
                        "answer": matched,
                        "confidence": math_result['confidence'],
                        "explanation": f"Math Engine: {math_result['explanation']}"
                    }
                
                return {
                    "answer": answer,
                    "confidence": math_result['confidence'],
                    "explanation": math_result['explanation']
                }
        
        # ============================================================
        # 2. Chemistry - ກວດກ່ອນ Knowledge Base
        # ============================================================
        if q_type == "chemistry":
            chem_result = self.knowledge_base.search(question)
            
            if chem_result and chem_result['category'] == 'chemistry':
                answer = self.clean_answer(chem_result['answer'])
                matched = self.find_in_options(answer, options)
                
                if matched:
                    return {
                        "answer": matched,
                        "confidence": chem_result['confidence'],
                        "explanation": f"Chemistry: {chem_result['matched_key']}"
                    }
                
                return {
                    "answer": answer,
                    "confidence": chem_result['confidence'],
                    "explanation": f"Chemistry: {chem_result['matched_key']}"
                }
        
        # ============================================================
        # 3. Knowledge Base
        # ============================================================
        kb_result = self.knowledge_base.search(question)
        
        if kb_result:
            answer = self.clean_answer(kb_result['answer'])
            matched = self.find_in_options(answer, options)
            
            if matched:
                return {
                    "answer": matched,
                    "confidence": kb_result['confidence'],
                    "explanation": f"Knowledge Base: {kb_result['category']}"
                }
            
            return {
                "answer": answer,
                "confidence": kb_result['confidence'],
                "explanation": f"Knowledge Base: {kb_result['category']}"
            }
        
        # ============================================================
        # 4. Base Solver V2 (fallback)
        # ============================================================
        result = self.base_solver.solve_mcq(question, options)
        result['answer'] = self.clean_answer(result['answer'])
        
        return result
    
    def get_answer(self, question: str, options: List[str] = None) -> Dict:
        """ຕອບຄຳຖາມ"""
        if options:
            return self.solve_mcq(question, options)
        
        math_result = self.math_engine.solve(question)
        if math_result:
            return math_result
        
        kb_result = self.knowledge_base.search(question)
        if kb_result:
            return kb_result
        
        return {
            "answer": "ບໍ່ສາມາດຕອບໄດ້",
            "confidence": 0.0,
            "explanation": "No matching solution found"
        }


def test_solver_v4():
    """ທົດສອບ AI Solver V4"""
    
    print("=" * 60)
    print("🧪 ທົດສອບ AI Solver V4")
    print("=" * 60)
    
    solver = AISolverV4()
    
    test_cases = [
        # Math
        {"q": "Solve: 3x - 7 = 14", 
         "opts": ["x = 5", "x = 7", "x = 9", "x = 11"], 
         "exp": "x = 7"},
        {"q": "Solve: 2x + 5 = 15", 
         "opts": ["x = 3", "x = 5", "x = 7", "x = 10"], 
         "exp": "x = 5"},
        {"q": "What is 25% of 80?", 
         "opts": ["15", "20", "25", "30"], 
         "exp": "20"},
        {"q": "What is the area of a circle with radius 7?", 
         "opts": ["153.94", "100", "200", "50"], 
         "exp": "153.94"},
        
        # Chemistry
        {"q": "What is the chemical symbol for gold?", 
         "opts": ["Go", "Gd", "Au", "Ag"], 
         "exp": "Au"},
        {"q": "What is the chemical symbol for silver?", 
         "opts": ["Si", "Ag", "Au", "Sv"], 
         "exp": "Ag"},
        {"q": "What is the chemical formula for water?", 
         "opts": ["CO2", "H2O", "NaCl", "O2"], 
         "exp": "H2O"},
        
        # Knowledge
        {"q": "What is the capital of Laos?", 
         "opts": ["Bangkok", "Hanoi", "Vientiane", "Phnom Penh"], 
         "exp": "Vientiane"},
        {"q": "What is the past tense of go?", 
         "opts": ["Goed", "Went", "Gone", "Going"], 
         "exp": "Went"},
    ]
    
    correct = 0
    total = len(test_cases)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'=' * 60}")
        print(f"ທົດສອບທີ {i}")
        print(f"{'=' * 60}")
        print(f"📝 ຄຳຖາມ: {test['q']}")
        print(f"📋 ຕົວເລືອກ: {test['opts']}")
        print(f"🎯 ຄາດຫວັງ: {test['exp']}")
        
        result = solver.solve_mcq(test['q'], test['opts'])
        
        print(f"\n✅ ຕອບ: {result['answer']}")
        print(f"📊 ຄວາມໝັ້ນໃຈ: {result['confidence'] * 100:.0f}%")
        print(f"💡 {result['explanation']}")
        
        if test['exp'].lower() in result['answer'].lower():
            print("✅ ຖືກຕ້ອງ!")
            correct += 1
        else:
            print(f"❌ ຜິດ! ຄວນເປັນ {test['exp']}")
    
    print("\n" + "=" * 60)
    print(f"📊 ຜົນລວມ: {correct}/{total} ຖືກຕ້ອງ")
    print(f"📈 ອັດຕາ: {correct/total*100:.0f}%")
    print("=" * 60)


if __name__ == "__main__":
    test_solver_v4()