import sys
from typing import List


class ExpressionParser:
    PRECEDENCE = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
    }
    
    ASSOCIATIVITY = {
        '+': 'left',
        '-': 'left',
        '*': 'left',
        '/': 'left',
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
            
            if char.isdigit() or char == '.':
                num_str = ''
                has_decimal = False
                
                while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                    if expr[i] == '.':
                        if has_decimal:
                            raise ValueError("Invalid number: multiple decimal points")
                        has_decimal = True
                    num_str += expr[i]
                    i += 1
                tokens.append(num_str)
                continue
            
            if char in '+-*/()':
                if char == '-':
                    if not tokens or tokens[-1] in '()*/+-':
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
            
        output = []
        stack = []
        
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            
            if token.replace('.', '').isdigit():
                output.append(token)
            
            elif token == '_':
                if i + 1 < len(self.tokens) and self.tokens[i+1].replace('.', '').isdigit():
                    output.append('-' + self.tokens[i+1])
                    i += 1 
                else:
                    stack.append('_')
            
            elif token in self.PRECEDENCE:
                while (stack and stack[-1] != '(' and 
                       stack[-1] != '_' and
                       self.PRECEDENCE.get(stack[-1], 0) >= self.PRECEDENCE[token]):
                    output.append(stack.pop())
                stack.append(token)
            
            elif token == '(':
                stack.append(token)
            
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack:
                    raise ValueError("Mismatched parentheses")
                stack.pop()              
            i += 1
        
        while stack:
            if stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output.append(stack.pop())
        
        self.rpn_tokens = output
        return output
    
    def evaluate_rpn(self) -> float:
        if not self.rpn_tokens:
            self.infix_to_rpn()
            
        stack = []
        
        for token in self.rpn_tokens:
            if token.replace('.', '').replace('-', '').isdigit():
                stack.append(float(token))
            
            elif token in self.PRECEDENCE:
                if len(stack) < 2:
                    raise ValueError("Invalid expression")
                b = stack.pop()
                a = stack.pop()
                
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ValueError("Division by zero")
                    stack.append(a / b)
        
        if len(stack) != 1:
            raise ValueError("Invalid expression")
        return stack[0]
    
    def evaluate(self) -> float:
        self.tokenize()
        self.infix_to_rpn()
        return self.evaluate_rpn()


def main():
    if len(sys.argv) == 2:
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                expression = f.read().strip()
        except FileNotFoundError:
            print(f"Error: File {sys.argv[1]} not found")
            return
    elif len(sys.argv) == 1:
        print("Enter expression (type 'quit' to exit):")
        expression = input().strip()
        if expression.lower() == 'quit':
            return
    else:
        print("Usage: python calculator.py [filename]")
        return
    
    try:
        parser = ExpressionParser(expression)
        result = parser.evaluate()
        
        print(f"Expression: {expression}")
        print(f"Tokens: {parser.tokens}")
        print(f"RPN: {parser.rpn_tokens}")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()