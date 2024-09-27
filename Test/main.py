import random
import argparse
import os
from fractions import Fraction

# 将分数格式化为指定格式
def format_fraction(fraction):
    if fraction.numerator == 0:
        return '0'
    elif fraction.denominator == 1:
        return str(fraction.numerator)
    else:
        # 约分
        gcd = fraction.numerator.gcd(fraction.denominator)
        simplified_numerator = fraction.numerator // gcd
        simplified_denominator = fraction.denominator // gcd
        return f'{simplified_numerator}/{simplified_denominator}'

# 判断是否为整数
def is_integer(num_str):
    try:
        int(num_str)
        return True
    except ValueError:
        return False

# 生成一个真分数，分子随机在 1 到 9 之间，分母随机在 2 到 9 之间
def generate_fraction():
    numerator = random.randint(1, 9)
    denominator = random.randint(2, 9)
    return f'{numerator}/{denominator}'

# 生成一个数字，随机决定是生成一个自然数还是真分数
def generate_number(range_num):
    choice = random.randint(0, 1)
    if choice:
        return generate_fraction()
    else:
        return str(random.randint(0, range_num - 1))

# 递归地生成表达式，随机选择运算符和数字，最多有三个运算符
def generate_expression(range_num):
    operators = ['+', '-', '*', '/']
    expr = generate_number(range_num)
    operator_count = random.randint(1, 3)
    for _ in range(operator_count):
        op = random.choice(operators)
        if op == '/' and random.random() < 0.5:
            expr = f'({expr}) {op} ({generate_number(range_num)})'
        else:
            expr = f'{expr} {op} {generate_number(range_num)}'
    return expr

# 生成一个四则运算题目，即一个表达式加上等号
def generate_question(range_num):
    expr = generate_expression(range_num)
    return f'{expr} ='

# 计算表达式的值，将带分数转换为加法形式后用 eval 函数求值
def evaluate_expression(expr):
    expr = expr.replace("'", '+')
    try:
        parts = expr.split(' ')
        new_expr = ''
        for part in parts:
            if '/' in part:
                fraction = Fraction(part)
                new_expr += f'{fraction} '
            else:
                new_expr += f'{part} '
        result = eval(new_expr)
        return format_fraction(Fraction(result))
    except:
        return "Error"

# 生成指定数量的问题和答案，并保存到文件
def generate_and_save_questions(num_questions, range_num, exercise_filename, answer_filename):
    questions = []
    answers = []
    while len(questions) < num_questions:
        question = generate_question(range_num)
        answer = evaluate_expression(question[:-1])
        if answer != "Error" and all(question not in q for q in questions):
            questions.append(question)
            answers.append(answer)
    with open(exercise_filename, 'w') as ef:
        for item in questions:
            ef.write(item + '\n')
    with open(answer_filename, 'w') as af:
        for item in answers:
            af.write(item + '\n')

# 检查答案的正确性并统计正确和错误的数量，输出到 Grade.txt 文件
# answers_file可以是用户自己编辑的答案文件，但是要先保存在该py文件的目录下
def check_answers(exercise_file, answer_file):
    correct_count = 0
    wrong_count = 0
    correct_indices = []
    wrong_indices = []
    answer_f = open(answer_file, 'r')
    with open(exercise_file, 'r') as ef:
        exercises = ef.readlines()
        for i, exercise in enumerate(exercises, start=1):
            exercise_expr = exercise[:-1].split('=')[0]
            calculated_answer = evaluate_expression(exercise_expr)
            answer_line = answer_f.readline().strip()
            # 将答案转换为统一格式进行比较
            try:
                if calculated_answer != "Error":
                    formatted_calculated_answer = Fraction(calculated_answer)
                else:
                    formatted_calculated_answer = calculated_answer
                if answer_line != "Error":
                    formatted_answer_line = Fraction(answer_line)
                else:
                    formatted_answer_line = answer_line
                if formatted_calculated_answer == formatted_answer_line:
                    correct_count += 1
                    correct_indices.append(i)
                else:
                    wrong_count += 1
                    wrong_indices.append(i)
            except ValueError:
                wrong_count += 1
                wrong_indices.append(i)
    answer_f.close()
    with open('Grade.txt', 'w') as gf:
        gf.write(f'Correct: {correct_count} ({", ".join(map(str, correct_indices))})\n')
        gf.write(f'Wrong: {wrong_count} ({", ".join(map(str, wrong_indices))})\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate arithmetic exercises.')
    parser.add_argument('-n', type=int, help='Number of questions to generate.')
    parser.add_argument('-r', type=int, required=False, help='Range for numbers and fractions.')
    parser.add_argument('-e', type=str, help='Exercise file for checking answers.')
    parser.add_argument('-a', type=str, help='Answer file for checking answers.')
    args = parser.parse_args()

    if args.n:
        generate_and_save_questions(args.n, args.r, os.path.join(os.getcwd(), 'Exercises.txt'), os.path.join(os.getcwd(), 'Answers.txt'))
    elif args.e and args.a:
        check_answers(args.e, args.a)
    else:
        print("Invalid arguments. Use -h for help.")