def remove_lines_with_keywords(file_path, keywords, output_file=None):
    """
    删除文件中包含指定关键字的行。
    
    :param file_path: 输入文件路径
    :param keywords: 需要匹配的关键字列表
    :param output_file: 输出文件路径。如果为 None，则覆盖原文件。
    """
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 保留不包含关键字的行
        filtered_lines = [
            line for line in lines if not any(keyword in line for keyword in keywords)
        ]

        # 去重并保持行的顺序
        unique_lines = list(dict.fromkeys(filtered_lines))
        # 如果未提供输出文件路径，则覆盖原文件
        if output_file is None:
            output_file = file_path

        # 写入过滤后的内容
        with open(output_file, 'w', encoding='utf-8') as file:
            file.writelines(unique_lines)

        print(f"已处理文件：{file_path}")
        print(f"过滤后的内容已保存到：{output_file}")

    except Exception as e:
        print(f"处理文件时发生错误：{e}")


# 示例用法
if __name__ == "__main__":
    # 输入文件路径
    input_path = "include/CustomOperator.def"  # 替换为你的文件路径

    # 需要匹配的关键字
    keywords_to_remove = ["Void", "SizePtr", "NeedMerge", "lm_", "lse", 
                          "setvl_etvl", "setvlmax_etvlmax", "reinterpret_eint", 
                          "lmul_ext_v_mul_ext", "lmul_trunc_v_mul_trunc", "undefined_undef",
                          "get_get", "create_create", "mv_x_v", "compress_vv", "slide1down", "slide1up",
                          "slidedown", "rgather", "TailUndisturbed", "MaskUndisturbed", "merge_vvm", 
                          "mv_v_v", "mv_v_x", "mclr_m", "mset_m", "fwnmacc"]

    # 输出文件路径（如果为 None，将覆盖原文件）
    output_path = None  # 替换为新文件路径，或保留为 None 覆盖原文件

    remove_lines_with_keywords(input_path, keywords_to_remove, output_path)
