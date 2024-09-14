"""
论文查重程序（用终端命令行输入参数实现）
"""
import sys
import re
import os


def calculate_similarity(ori_file, cop_file):
    """
    计算两个文件的相似度。

    :param ori_file: 原文文件路径
    :param cop_file: 抄袭版文件路径
    :return: 重复率，若发生错误则返回 None
    """
    try:
        with open(ori_file, 'r', encoding='utf-8')as f1, open(cop_file, 'r', encoding='utf-8')as f2:
            ori_text = f1.read()
            cop_text = f2.read()
    except IOError as e:
        print(f"Error opening files: {e}")
        return None

    # 去除标点符号、空格和空行，转换为小写
    ori_words = re.findall(r'\w+', ori_text.lower().replace(' ', '').replace('\n', ''))
    cop_words = re.findall(r'\w+', cop_text.lower().replace(' ', '').replace('\n', ''))

    # 计算重复词的数量
    common_words = set(ori_words) & set(cop_words)
    num_common_words = len(common_words)
    # 计算文本重复率
    return num_common_words / len(ori_words) if len(ori_words) > 0 else 0


def split_arguments():
    """提取命令行参数中的文件路径"""
    if len(sys.argv) != 4:
        print("Usage: python main.py [original_file] [copied_file] [answer_file]")
        sys.exit(1)

    original_file = sys.argv[1]
    copied_file = sys.argv[2]
    answer_file = sys.argv[3]

    return original_file, copied_file, answer_file


def write_to_file(answer_file, message):
    """将消息写入指定文件"""
    try:
        if os.path.exists(answer_file):
            with open(answer_file, 'w', encoding='utf-8') as f:
                f.write(message)
        else:
            with open(answer_file, 'x', encoding='utf-8') as f:
                f.write(message)
    except IOError as e:
        print(f"Error writing to file: {e}")


def main():
    """主函数，执行论文查重流程"""
    original_file, copied_file, answer_file = split_arguments()

    similarity = calculate_similarity(original_file, copied_file)

    if similarity is not None:
        # 构建要写入文件的消息
        message = f"【{copied_file}】与【{original_file}】的重复率为{similarity:.2f}"

        # 将消息写入指定文件
        write_to_file(answer_file, message)
        print(f"结果已写入文件: {answer_file}")
    else:
        print("计算重复率时发生错误！")


if __name__ == '__main__':
    main()
