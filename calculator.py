import sys
import re
from typing import List, Union


class ExpressionParser:
    PRECEDENCE = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '^': 3
    }
    
    ASSOCIATIVITY = {
        '+': 'left',
        '-': 'left',
        '*': 'left',
        '/': 'left',
        '^': 'right'
    }
    
    def __init__(self, expression: str):
        self.expression = expression.strip()
        self.tokens = []
        self.rpn_tokens = []
        
    def tokenize(self) -> List[str]:
        tokens = []
        i = 0
        expr = self.expression
        
        while i < len(expr):
            char = expr[i]
            
            if char.isspace():
                i += 1
                continue
                
            if char.isdigit() or (char == '.' and i + 1 < len(expr) and expr[i + 1].isdigit()):
                num_str = ''
                has_decimal = False
                
                while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                    if expr[i] == '.':
                        if has_decimal:
                            raise ValueError(f"Invalid number: multiple decimal points")
                        has_decimal = True
                    num_str += expr[i]
                    i += 1
                
                if num_str and (not tokens or tokens[-1] in '+-*/^(' or tokens[-1] in self.PRECEDENCE):
                    tokens.append(num_str)
                else:
                    tokens.append(num_str)
                continue
                
            if char in '+-*/^()':
                if char == '-' and (not tokens or tokens[-1] in '(*+-/^'):
                    if i + 1 < len(expr) and (expr[i+1].isdigit() or expr[i+1] == '('):
                        tokens.append('_')
                        i += 1
                        continue
                tokens.append(char)
                i += 1
                continue
                
            raise ValueError(f"Invalid character: {char}")
        
        self.tokens = tokens
        return tokens
    
    def infix_to_rpn(self) -> List[str]:
        if not self.tokens:
            self.tokenize()
            
        output_queue = []
        operator_stack = []
        
        for token in self.tokens:
            if token.replace('.', '').replace('-', '').isdigit() or token == '_':
                if token == '_':
                    output_queue.append('-1')
                else:
                    output_queue.append(token)
                    
            elif token.isalpha():
                operator_stack.append(token)
                
            elif token in self.PRECEDENCE:
                while (operator_stack and operator_stack[-1] != '(' and
                       (self.PRECEDENCE.get(operator_stack[-1], 0) > self.PRECEDENCE[token] or
                        (self.PRECEDENCE.get(operator_stack[-1], 0) == self.PRECEDENCE[token] and
                         self.ASSOCIATIVITY[token] == 'left'))):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
                
            elif token == '(':
                operator_stack.append(token)
                
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses")
                operator_stack.pop()
                
                if operator_stack and operator_stack[-1].isalpha():
                    output_queue.append(operator_stack.pop())
        
        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())
        
        self.rpn_tokens = output_queue
        return output_queue
    
    def evaluate_rpn(self) -> float:
        if not self.rpn_tokens:
            self.infix_to_rpn()
            
        stack = []
        
        for token in self.rpn_tokens:
            if token.replace('.', '').replace('-', '').replace('_', '').isdigit():
                if token == '_':
                    stack.append(-1)
                else:
                    stack.append(float(token))
                    
            elif token in self.PRECEDENCE:
                if len(stack) < 2:
                    raise ValueError(f"Invalid expression: missing operands for operator {token}")
                    
                b = stack.pop()
                a = stack.pop()
                
                if token == '+':
                    result = a + b
                elif token == '-':
                    result = a - b
                elif token == '*':
                    result = a * b
                elif token == '/':
                    if b == 0:
                        raise ValueError("Division by zero")
                    result = a / b
                elif token == '^':
                    result = a ** b
                else:
                    raise ValueError(f"Unknown operator: {token}")
                    
                stack.append(result)
                
        if len(stack) != 1:
            raise ValueError("Invalid expression")
            
        return stack[0]
    
    def evaluate(self) -> float:
        self.tokenize()
        self.infix_to_rpn()
        return self.evaluate_rpn()


def read_from_file(filename: str) -> str:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) == 2:
        expression = read_from_file(sys.argv[1])
    elif len(sys.argv) == 1:
        print("Enter expression (type 'quit' to exit):")
        expression = input().strip()
        if expression.lower() == 'quit':
            return
    else:
        print("Usage: python calculator.py [filename]")
        print("   or: python calculator.py")
        sys.exit(1)
    
    try:
        parser = ExpressionParser(expression)
        result = parser.evaluate()
        
        print(f"Expression: {expression}")
        print(f"Tokens: {parser.tokens}")
        print(f"RPN: {parser.rpn_tokens}")
        print(f"Result: {result}")
        
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()