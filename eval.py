#!/usr/bin/env python3

import re
import math

class Tokenizer:

   def tokenize(self):
       tokens_value = []
       tokens_enum = []
       file = open("test_input.txt", "r")
       f = open("output.txt", "w+")
       data = file.read().splitlines()
       compile = re.compile(r'[-+=()/^*;.{}]|[+-]?[0-9]*\.?[0-9]+|([a-z]|[A-Z])+[0-9]*')
       token = compile.finditer(str(data))
       for i in token:
           tokens_value.append(i.group(0))
       for i in range(len(tokens_value)):
           token_id = self.match_token(tokens_value[i])
           tokens_enum.append(token_id)
       tokens = []
       for i in range(len(tokens_value)):
           tokens.append((tokens_value[i], tokens_enum[i]))
           f.write(tokens_value[i] + " " + tokens_enum[i] + "\n")
       f.close()
       return tokens

   def match_token(self,token):
       value = 'TT_ERROR'
       if self.is_trig(token):
           if token == 'cos':
               value = 'TT_COS'
           elif token == "sin":
               value = 'TT_SIN'
           else:
               value = 'TT_TAN'
       elif self.is_Identifier(token):
           value = "TT_IDENTIFIER"
       elif self.is_int(token) or self.is_double(token):
           value = 'TT_NUMBER'
       elif self.is_syb(token):
           value = 'TT_SYMBOL'
       return value

   def is_Identifier(self, token):
       is_identifier = True
       for i in range(len(token)):
           if str.isalpha(token[0]):
               if not (self.is_int(token[i]) or str.isalpha(token[i])):
                   is_identifier = False
           else:
               is_identifier = False
       return is_identifier

   def is_int(self, token):
       for digit in token:
           if not int(digit):
               return False
       return True

   def int(self, token):
       if (token == "0" or token == "1" or token == "2" or token == "3" or token == "4" or
               token == "5" or token == "6" or token == "7" or token == "8" or token == "9"):
           return True
       return False

   def is_double(self, token):
       is_double = True
       dots = 0
       if int(token[0]) != True:
           return False
       for digit in token:
           if digit == ".":
               dots += 1
           elif not int(digit):
               is_double = False
           if dots > 1:
               is_double = False
       if is_double:
           return True

   def is_trig(self, token):
       if token == "cos" or token == "sin" or token == "tan":
           return True
       return False

   def is_syb(self, token):
       if (token == '+' or token == '-' or token == '(' or token == ')' or token == '/' or token == '*'
               or token == '.' or token == ';' or token == '=' or token == '^' or token == '{' or token == '}'):
           return True
       return False

import re
import math

#dict[key] = "value"


class Parser:
    def __init__(self, tokens,  environment = {}, result = []):
        self.tokens = tokens
        self.environment = environment
        self.current = tokens[0]
        self.result = result

    def eval(self):
        for i in range(len(self.result)):
            print("line " + str(i + 3) + " output: " + str(self.result[i]))

    def parse(self):
        self.result = self.prog()

    def next(self):
        self.tokens = self.tokens[1:]
        self.current = self.tokens[0] if len(self.tokens) > 0 else None

    def error(self, error):
        print(error)
        exit()

    def prog(self):
        print("\t" + "prog" + "\n")
        if self.current[0] == "prog":
            self.next()
            if self.current[1] == "TT_IDENTIFIER":
                self.next()
        if self.current[0] == '(':
            self.next()
            if self.current[1] == "TT_IDENTIFIER":
                ID = self.current[0]
                self.next()
                if self.current[0] != "=":
                    self.error("expected =")
                self.next()
                if self.current[1] == "TT_IDENTIFIER":
                    self.environment[ID] = self.id[self.id[self.current[0]]]
                    self.next()
                elif self.current[1] == "TT_NUMBER":
                    self.environment[ID] = float(self.current[0])
                    self.next()
                else:
                    self.error("expected number or identifier")
            if self.current[0] != ')':
                self.error("expected )")
            self.next()
        if self.current[0] != '{':
            self.error("expected {")
        self.next()
        result = self.sl()
        if self.current[0] != '}':
            self.error("expected }")
        self.next()
        return result

    def sl(self):
        print("\t\t" + "sl" + "\n")
        result = []
        while self.current is not None and self.current[0] != '}':
            while self.current[0] != ';':
                result.append(self.s())
            self.next()
        return result

    def s(self):
        print("\t\t\t" + "s" + "\n")
        result = None
        if self.current[1] == "TT_IDENTIFIER":
            ID = self.current[0]
            self.next()
            if self.current[0] == '=':
                self.next()
                self.environment[ID] = self.exp()
            else:
                if ID in self.environment:
                    result = self.environment[ID]
                else:
                    self.error("semantic error " + ID + " undefined")
        else:
            result = self.exp()
        return result

    def exp(self):
        print("\t\t\t\t" + "exp" + "\n")
        result = self.term()
        while self.current[0] in ('+', '-'):
            if self.current[0] == '+':
                self.next()
                result += self.term()
            if self.current[0] == '-':
                self.next()
                result -= self.term()
        return result

    def term(self):
        print("\t\t\t\t\t" + "term" + "\n")
        result = self.pow()
        while self.current[0] in ('*', '/'):
            if self.current[0] == '*':
                self.next()
                result *= self.pow()
            if self.current[0] == '/':
                self.next()
                result /= self.pow()
        return result

    def pow(self):
        print("\t\t\t\t\t\t" + "pow" + "\n")
        result = self.fact()
        while self.current[0] == '^':
                self.next()
                result = result ** self.fact()
        return result

    def fact(self):
        print("\t\t\t\t\t\t" + "fact" + "\n")
        result = None
        if self.current[1] == "TT_NUMBER":
            result = float(self.current[0])
            self.next()
        elif self.current[0] == '(':
            self.next()
            result = self.exp()
            if self.current[0] != ')':
                self.error("error expected )")
            self.next()
        elif self.current[1] == "TT_TAN":
            self.next()
            if self.current[0] != '(':
                self.error("error expected (")
            self.next()
            result = math.tan(self.exp())
            if self.current[0] != ')':
                self.error("error expected )")
            self.next()
        elif self.current[1] == "TT_COS":
            self.next()
            if self.current[0] != '(':
                self.error("error expected (")
            self.next()
            result = math.cos(self.exp())
            if self.current[0] != ')':
                self.error("error expected )")
            self.next()
        elif self.current[1] == "TT_SIN":
            self.next()
            if self.current[0] != '(':
                self.error("error expected (")
            self.next()
            result = math.sin(self.exp())
            if self.current[0] != ')':
                self.error("error expected )")
            self.next()
        elif self.current[1] == "TT_IDENTIFIER":
            result = self.environment[self.current[0]]
            self.next()
        else:
            self.error("unknown symbol for fact")
        return result


def is_trig(token):
    if token == "cos" or token == "sin" or token == "tan":
        return True
    return False

def is_int(token):
    for digit in token:
        if not int(digit):
            return False
    return True

def int(token):
        digits = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}
        return token in digits

def main():
    t = Tokenizer()
    p = Parser(t.tokenize())
    p.parse()
    p.eval()


main()
