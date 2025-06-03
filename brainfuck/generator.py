from typing import List


class BrainfuckGenerator:
    """Класс для преобразования текста в код Brainfuck"""

    __slots__ = ('_memory_size', '_pointer')

    def __init__(self, memory_size: int = 10):
        """
        Инициализация генератора.

        Аргументы:
            memory_size: Количество используемых ячеек памяти (по умолчанию 10)
        """
        self._memory_size = memory_size
        self._pointer = 0  # Текущая позиция указателя в памяти

    def reset(self) -> None:
        """Сброс состояния генератора (обнуление указателя)"""
        self._pointer = 0

    def generate(self, text: str) -> str:
        """
        Генерирует код Brainfuck для вывода заданного текста.

        Аргументы:
            text: Текст для преобразования

        Возвращает:
            Строку с кодом Brainfuck
        """
        bf_code = []
        memory = [0] * self._memory_size  # Инициализируем память нулями

        for char in text:
            target = ord(char)  # Получаем ASCII-код символа

            # Ищем ячейку, которая потребует минимального количества команд
            best_cell = 0
            min_commands = float('inf')  # Начинаем с бесконечности

            for cell in range(self._memory_size):
                # Вычисляем количество команд для перемещения
                move = abs(cell - self._pointer)
                # Вычисляем количество команд для изменения значения
                value_diff = abs(target - memory[cell])
                # Общее количество команд = перемещение + изменение + 1 (для вывода)
                total_commands = move + value_diff

                if total_commands < min_commands:
                    min_commands = total_commands
                    best_cell = cell

            # Генерируем команды для выбранной ячейки
            self._add_move_commands(bf_code, best_cell)
            self._add_value_commands(bf_code, memory[best_cell], target)

            bf_code.append('.')  # Команда вывода
            memory[best_cell] = target  # Обновляем значение в памяти
            self._pointer = best_cell  # Перемещаем указатель

        return ''.join(bf_code)

    def _find_best_cell(self, memory: List[int], target: int) -> tuple[int, int]:
        """Находит ячейку с минимальной разницей для целевого значения"""
        best_cell = 0
        best_diff = abs(target - memory[0])

        for i in range(1, self._memory_size):
            diff = abs(target - memory[i])
            if diff < best_diff:
                best_diff = diff
                best_cell = i

        return best_cell, best_diff

    def _add_move_commands(self, bf_code: List[str], target_cell: int) -> None:
        """Добавляет команды перемещения указателя"""
        move = target_cell - self._pointer
        if move > 0:
            bf_code.append('>' * move)  # Перемещаемся вправо
        elif move < 0:
            bf_code.append('<' * -move)  # Перемещаемся влево

    @staticmethod
    def _add_value_commands(bf_code: List[str], current: int, target: int) -> None:
        """Добавляет команды изменения значения ячейки"""
        delta = target - current
        if delta > 0:
            bf_code.append('+' * delta)  # Увеличиваем значение
        elif delta < 0:
            bf_code.append('-' * -delta)  # Уменьшаем значение

    @staticmethod
    def simple_generate(text: str, start_cell: int = 0) -> str:
        """
        Статический метод для простой генерации кода (использует одну ячейку)

        Аргументы:
            text: Текст для преобразования
            start_cell: Начальная ячейка

        Возвращает:
            Код Brainfuck
        """
        bf_code = []
        current_value = 0
        pointer = 0

        for char in text:
            target = ord(char)
            delta = target - current_value

            # Перемещение если нужно
            if pointer != start_cell:
                move = start_cell - pointer
                bf_code.append('>' * move if move > 0 else '<' * -move)
                pointer = start_cell

            # Изменение значения
            if delta != 0:
                bf_code.append('+' * delta if delta > 0 else '-' * -delta)

            bf_code.append('.')  # Команда вывода
            current_value = target

        return ''.join(bf_code)
