"""
src/question_analyzer.py
ວິເຄາະຄຳຖາມ ແລະ ຊອກຫາ MCQ
"""

import re
from typing import List, Dict, Optional


class QuestionAnalyzer:
    """ວິເຄາະຄຳຖາມ ແລະ ສະກັດ MCQ"""
    
    def __init__(self):
        """ຕັ້ງຄ່າ"""
        # ຮູບແບບການກວດຫາຄຳຖາມ
        self.question_patterns = [
            r'(?i)^(?:what|why|how|when|where|who|which|can|could|would|will|do|does|is|are|was|were)\s+',
            r'(?i)^[0-9]+[\.\)]\s+.+',
            r'(?i)^[a-z][\.\)]\s+.+',
            r'(?i).+\?$',
        ]
        
        # ຮູບແບບການກວດຫາຕົວເລືອກ
        self.option_patterns = [
            r'(?i)^([a-d][\.\)])\s*(.+)$',
            r'(?i)^([0-9]+[\.\)])\s*(.+)$',
            r'(?i)^[•\-\*]\s*(.+)$',
        ]
    
    def is_question(self, text: str) -> bool:
        """ກວດວ່າເປັນຄຳຖາມບໍ່"""
        text = text.strip()
        
        # ຖ້າມີເຄື່ອງໝາຍຄຳຖາມ
        if '?' in text:
            return True
        
        # ກວດດ້ວຍຮູບແບບ
        for pattern in self.question_patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def is_option(self, text: str) -> Optional[str]:
        """ກວດວ່າເປັນຕົວເລືອກ ແລະ ສະກັດຂໍ້ຄວາມ"""
        text = text.strip()
        
        for pattern in self.option_patterns:
            match = re.match(pattern, text, re.IGNORECASE)
            if match:
                # ຖ້າມີ 2 ກຸ່ມ (ຕົວເລືອກ ແລະ ຂໍ້ຄວາມ)
                if len(match.groups()) == 2:
                    return match.group(2).strip()
                return match.group(1).strip()
        
        return None
    
    def clean_options(self, options: List[str]) -> List[str]:
        """
        ກັ່ນຕອງຕົວເລືອກທີ່ບໍ່ຖືກຕ້ອງ
        
        Args:
            options: ລາຍຊື່ຕົວເລືອກ
        
        Returns:
            List[str]: ລາຍຊື່ຕົວເລືອກທີ່ກັ່ນຕອງແລ້ວ
        """
        cleaned = []
        
        for opt in options:
            opt = opt.strip()
            
            # ຕັດທີ່ຫວ່າງ ຫຼື ສັ້ນເກີນໄປ
            if len(opt) < 2:
                continue
            
            # ຕັດທີ່ຍາວເກີນໄປ (ບໍ່ແມ່ນຕົວເລືອກ)
            if len(opt) > 100:
                continue
            
            # ຕັດທີ່ມີຕົວອັກສອນພິເສດຫຼາຍ
            special_chars = sum(1 for c in opt if not c.isalnum() and c not in ' .,!?-()')
            if special_chars > len(opt) * 0.4:
                continue
            
            # ຕັດທີ່ເປັນຕົວເລກລ້ວນໆ
            if opt.replace('.', '').replace(',', '').strip().isdigit():
                continue
            
            cleaned.append(opt)
        
        # ຈຳກັດສູງສຸດ 6 ຕົວເລືອກ
        return cleaned[:6]
    
    def extract_mcq(self, text: str) -> Dict:
        """
        ສະກັດ MCQ ຈາກຂໍ້ຄວາມ
        
        Args:
            text: ຂໍ້ຄວາມທີ່ຕ້ອງການວິເຄາະ
        
        Returns:
            Dict: {
                "question": str,
                "options": List[str],
                "is_mcq": bool,
                "confidence": float
            }
        """
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not lines:
            return {
                "question": "",
                "options": [],
                "is_mcq": False,
                "confidence": 0.0
            }
        
        question = None
        options = []
        is_mcq = False
        confidence = 0.0
        
        # ຊອກຫາຄຳຖາມ
        for line in lines:
            if self.is_question(line):
                question = line
                confidence += 0.3
                break
        
        # ຖ້າບໍ່ເຫັນຄຳຖາມ, ໃຊ້ບັນທັດທຳອິດ
        if question is None:
            question = lines[0]
            if len(lines) > 1:
                confidence += 0.1
        
        # ຊອກຫາຕົວເລືອກ (ສະເພາະຕົວອັກສອນ A-D)
        option_letters = ['A', 'B', 'C', 'D']
        
        for line in lines:
            line_upper = line.upper()
            
            # ກວດວ່າຂຶ້ນຕົ້ນດ້ວຍ A., B., C., D.
            for letter in option_letters:
                if line_upper.startswith(f"{letter}.") or line_upper.startswith(f"{letter})"):
                    # ຕັດສ່ວນຕົວອັກສອນອອກ
                    option_text = line[2:].strip()
                    options.append(option_text)
                    confidence += 0.1
                    break
        
        # ຖ້າບໍ່ພົບຕົວເລືອກ A-D, ລອງໃຊ້ຮູບແບບອື່ນ
        if len(options) < 2:
            for line in lines:
                option_text = self.is_option(line)
                if option_text:
                    options.append(option_text)
                    confidence += 0.1
        
        # ກັ່ນຕອງຕົວເລືອກ
        options = self.clean_options(options)
        
        # ກວດວ່າເປັນ MCQ
        if len(options) >= 2:
            is_mcq = True
            confidence += 0.3
        
        # ປັບຄ່າຄວາມໝັ້ນໃຈ
        confidence = min(confidence, 1.0)
        
        return {
            "question": question,
            "options": options,
            "is_mcq": is_mcq,
            "confidence": round(confidence, 2)
        }
    
    def analyze_text(self, text: str) -> Dict:
        """
        ວິເຄາະຂໍ້ຄວາມຢ່າງສົມບູນ
        
        Returns:
            Dict: {
                "text": str,
                "lines": List[str],
                "mcq": Dict,
                "stats": Dict
            }
        """
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        mcq = self.extract_mcq(text)
        
        return {
            "text": text,
            "lines": lines,
            "mcq": mcq,
            "stats": {
                "total_lines": len(lines),
                "total_chars": len(text),
                "has_question": mcq["question"] != "",
                "has_options": len(mcq["options"]) > 0,
                "is_mcq": mcq["is_mcq"],
                "confidence": mcq["confidence"]
            }
        }


def test_analyzer():
    """ທົດສອບ Question Analyzer"""
    
    print("=" * 60)
    print("🧪 ທົດສອບ Question Analyzer")
    print("=" * 60)
    
    # ສ້າງຕົວວິເຄາະ
    analyzer = QuestionAnalyzer()
    
    # ທົດສອບຄຳຖາມຕົວຢ່າງ
    test_texts = [
        """
        What is the capital of France?
        A. London
        B. Paris
        C. Berlin
        D. Madrid
        """,
        
        """
        Which of the following is a programming language?
        A. Python
        B. Java
        C. C++
        D. All of the above
        """,
        
        """
        This is just a normal sentence without any question.
        """
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{'=' * 60}")
        print(f"ທົດສອບທີ {i}")
        print(f"{'=' * 60}")
        
        result = analyzer.analyze_text(text)
        
        print(f"📝 ຂໍ້ຄວາມ:")
        print(text.strip())
        
        print(f"\n📊 ຜົນການວິເຄາະ:")
        print(f"  ຈຳນວນບັນທັດ: {result['stats']['total_lines']}")
        print(f"  ເປັນຄຳຖາມ: {result['stats']['has_question']}")
        print(f"  ມີຕົວເລືອກ: {result['stats']['has_options']}")
        print(f"  ເປັນ MCQ: {result['stats']['is_mcq']}")
        print(f"  ຄວາມໝັ້ນໃຈ: {result['stats']['confidence'] * 100}%")
        
        if result['mcq']['is_mcq']:
            print(f"\n📝 MCQ ທີ່ພົບ:")
            print(f"  ຄຳຖາມ: {result['mcq']['question']}")
            print(f"  ຕົວເລືອກ:")
            for j, opt in enumerate(result['mcq']['options']):
                print(f"    {chr(65+j)}. {opt}")
        else:
            print("\n⚠️ ບໍ່ພົບ MCQ")
    
    print("\n" + "=" * 60)
    print("✅ ການທົດສອບສຳເລັດ!")


if __name__ == "__main__":
    test_analyzer()