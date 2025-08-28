import re
import sys
import os

def extract_and_inject_mcdc_variants(source_code):
    output_code = ""
    pattern = re.compile(r'(if\s*\(([^)]*&&[^)]*)\))')  # 匹配含 && 的 if 条件

    lines = source_code.splitlines()
    for line in lines:
        match = pattern.search(line)
        if match:
            full_if = match.group(1)
            condition = match.group(2)
            indent = re.match(r'^(\s*)', line).group(1)  # 保留原始缩进

            # 拆分子表达式
            expressions = [expr.strip() for expr in condition.split('&&')]

            output_code += line + "\n"  # 原始 if 保留

            # 插入每一个 MCDC 变异语句
            for i in range(len(expressions)):
                mutated = []
                for j, expr in enumerate(expressions):
                    if i == j:
                        mutated.append(f"!({expr})")
                    else:
                        mutated.append(expr)
                new_condition = " && ".join(mutated)
                mutated_if = f"{indent}if ({new_condition}) {{ /* MCDC mutant {i+1} */ }}"
                output_code += mutated_if + "\n"

        else:
            output_code += line + "\n"
    
    return output_code


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("example: python Add_MCDC.py input.c [output.c]")
        sys.exit(1)

    input_path = sys.argv[1]

    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        # 自动生成默认输出文件名
        base, ext = os.path.splitext(input_path)
        output_path = base + "_MCDC" + ext

    # 读取源代码
    with open(input_path, "r") as f:
        source_code = f.read()

    # 处理并生成新代码
    mutated_code = extract_and_inject_mcdc_variants(source_code)

    # 写入输出文件
    with open(output_path, "w") as f:
        f.write(mutated_code)

    print(f" MC/DC mutation inject successful：{output_path}")
