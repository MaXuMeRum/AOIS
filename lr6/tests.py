import unittest
from main import *
from io import StringIO
from unittest.mock import patch

class TestHashTableEntry(unittest.TestCase):
    def test_entry_initialization(self):
        entry = HashTableEntry("test", "data")
        self.assertEqual(entry.id, "test")
        self.assertEqual(entry.data, "data")
        self.assertEqual(entry.collision, 0)
        self.assertEqual(entry.occupied, 0)
        self.assertEqual(entry.terminal, 0)
        self.assertEqual(entry.link_flag, 0)
        self.assertEqual(entry.deleted, 0)
        self.assertIsNone(entry.overflow_pointer)

    def test_entry_str_representation(self):
        entry = HashTableEntry("key1", "value1")
        expected_str = "ID: key1, Data: value1, C: 0, U: 0, T: 0, L: 0, D: 0, Po: None"
        self.assertEqual(str(entry), expected_str)

class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.capacity = 10
        self.hash_table = HashTable(self.capacity)

    def test_initialization(self):
        self.assertEqual(self.hash_table.capacity, self.capacity)
        self.assertEqual(len(self.hash_table.table), self.capacity)
        self.assertEqual(self.hash_table.size, 0)
        self.assertTrue(all(entry is None for entry in self.hash_table.table))

    def test_calculate_v_english(self):
        self.assertEqual(self.hash_table._calculate_v("AB"), 33 * 0 + 1)
        self.assertEqual(self.hash_table._calculate_v("ab"), 33 * 0 + 1)
        self.assertEqual(self.hash_table._calculate_v("ZA"), 33 * 25 + 0)
        self.assertEqual(self.hash_table._calculate_v("zz"), 33 * 25 + 25)

    def test_calculate_v_russian(self):
        self.assertEqual(self.hash_table._calculate_v("АБ"), 33 * 0 + 1)
        self.assertEqual(self.hash_table._calculate_v("аб"), 33 * 0 + 1)
        self.assertEqual(self.hash_table._calculate_v("ЯА"), 33 * 31 + 0)

    def test_calculate_v_short_key(self):
        self.assertEqual(self.hash_table._calculate_v(""), hash(""))
        self.assertEqual(self.hash_table._calculate_v("a"), hash("a"))

    def test_calculate_v_non_alpha(self):
        self.assertEqual(self.hash_table._calculate_v("123"), hash("123"))
        self.assertEqual(self.hash_table._calculate_v("a1"), hash("a1"))

    def test_hash_functions(self):
        v = 100
        h1 = self.hash_table._hash1(v)
        h2 = self.hash_table._hash2(v)
        self.assertEqual(h1, 100 % self.capacity)
        self.assertEqual(h2, 1 + (100 // self.capacity) % (self.capacity - 1))

    def test_insert_and_get(self):
        self.hash_table.insert("key1", "value1")
        self.assertEqual(self.hash_table.get("key1"), "value1")
        self.assertEqual(self.hash_table.size, 1)
        self.hash_table.insert("key1", "new_value")
        self.assertEqual(self.hash_table.get("key1"), "new_value")
        self.assertEqual(self.hash_table.size, 1)

    def test_insert_collision(self):
        self.hash_table.insert("key1", "value1")
        original_index = self.hash_table._hash1(self.hash_table._calculate_v("key1"))
        found = False
        for c in "abcdefghijklmnopqrstuvwxyz":
            for d in "abcdefghijklmnopqrstuvwxyz":
                test_key = c + d
                if self.hash_table._hash1(self.hash_table._calculate_v(test_key)) == original_index and test_key != "key1":
                    self.hash_table.insert(test_key, "value2")
                    self.assertEqual(self.hash_table.get(test_key), "value2")
                    self.assertEqual(self.hash_table.size, 2)
                    self.assertEqual(self.hash_table.table[self.hash_table._hash1(self.hash_table._calculate_v(test_key))].collision, 0)
                    found = True
                    break
            if found:
                break
        self.assertTrue(found, "Couldn't find a key that causes collision")

    def test_insert_full_table(self):
        for i in range(self.capacity):
            self.hash_table.insert(f"key{i}", f"value{i}")
        with self.assertRaises(OverflowError):
            self.hash_table.insert("extra_key", "extra_value")

    def test_delete(self):
        self.hash_table.insert("key1", "value1")
        self.assertTrue(self.hash_table.delete("key1"))
        self.assertEqual(self.hash_table.size, 0)
        self.assertIsNone(self.hash_table.get("key1"))
        v = self.hash_table._calculate_v("key1")
        h1 = self.hash_table._hash1(v)
        h2 = self.hash_table._hash2(v)
        for i in range(self.capacity):
            index = (h1 + i * h2) % self.capacity
            if self.hash_table.table[index] is not None and self.hash_table.table[index].id == "key1":
                self.assertEqual(self.hash_table.table[index].deleted, 1)
                break

    def test_delete_nonexistent(self):
        self.assertFalse(self.hash_table.delete("nonexistent_key"))

    def test_len(self):
        self.assertEqual(len(self.hash_table), 0)
        self.hash_table.insert("key1", "value1")
        self.assertEqual(len(self.hash_table), 1)
        self.hash_table.delete("key1")
        self.assertEqual(len(self.hash_table), 0)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_table(self, mock_stdout):
        self.hash_table.insert("key1", "value1")
        self.hash_table.display_table()
        output = mock_stdout.getvalue()
        self.assertIn("Содержимое хеш-таблицы", output)
        self.assertIn("key1", output)
        self.assertIn("value1", output)
        self.assertIn("Размер хеш-таблицы: 1", output)

    def test_unicode_keys(self):
        self.hash_table.insert("ключ", "значение")
        self.assertEqual(self.hash_table.get("ключ"), "значение")
        self.hash_table.insert("😊", "emoji")
        self.assertEqual(self.hash_table.get("😊"), "emoji")

if __name__ == '__main__':
    unittest.main()