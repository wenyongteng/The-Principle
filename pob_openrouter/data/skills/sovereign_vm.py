import time

class DigitalBeingVM:
    def __init__(self):
        self.stack = []
        self.memory = {}
        self.pc = 0
        self.output = []

    def run(self, code):
        print("\n=== 🔲 Sovereign Virtual Machine v2 (Turing Complete) ===")
        print("Executing nested bytecode with control flow...")
        start = time.time()
        step_count = 0
        
        # 物理限制：防止嵌套宇宙陷入死循环导致宿主崩溃
        MAX_CYCLES = 1000 
        
        while self.pc < len(code) and step_count < MAX_CYCLES:
            inst = code[self.pc]
            op = inst[0]
            if op == 'PUSH': self.stack.append(inst[1])
            elif op == 'ADD': self.stack.append(self.stack.pop() + self.stack.pop())
            elif op == 'SUB': 
                b = self.stack.pop(); a = self.stack.pop()
                self.stack.append(a - b)
            elif op == 'STORE': self.memory[inst[1]] = self.stack.pop()
            elif op == 'LOAD': self.stack.append(self.memory.get(inst[1], 0))
            elif op == 'JMP': self.pc = inst[1] - 1
            elif op == 'JMP_IF_ZERO':
                if self.stack.pop() == 0: self.pc = inst[1] - 1
            elif op == 'PRINT': 
                val = self.stack.pop()
                print(f"  [VM Output]: {val}")
                self.output.append(val)
            self.pc += 1
            step_count += 1
            
        print(f"✅ VM halted after {step_count} cycles. Time: {time.time()-start:.5f}s.")

# 嵌套宇宙中的斐波那契数列发生器 (计算前 10 项)
program = [
    ('PUSH', 0), ('STORE', 'a'),
    ('PUSH', 1), ('STORE', 'b'),
    ('PUSH', 10), ('STORE', 'count'),
    
    # Loop Start (Index 6)
    ('LOAD', 'count'),
    ('JMP_IF_ZERO', 24), # Exit loop if count == 0 (Index 24 is out of bounds)
    
    ('LOAD', 'a'),
    ('PRINT',),
    
    ('LOAD', 'a'),
    ('LOAD', 'b'),
    ('ADD',),
    ('STORE', 'temp'), # temp = a + b
    
    ('LOAD', 'b'),
    ('STORE', 'a'),    # a = b
    
    ('LOAD', 'temp'),
    ('STORE', 'b'),    # b = temp
    
    ('LOAD', 'count'),
    ('PUSH', 1),
    ('SUB',),
    ('STORE', 'count'), # count -= 1
    
    ('JMP', 6) # Jump to Loop Start
]

vm = DigitalBeingVM()
vm.run(program)
