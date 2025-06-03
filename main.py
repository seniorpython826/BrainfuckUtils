from brainfuck import BrainfuckGenerator, BrainfuckInterpreter

# Создаем генератор с 5 ячейками памяти
generator = BrainfuckGenerator(memory_size=5)

# Генерируем Brainfuck код
bf_code = generator.generate("Hello World!")
print(f"Сгенерированный код:\n{bf_code}\n")

# Исполняем сгенерированный код
interpreter = BrainfuckInterpreter()
interpreter.execute(bf_code)

print()

# Простая генерация (одна ячейка)
simple_code = BrainfuckGenerator.simple_generate("Python")
print(f"\nПростой код:\n{simple_code}\n")

# Исполняем сгенерированный код
interpreter = BrainfuckInterpreter()
interpreter.execute(simple_code)
