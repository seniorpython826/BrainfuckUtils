from __future__ import annotations
import sys
from typing import Optional, Dict, TextIO, Union
from enum import IntEnum



class EOFBehavior(IntEnum):
    """Поведение при достижении конца ввода (совместимо с Python 3.13+)"""
    LEAVE_UNCHANGED = 0
    SET_TO_ZERO = -1
    SET_TO_MINUS_ONE = -2  # Пример дополнительного значения

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """Кастомный генератор значений для совместимости с Python 3.13+"""
        if not last_values:
            return start
        return last_values[-1] - 1  # Генерируем последовательные отрицательные числа


class ExecutionState:
    """Состояние выполнения программы"""
    __slots__ = ('memory', 'pointer', 'program_counter', 'steps')

    def __init__(
            self,
            memory: bytearray,
            pointer: int,
            program_counter: int,
            steps: int
    ):
        self.memory = memory
        self.pointer = pointer
        self.program_counter = program_counter
        self.steps = steps


class BrainfuckInterpreter:
    """интерпретатор Brainfuck с полной совместимостью"""

    __slots__ = (
        '_memory_size', '_eof_behavior', '_max_steps',
        '_input', '_output', '_bracket_map'
    )

    def __init__(
            self,
            memory_size: int = 30000,
            eof_behavior: Union[EOFBehavior, int] = EOFBehavior.LEAVE_UNCHANGED,
            max_steps: Optional[int] = 1_000_000,
            input_stream: Optional[TextIO] = None,
            output_stream: Optional[TextIO] = None,
    ):
        """
        Инициализация интерпретатора.

        Args:
            memory_size: Размер памяти в ячейках (по умолчанию 30000)
            eof_behavior: Поведение при EOF (0 - оставить значение, -1 - установить 0)
            max_steps: Максимальное количество шагов выполнения
            input_stream: Поток ввода (по умолчанию sys.stdin)
            output_stream: Поток вывода (по умолчанию sys.stdout)
        """
        self._memory_size = memory_size
        self._eof_behavior = eof_behavior if isinstance(eof_behavior, EOFBehavior) else EOFBehavior(eof_behavior)
        self._max_steps = max_steps
        self._input = input_stream if input_stream is not None else sys.stdin
        self._output = output_stream if output_stream is not None else sys.stdout
        self._bracket_map: Dict[int, int] = {}

    def reset(self) -> None:
        """Сброс состояния интерпретатора"""
        self._bracket_map.clear()

    def _validate_program(self, program: str) -> None:
        """Валидация программы (проверка баланса скобок)"""
        stack = []
        for pos, cmd in enumerate(program):
            if cmd == '[':
                stack.append(pos)
            elif cmd == ']':
                if not stack:
                    raise SyntaxError(f"Unmatched ']' at position {pos}")
                start = stack.pop()
                self._bracket_map[start] = pos
                self._bracket_map[pos] = start

        if stack:
            raise SyntaxError(f"Unmatched '[' at positions: {stack}")

    @staticmethod
    def _clean_program(program: str) -> str:
        """Очистка программы от незначимых символов"""
        return ''.join(c for c in program if c in '><+-.,[]')

    def _handle_io(self, cmd: str, memory: bytearray, pointer: int) -> None:
        """Обработка операций ввода/вывода"""
        if cmd == '.':
            self._output.write(chr(memory[pointer]))
            self._output.flush()
        elif cmd == ',':
            char = self._input.read(1)
            if not char:  # EOF
                if self._eof_behavior == EOFBehavior.LEAVE_UNCHANGED:
                    return
                memory[pointer] = abs(self._eof_behavior.value)  # Используем значение из Enum

    def execute(
            self,
            program: str,
            *,
            initial_memory: Optional[bytes] = None,
            initial_pointer: int = 0
    ) -> ExecutionState:
        """
        Выполнение Brainfuck программы.

        Args:
            program: Программа на Brainfuck
            initial_memory: Начальное состояние памяти
            initial_pointer: Начальная позиция указателя

        Returns:
            Состояние выполнения после завершения программы
        """
        self.reset()
        cleaned = self._clean_program(program)
        self._validate_program(cleaned)

        memory = bytearray(initial_memory if initial_memory is not None else self._memory_size)
        memory.extend(b'\0' * (self._memory_size - len(memory)))

        state = ExecutionState(
            memory=memory,
            pointer=initial_pointer,
            program_counter=0,
            steps=0
        )

        program_len = len(cleaned)
        memory_len = len(memory)

        while state.program_counter < program_len:
            cmd = cleaned[state.program_counter]

            if cmd == '>':
                state.pointer = (state.pointer + 1) % memory_len
            elif cmd == '<':
                state.pointer = (state.pointer - 1) % memory_len
            elif cmd == '+':
                state.memory[state.pointer] = (state.memory[state.pointer] + 1) % 256
            elif cmd == '-':
                state.memory[state.pointer] = (state.memory[state.pointer] - 1) % 256
            elif cmd in '.,':
                self._handle_io(cmd, state.memory, state.pointer)
            elif cmd == '[' and not state.memory[state.pointer]:
                state.program_counter = self._bracket_map[state.program_counter]
            elif cmd == ']' and state.memory[state.pointer]:
                state.program_counter = self._bracket_map[state.program_counter]

            state.program_counter += 1
            state.steps += 1

            if self._max_steps and state.steps >= self._max_steps:
                raise RuntimeError(f"Max steps limit reached ({self._max_steps})")

        return state
