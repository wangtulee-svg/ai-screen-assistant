"""
src/math_engine.py
Math Engine ສຳລັບແກ້ໂຈດຄະນິດສາດ
"""

import re
import math
from sympy import (
    symbols, solve, simplify, expand, factor,
    sympify, sqrt, pi, E
)
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations,
    implicit_multiplication_application
)


class MathEngine:
    """ເຄື່ອງມືແກ້ໂຈດຄະນິດສາດ"""
    
    def __init__(self):
        # ຕົວແປ
        self.x, self.y, self.z = symbols('x y z')
        self.a, self.b, self.c = symbols('a b c')
        
        # ການແປງ
        self.transformations = (
            standard_transformations +
            (implicit_multiplication_application,)
        )
    
    def clean_text(self, text):
        """ລຶບຂໍ້ຄວາມທີ່ບໍ່ຈຳເປັນ"""
        text = text.lower()
        
        words_to_remove = [
            'what is', 'calculate', 'solve', 'find x', 
            'what is x', 'equals', 'equal', 'the value of',
            '?', ':', 'please', 'can you', 'find the'
        ]
        
        for word in words_to_remove:
            text = text.replace(word, '')
        
        return text.strip()
    
    def solve_arithmetic(self, expression):
        """ແກ້ໂຈດເລກຄະນິດພື້ນຖານ"""
        try:
            expr = self.clean_text(expression)
            
            # ປ່ຽນສັນຍະລັກ
            expr = expr.replace('×', '*').replace('÷', '/')
            expr = expr.replace('^', '**')
            expr = expr.replace('plus', '+').replace('minus', '-')
            expr = expr.replace('times', '*').replace('divided by', '/')
            
            # ຊອກຫາສົມຜົນ
            match = re.search(
                r'(\d+(?:\.\d+)?)\s*([+\-*/])\s*(\d+(?:\.\d+)?)', 
                expr
            )
            
            if match:
                a = float(match.group(1))
                op = match.group(2)
                b = float(match.group(3))
                
                if op == '+': result = a + b
                elif op == '-': result = a - b
                elif op == '*': result = a * b
                elif op == '/':
                    if b == 0: return None
                    result = a / b
                else: return None
                
                if result == int(result):
                    return str(int(result))
                return str(round(result, 4))
            
            return None
        except Exception:
            return None
    
    def solve_linear_equation(self, equation):
        """ແກ້ສົມຜົນເສັ້ນຊື່"""
        try:
            eq = self.clean_text(equation)
            
            if '=' not in eq:
                return None
            
            parts = eq.split('=')
            if len(parts) != 2:
                return None
            
            left = parts[0].strip()
            right = parts[1].strip()
            
            # ສ້າງ expression
            expr_str = f"({left}) - ({right})"
            
            try:
                expr = parse_expr(
                    expr_str,
                    transformations=self.transformations,
                    evaluate=True
                )
            except Exception as e:
                print(f"Parse error: {e}")
                return None
            
            # ແກ້
            solutions = solve(expr, self.x)
            
            if solutions:
                result_parts = []
                for s in solutions:
                    if s.is_integer:
                        result_parts.append(str(int(s)))
                    else:
                        result_parts.append(str(s))
                
                if len(result_parts) == 1:
                    return f"x = {result_parts[0]}"
                return f"x = {', '.join(result_parts)}"
            
            return None
        except Exception as e:
            print(f"Equation error: {e}")
            return None
    
    def calculate_percentage(self, question):
        """ຄຳນວນເປີເຊັນ"""
        try:
            match = re.search(
                r'(\d+(?:\.\d+)?)\s*%\s*(?:of)?\s*(\d+(?:\.\d+)?)', 
                question, re.I
            )
            if match:
                percent = float(match.group(1))
                number = float(match.group(2))
                result = (percent / 100) * number
                
                if result == int(result):
                    return str(int(result))
                return str(round(result, 4))
            return None
        except Exception:
            return None
    
    def solve_geometry(self, question):
        """ແກ້ໂຈດເລຂາຄະນິດ"""
        q = question.lower()
        
        # ພື້ນທີ່ວົງມົນ
        if 'area' in q and 'circle' in q:
            match = re.search(r'radius\s*(?:of|=|is)?\s*(\d+(?:\.\d+)?)', q)
            if match:
                r = float(match.group(1))
                area = math.pi * r ** 2
                return str(round(area, 2))
        
        # ພື້ນທີ່ສີ່ຫຼ່ຽມ
        if 'area' in q and ('rectangle' in q or 'square' in q):
            numbers = re.findall(r'(\d+(?:\.\d+)?)', q)
            if len(numbers) >= 2:
                w = float(numbers[0])
                h = float(numbers[1])
                area = w * h
                
                if area == int(area):
                    return str(int(area))
                return str(round(area, 2))
        
        return None
    
    def solve(self, question):
        """ແກ້ໂຈດຄະນິດສາດທຸກປະເພດ"""
        
        # 1. ລອງເປີເຊັນ
        result = self.calculate_percentage(question)
        if result:
            return {
                "answer": result,
                "confidence": 0.95,
                "explanation": f"Percentage: {result}"
            }
        
        # 2. ລອງເລຂາຄະນິດ
        result = self.solve_geometry(question)
        if result:
            return {
                "answer": result,
                "confidence": 0.9,
                "explanation": f"Geometry: {result}"
            }
        
        # 3. ລອງສົມຜົນ
        if 'x' in question.lower() and '=' in question:
            result = self.solve_linear_equation(question)
            if result:
                return {
                    "answer": result,
                    "confidence": 0.95,
                    "explanation": f"Equation: {result}"
                }
        
        # 4. ລອງເລກຄະນິດ
        result = self.solve_arithmetic(question)
        if result:
            return {
                "answer": result,
                "confidence": 0.95,
                "explanation": f"Arithmetic: {result}"
            }
        
        return None


def test_math_engine():
    """ທົດສອບ Math Engine"""
    
    print("=" * 60)
    print("🧪 ທົດສອບ Math Engine")
    print("=" * 60)
    
    engine = MathEngine()
    
    test_cases = [
        "What is 25 + 17?",
        "What is 100 / 4?",
        "What is 20% of 50?",
        "What is 15% of 200?",
        "Solve: 2x + 5 = 15",
        "Solve: 3x - 7 = 14",
        "Solve: x^2 - 4 = 0",
        "What is the area of a circle with radius 7?",
        "What is the area of a rectangle 5 x 3?",
    ]
    
    for i, question in enumerate(test_cases, 1):
        print(f"\n{'=' * 60}")
        print(f"ທົດສອບທີ {i}: {question}")
        print(f"{'=' * 60}")
        
        result = engine.solve(question)
        
        if result:
            print(f"✅ ຄຳຕອບ: {result['answer']}")
            print(f"📊 ຄວາມໝັ້ນໃຈ: {result['confidence'] * 100}%")
        else:
            print("⚠️ ບໍ່ສາມາດແກ້ໄດ້")
    
    print("\n" + "=" * 60)
    print("✅ ການທົດສອບສຳເລັດ!")


if __name__ == "__main__":
    test_math_engine()