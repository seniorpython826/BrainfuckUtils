# Brainfuck Interpreter and Generator

Полнофункциональный интерпретатор и генератор кода Brainfuck на Python с расширенными возможностями.

## Особенности

- 🚀 Высокопроизводительный интерпретатор Brainfuck
- 🔄 Генератор эффективного Brainfuck-кода из текста
- ⚙️ Гибкая настройка параметров выполнения
- 🔍 Поддержка различных стратегий обработки EOF

## Установка

```bash
git clone https://github.com/seniorpython826/BrainfuckUtils.git
cd BrainfuckUtils
```

## Использование интерпретатора

```

from brainfuck import BrainfuckInterpreter, EOFBehavior

# Создание интерпретатора
interpreter = BrainfuckInterpreter(
    memory_size=30000,
    eof_behavior=EOFBehavior.SET_TO_ZERO,
    max_steps=1_000_000
)

# Пример программы (выводит "Hello World!")
program = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."

# Выполнение программы
result = interpreter.execute(program)
print(f"Выполнено за {result.steps} шагов")

```

## Параметры интерпретатора
| Параметр | По умолчанию | Описание |
|----------|-------------|----------|
| memory_size | 30000    | Размер памяти в ячейках |
| eof_behavior | EOFBehavior.LEAVE_UNCHANGED    | Поведение при EOF |
| max_steps | 1_000_000    | Максимальное количество шагов выполнения |
| input_stream | sys.stdin | Поток ввода |
| output_stream | sys.stdout | Поток вывода |


## Использование генератора кода

```

from brainfuck import BrainfuckGenerator

# Создание генератора с 10 ячейками памяти
generator = BrainfuckGenerator(memory_size=10)

# Генерация кода для строки
bf_code = generator.generate("Hello!")
print(bf_code)  # Выведет Brainfuck-код

```
