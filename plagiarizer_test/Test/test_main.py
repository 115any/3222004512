"""
Created on Sep 21, 2021
"""
import unittest
import sys
from main import calculate_similarity, split_arguments, write_to_file

class TestFunctions(unittest.TestCase):
    """
    测试用例类，用于对论文查重程序中的各个函数进行单元测试。
    """

    def setUp(self):
        """
        测试用例初始化方法，在每个测试方法执行前都会被调用。
        设置测试所需的文件路径。
        """
        self.original_file_path = r'C:\Users\YANGY\Desktop\testbar\orig.txt'
        self.copied_file_paths = [
            r'C:\Users\YANGY\Desktop\testbar\orig_0.8_add.txt',
            r'C:\Users\YANGY\Desktop\testbar\orig_0.8_del.txt',
            r'C:\Users\YANGY\Desktop\testbar\orig_0.8_dis_1.txt',
            r'C:\Users\YANGY\Desktop\testbar\orig_0.8_dis_10.txt',
            r'C:\Users\YANGY\Desktop\testbar\orig_0.8_dis_15.txt'
        ]
        self.answer_file_path = r'C:\Users\YANGY\Desktop\testbar\answer.txt'

    def test_calculate_similarity(self):
        """
        测试 calculate_similarity 函数，确保计算结果不为 None。
        """
        for copied_file_path in self.copied_file_paths:
            similarity = calculate_similarity(self.original_file_path, copied_file_path)
            self.assertIsNotNone(similarity)

    def test_split_arguments(self):
        """
        测试 split_arguments 函数，确保提取的文件路径正确。
        """
        sys.argv = [
            'script_name', 
            self.original_file_path, self.copied_file_paths[0], self.answer_file_path
        ]
        original_file, copied_file, answer_file = split_arguments()
        self.assertEqual(original_file, self.original_file_path)
        self.assertEqual(copied_file, self.copied_file_paths[0])
        self.assertEqual(answer_file, self.answer_file_path)

    def test_write_to_file(self):
        """
        测试 write_to_file 函数，确保能正确写入文件并读取验证内容。
        """
        test_message = "Test message"
        write_to_file(self.answer_file_path, test_message)
        with open(self.answer_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertEqual(content, test_message)

if __name__ == '__main__':
    unittest.main()
