import unittest
from calculator import ExpressionParser


class TestExpressionParser(unittest.TestCase):
    
    def test_basic_operations(self):
        test_cases = [
            ("2+3", 5),
            ("10-4", 6),
            ("3*4", 12),
            ("8/2", 4),
            ("2+3*4", 14),
            ("(2+3)*4", 20),
            ("10/2-3", 2),
            ("2.5+3.5", 6),
        ]
        
        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                parser = ExpressionParser(expr)
                result = parser.evaluate()
                self.assertAlmostEqual(result, expected)
    
    def test_complex_expressions(self):
        test_cases = [
            ("(2+3)*4-10/2", 15),
            ("2*3+4*5", 26),
            ("(1+2)*(3+4)", 21),
            ("10/(5-3)", 5),
            ("2.5*4+1.5", 11.5),
            ("-5+3", -2),
            ("(-5)+3", -2),
        ]
        
        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                parser = ExpressionParser(expr)
                result = parser.evaluate()
                self.assertAlmostEqual(result, expected)
    
    def test_invalid_expressions(self):
        invalid_exprs = [
            "2++3",
            "2/0",
            "(2+3",
            "2+3)",
            "abc",
            "2@3",
        ]
        
        for expr in invalid_exprs:
            with self.subTest(expr=expr):
                parser = ExpressionParser(expr)
                with self.assertRaises(ValueError):
                    parser.evaluate()


if __name__ == "__main__":
    unittest.main()