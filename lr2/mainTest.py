import unittest
import itertools

from main import *


class TestLogicFunctions(unittest.TestCase):
    def test_parse_expression(self):
        self.assertEqual(parse_expression("A ∨ B"), "A  or  B")
        self.assertEqual(parse_expression("A ∧ B"), "A  and  B")
        self.assertEqual(parse_expression("!A"), " not A")
        self.assertEqual(parse_expression("A -> B"), "A  <=  B")
        self.assertEqual(parse_expression("A ~ B"), "A  ==  B")

    def test_generate_truth_table(self):
        variables = ["A", "B"]
        expression = "A ∨ B"
        expected_table = [
            (0, 0, 0),
            (0, 1, 1),
            (1, 0, 1),
            (1, 1, 1)
        ]
        result = generate_truth_table(variables, expression)
        self.assertEqual(result, expected_table)

    def test_build_sdnf_sknf(self):
        table = [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 1)]
        variables = ["A", "B"]
        expected_sdnf = "(¬A ∧ B) ∨ (A ∧ ¬B) ∨ (A ∧ B)"
        expected_sknf = "(A ∨ B)"
        expected_sdnf_nums = (1, 2, 3)
        expected_sknf_nums = (0,)
        result_sdnf, result_sknf, sdnf_nums, sknf_nums = build_sdnf_sknf(table, variables)
        self.assertEqual(result_sdnf, expected_sdnf)
        self.assertEqual(result_sknf, expected_sknf)
        self.assertEqual(sdnf_nums, expected_sdnf_nums)
        self.assertEqual(sknf_nums, expected_sknf_nums)

    def test_compute_index_form(self):
        table = [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 1)]
        expected_index_form = "0111 - 7"
        result = compute_index_form(table)
        self.assertEqual(result, expected_index_form)