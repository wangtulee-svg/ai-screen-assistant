"""
src/ai_solver_v3.py
AI Solver V3 - ໃຊ້ Math Engine + Knowledge Base
"""

import sys
import os
import re
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.math_engine import MathEngine
from src.ai_solver_v2 import AISolverV2


class AISolverV3:
    """AI Solver V3 ທີ່ເກັ່ງທີ່ສຸດ"""
    
    def __init__(self):
        self.math_engine = MathEngine()
        self.base_solver = AISolverV2()
        
        print("✅ AI Solver V3 ພ້ອມໃຊ້ງານ!")
    
    def clean_answer(self, answer: str) -> str:
        """
        ກັ່ນຕອງຄຳຕອບໃຫ້ສະອາດ
        """
        if not answer:
            return answer
        
        # ລຶບຊ່ອງຫວ່າງ
        answer = answer.strip()
        
        # ລຶບຕົວອັກສອນທີ່ບໍ່ຕ້ອງການຢູ່ທ້າຍ
        # ເຊັ່ນ: "Vientiane a" → "Vientiane"
        #       "Mars b" → "Mars"
        #       "8." → "8"
        
        # ກວດວ່າມີຕົວອັກສອນດຽວຢູ່ທ້າຍ
        if len(answer) > 1:
            last_char = answer[-1]
            
            # ຖ້າເປັນ a, b, c, d ດຽວໆ ຫຼື . , ; :
            if last_char.lower() in 'abcd' or last_char in '.,;:':
                # ກວດວ່າຕົວອັກສອນກ່ອນໜ້າເປັນຕົວໜັງສື
                if answer[-2].isalpha():
                    # ກວດວ່າຕ້ອງລຶບຫຼືບໍ່
                    # ຖ້າຄຳສຸດທ້າຍຍາວກວ່າ 2 ຕົວ
                    words = answer.split()
                    if words:
                        last_word = words[-1]
                        # ຖ້າຄຳສຸດທ້າຍຍາວກວ່າ 1 ຕົວ ແລະ ລົງທ້າຍດ້ວຍ a/b/c/d
                        if len(last_word) > 1 and last_word[-1].lower() in 'abcd':
                            # ລຶບຕົວອັກສອນສຸດທ້າຍ
                            answer = answer[:-1].strip()
        
        return answer
    
    def classify_question(self, question: str) -> str:
        """ຈຳແນກປະເພດຄຳຖາມ"""
        q = question.lower()
        
        # ຄະນິດສາດ
        if re.search(r'\d+\s*[+\-*/=^%]\s*\d+', q):
            return "math"
        if any(word in q for word in 
               ['solve', 'calculate', 'equation', 'area', 'percent', '%']):
            return "math"
        if '=' in q and 'x' in q:
            return "math"
        
        # ເມືອງຫຼວງ
        if 'capital' in q:
            return "capital"
        
        # ດາວເຄາະ
        if 'planet' in q:
            return "planet"
        
        # ວິທະຍາສາດ
        if any(word in q for word in ['chemical', 'h2o', 'co2', 'element']):
            return "science"
        
        # ໂປຣແກຣມມິ່ງ
        if any(word in q for word in 
               ['programming', 'code', 'cpu', 'ram', 'api']):
            return "programming"
        
        return "general"
    
    def find_in_options(self, answer: str, options: List[str]) -> Optional[str]:
        """ຊອກຫາຄຳຕອບໃນ options"""
        answer_clean = answer.lower().strip()
        
        for opt in options:
            opt_clean = opt.lower().strip()
            
            # ກວດສອບແບບຊື່
            if answer_clean == opt_clean:
                return opt
            
            # ກວດສອບວ່າມີຢູ່ໃນກັນ
            if answer_clean in opt_clean or opt_clean in answer_clean:
                return opt
            
            # ກວດສອບຕົວເລກ
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
        
        # ໃຊ້ base_solver
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
        
        return {
            "answer": "ບໍ່ສາມາດຕອບໄດ້",
            "confidence": 0.0,
            "explanation": "No matching solution found"
        }


def test_solver_v3():
    """ທົດສອບ AI Solver V3"""
    
    print("=" * 60)
    print("🧪 ທົດສອບ AI Solver V3")
    print("=" * 60)
    
    solver = AISolverV3()
    
    test_cases = [
        {"q": "What is the capital of Laos?", "opts": ["Bangkok", "Hanoi", "Vientiane", "Phnom Penh"], "exp": "Vientiane"},
        {"q": "What is 5 + 3?", "opts": ["6", "7", "8", "9"], "exp": "8"},
        {"q": "Which planet is the Red Planet?", "opts": ["Venus", "Mars", "Jupiter", "Saturn"], "exp": "Mars"},
        {"q": "What is 25 + 17?", "opts": ["40", "42", "45", "48"], "exp": "42"},
        {"q": "Solve: 2x + 5 = 15", "opts": ["x = 3", "x = 5", "x = 7", "x = 10"], "exp": "x = 5"},
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
    test_solver_v3()