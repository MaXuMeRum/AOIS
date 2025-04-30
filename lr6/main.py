class HashTableEntry:
    def __init__(self, key, data=None):
        self.id = key
        self.data = data
        self.collision = 0
        self.occupied = 0
        self.terminal = 0
        self.link_flag = 0
        self.deleted = 0
        self.overflow_pointer = None

    def __str__(self):
        return (f"ID: {self.id}, Data: {self.data}, C: {self.collision}, U: {self.occupied}, "
                f"T: {self.terminal}, L: {self.link_flag}, D: {self.deleted}, Po: {self.overflow_pointer}")

class HashTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.table = [None] * capacity
        self.size = 0

    def _calculate_v(self, key):
        if len(key) < 2 or not key[:2].isalpha():
            return hash(key)

        v = (ord(key[0].upper()) - ord('А') if 'А' <= key[0].upper() <= 'Я' else ord(key[0].upper()) - ord('A')) * 33 + \
            (ord(key[1].upper()) - ord('А') if 'А' <= key[1].upper() <= 'Я' else ord(key[1].upper()) - ord('A'))
        return v

    def _hash1(self, v):
        return v % self.capacity

    def _hash2(self, v):
        return 1 + (v // self.capacity) % (self.capacity - 1)

    def insert(self, key, data):
        if self.size == self.capacity:
            raise OverflowError("Хеш-таблица заполнена")

        v = self._calculate_v(key)
        h1 = self._hash1(v)
        h2 = self._hash2(v)

        for i in range(self.capacity):
            index = (h1 + i * h2) % self.capacity
            if self.table[index] is None or self.table[index].deleted == 1:
                self.table[index] = HashTableEntry(key, data)
                self.table[index].occupied = 1
                self.size += 1
                if i > 0:
                    self.table[index].collision = 1
                return
            elif self.table[index].id == key and self.table[index].deleted == 0:
                print(f"Ключ '{key}' уже существует в таблице. Обновление данных.")
                self.table[index].data = data
                return

        raise RuntimeError("Не удалось найти свободное место для вставки")

    def get(self, key):
        v = self._calculate_v(key)
        h1 = self._hash1(v)
        h2 = self._hash2(v)

        for i in range(self.capacity):
            index = (h1 + i * h2) % self.capacity
            if self.table[index] is None:
                return None
            elif self.table[index].id == key and self.table[index].deleted == 0:
                return self.table[index].data
        return None

    def delete(self, key):
        v = self._calculate_v(key)
        h1 = self._hash1(v)
        h2 = self._hash2(v)

        for i in range(self.capacity):
            index = (h1 + i * h2) % self.capacity
            if self.table[index] is None:
                return False
            elif self.table[index].id == key and self.table[index].deleted == 0:
                self.table[index].deleted = 1
                self.table[index].occupied = 0
                self.size -= 1
                return True
        return False

    def __len__(self):
        return self.size

    def load_factor(self):
        return self.size / self.capacity

    def display_table(self):
        print("\nСодержимое хеш-таблицы:")
        print("---------------------------------------------------------------------------------------------------")
        print("Индекс | ID             | V    | h1   | h2   | Data        | C | U | T | L | D | Po  |")
        print("---------------------------------------------------------------------------------------------------")
        for i, entry in enumerate(self.table):
            v_value = str(self._calculate_v(entry.id)) if entry and entry.id else "None"
            h1_value = str(self._hash1(self._calculate_v(entry.id))) if entry and entry.id else "None"
            h2_value = str(self._hash2(self._calculate_v(entry.id))) if entry and entry.id else "None"
            po_value = str(entry.overflow_pointer) if entry else "None"
            deleted_value = str(entry.deleted) if entry else "None"
            collision_value = str(entry.collision) if entry else "None"
            occupied_value = str(entry.occupied) if entry else "None"
            terminal_value = str(entry.terminal) if entry else "None"
            link_flag_value = str(entry.link_flag) if entry else "None"
            id_value = entry.id if entry else ""
            data_value = entry.data if entry else ""

            print(f"{i:<6} | {id_value:<14} | {v_value:<4} | {h1_value:<4} | {h2_value:<4} | {data_value:<11} | "
                  f"{collision_value:<1} | {occupied_value:<1} | {terminal_value:<1} | {link_flag_value:<1} | "
                  f"{deleted_value:<1} | {po_value:<3} |")
        print("---------------------------------------------------------------------------------------------------")
        print(f"Размер хеш-таблицы: {len(self)}")
        print(f"Коэффициент заполнения: {self.load_factor():.2f}")