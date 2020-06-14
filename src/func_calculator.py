class function:
    def __init__(self, func, type):
        self.func = func
        self.type = type

    def __add__(self, b):
        def f(arg):
            t = self.func(arg) if self.type == 1 else self.func
            t += b.func(arg) if b.type == 1 else b.func
            return t
        return function(f, self.type or b.type)

    def __sub__(self, b):
        def f(arg):
            t = self.func(arg) if self.type == 1 else self.func
            t -= b.func(arg) if b.type == 1 else b.func
            return t
        return function(f, self.type or b.type)

    def __mul__(self, b):
        def f(arg):
            t = self.func(arg) if self.type == 1 else self.func
            t *= b.func(arg) if b.type == 1 else b.func
            return t
        return function(f, self.type or b.type)

    def __truediv__(self, b):
        def f(arg):
            t = self.func(arg) if self.type == 1 else self.func
            t /= b.func(arg) if b.type == 1 else b.func
            return t
        return function(f, self.type or b.type)


class func_calculator:
    def __init__(self, text, func_para_dic, func_dict):
        self.text = text
        self.func_para_dic = func_para_dic
        self.func_dict = func_dict
        self.func = self.expression()

    def expression(self):
        ans = self.term()
        while self.text != '':
            op = self.text[0]
            self.text = self.text[1:]
            if op == '+':
                ans += self.term()
            elif op == '-':
                ans -= self.term()
            else:
                return ans
        return ans

    def term(self):
        ans = self.factor()
        while self.text != '':
            op = self.text[0]
            if op == '*':
                self.text = self.text[1:]
                ans = ans*self.factor()
            elif op == '/':
                self.text = self.text[1:]
                ans = ans/self.factor()
            else:
                return ans
        return ans

    def factor(self):
        if self.text[0] == '(':
            self.text = self.text[1:]
            return self.expression()
        elif self.text[0] in '0123456789':
            ans = int(self.text[0])
            self.text = self.text[1:]
            while self.text != '' and self.text[0] in '0123456789':
                ans = ans*10+int(self.text[0])
                self.text = self.text[1:]
            return function(ans, 0)
        else:
            ans = ''
            while self.text != '' and self.text[0] not in '+-*/() ':
                ans += self.text[0]
                self.text = self.text[1:]

            def f(p):
                ohlcv, para_list = p[:5], p[5:]
                para = []
                for i in self.func_para_dic[ans][0]:
                    para.append(ohlcv[i])
                rg = self.func_para_dic[ans][1]
                para.extend(para_list[rg[0]:rg[1]])
                return self.func_dict[ans][0](*para)
            return function(f, 1)

    def result(self):
        def f(l):
            return self.func.func(l).gt(0)
        return f
