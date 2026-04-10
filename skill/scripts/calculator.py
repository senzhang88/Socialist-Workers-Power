#!/usr/bin/env python3
"""
上海劳动仲裁赔偿计算器 v1.0
专为上海地区劳动者设计

功能：
- 计算经济补偿金（N）
- 计算违法解除赔偿金（2N）
- 计算加班费
- 计算未休年假补偿
- 自动处理上海三倍封顶（37,302元）

使用方式：
  交互式：python calculator.py
  命令行：python calculator.py --start 2020-03-15 --end 2025-03-15 --salary 25000 --illegal
"""

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import sys

# 上海2024-2025年度标准
SHANGHAI_AVG_SALARY = 12434  # 月平均工资（元）
SHANGHAI_TRIPLE_CAP = 37302  # 三倍封顶（元）


def get_float_input(prompt, default=None):
    """获取数字输入"""
    while True:
        try:
            value = input(prompt)
            if value.strip() == "" and default is not None:
                return default
            return float(value)
        except ValueError:
            print("请输入有效的数字！")


def get_date_input(prompt):
    """获取日期输入"""
    while True:
        try:
            date_str = input(prompt)
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("日期格式错误！请使用 YYYY-MM-DD 格式，例如：2020-03-15")


def get_yes_no_input(prompt):
    """获取是/否输入"""
    while True:
        value = input(prompt).lower().strip()
        if value in ["y", "yes", "是"]:
            return True
        elif value in ["n", "no", "否"]:
            return False
        else:
            print("请输入 y 或 n")


def calculate_work_years(start_date, end_date):
    """计算工作年限"""
    delta = relativedelta(end_date, start_date)
    years = delta.years
    months = delta.months
    days = delta.days

    # 六个月以上按1年算，不满六个月按0.5年算（《劳动合同法》第47条）
    if months >= 6:
        years += 1
    elif months > 0 or days > 0:
        years += 0.5

    return years


def calculate_n(monthly_salary, work_years):
    """计算经济补偿金（N）"""
    # 超过三倍封顶的按三倍封顶计算
    effective_salary = min(monthly_salary, SHANGHAI_TRIPLE_CAP)

    # 高收入者工作年限最高12年
    if monthly_salary > SHANGHAI_TRIPLE_CAP:
        work_years = min(work_years, 12)

    return effective_salary * work_years, effective_salary, work_years


def format_money(amount):
    """格式化金额"""
    return f"{amount:,.2f}"


def main():
    print("=" * 70)
    print(" " * 15 + "上海劳动仲裁赔偿计算器 v1.0")
    print(" " * 20 + "WorkPowers / 劳动者力量")
    print("=" * 70)
    print()
    print("【上海2024-2025年度标准】")
    print(f"  月平均工资：{SHANGHAI_AVG_SALARY:,}元")
    print(f"  三倍封顶：{SHANGHAI_TRIPLE_CAP:,}元")
    print()

    # 输入基本信息
    print("【基本信息】")
    start_date = get_date_input("请输入入职日期（格式：YYYY-MM-DD）：")
    end_date = get_date_input("请输入离职/拟离职日期（格式：YYYY-MM-DD）：")
    monthly_salary = get_float_input("请输入月薪（税前，含奖金补贴的平均工资，元）：")

    # 计算工作年限
    work_years = calculate_work_years(start_date, end_date)

    print()
    print("【工作年限计算】")
    print(f"  入职日期：{start_date}")
    print(f"  离职日期：{end_date}")
    print(f"  工作年限：{work_years:.1f} 年")

    # 判断是否高收入
    is_high_income = monthly_salary > SHANGHAI_TRIPLE_CAP
    if is_high_income:
        print(
            f"  ⚠️ 您的月薪{monthly_salary:,.0f}元超过上海三倍封顶（{SHANGHAI_TRIPLE_CAP:,}元）"
        )
        print(f"     按三倍封顶计算，工作年限最高12年")

    # 计算N
    n_amount, effective_salary, effective_years = calculate_n(
        monthly_salary, work_years
    )

    print()
    print("=" * 70)
    print("【赔偿计算结果】")
    print("=" * 70)

    # 1. 经济补偿金（N）
    print()
    print(f"1. 经济补偿金（N）- 协商解除或被迫解除")
    if is_high_income:
        print(
            f"   计算方式：{SHANGHAI_TRIPLE_CAP:,.0f}元 × {effective_years:.1f}年（封顶计算）"
        )
    else:
        print(f"   计算方式：{monthly_salary:,.0f}元 × {work_years:.1f}年")
    print(f"   金额：{format_money(n_amount)} 元")

    # 2. 代通知金（+1）
    plus_one = effective_salary
    n_plus_1 = n_amount + plus_one
    print()
    print(f"2. 经济补偿金+代通知金（N+1）")
    print(f"   适用场景：公司未提前30日通知解除（第40条情形）")
    if is_high_income:
        print(f"   计算方式：{format_money(n_amount)} + {SHANGHAI_TRIPLE_CAP:,.0f}元")
    else:
        print(f"   计算方式：{format_money(n_amount)} + {format_money(plus_one)}")
    print(f"   金额：{format_money(n_plus_1)} 元")

    # 3. 违法解除赔偿金（2N）
    n_double = n_amount * 2
    print()
    print(f"3. 违法解除赔偿金（2N）⭐ 推荐主张")
    print(f"   适用场景：公司违法解除（无理由、口头辞退、软裁员等）")
    print(f"   计算方式：{format_money(n_amount)} × 2")
    print(f"   金额：{format_money(n_double)} 元")

    # 4. 加班费（可选）
    print()
    print("4. 加班费（可选）")
    calc_overtime = get_yes_no_input("   是否计算加班费？（y/n）：")
    if calc_overtime:
        hourly_wage = effective_salary / 21.75 / 8
        print(f"   小时工资：{hourly_wage:.2f} 元")
        print()

        weekday_hours = get_float_input("   工作日加班小时数（1.5倍，默认0）：", 0)
        weekend_hours = get_float_input("   休息日加班小时数（2倍，默认0）：", 0)
        holiday_hours = get_float_input("   法定假日加班小时数（3倍，默认0）：", 0)

        weekday_pay = hourly_wage * 1.5 * weekday_hours
        weekend_pay = hourly_wage * 2 * weekend_hours
        holiday_pay = hourly_wage * 3 * holiday_hours
        total_overtime = weekday_pay + weekend_pay + holiday_pay

        print()
        print(f"   工作日加班费：{format_money(weekday_pay)} 元")
        print(f"   休息日加班费：{format_money(weekend_pay)} 元")
        print(f"   法定假日加班费：{format_money(holiday_pay)} 元")
        print(f"   加班费合计：{format_money(total_overtime)} 元")
    else:
        total_overtime = 0

    # 5. 未休年假补偿（可选）
    print()
    print("5. 未休年假补偿（可选）")
    calc_leave = get_yes_no_input("   是否计算未休年假补偿？（y/n）：")
    if calc_leave:
        unused_days = int(get_float_input("   未休年假天数：", 0))
        daily_wage = effective_salary / 21.75
        leave_compensation = daily_wage * unused_days * 3
        print(f"   日工资：{daily_wage:.2f} 元")
        print(f"   未休年假补偿：{format_money(leave_compensation)} 元")
    else:
        leave_compensation = 0

    # 总计
    print()
    print("=" * 70)
    print("【总结】")
    print("=" * 70)
    print(f"  经济补偿金（N）：        {format_money(n_amount)} 元")
    print(f"  违法解除赔偿金（2N）：    {format_money(n_double)} 元 ⭐")

    if calc_overtime and total_overtime > 0:
        print(f"  加班费：                 {format_money(total_overtime)} 元")
    if calc_leave and leave_compensation > 0:
        print(f"  未休年假补偿：           {format_money(leave_compensation)} 元")

    total_max = n_double + total_overtime + leave_compensation
    print()
    print(f"  合计（2N+加班费+年假）：{format_money(total_max)} 元")

    print()
    print("=" * 70)
    print("【重要提示】")
    print("  1. 仲裁时效为1年，从离职之日起算，不要拖！")
    print("  2. 劳动仲裁免费，无需支付任何费用")
    print("  3. 建议咨询专业劳动法律师获取针对性建议")
    print("  4. 以上计算仅供参考，实际金额以仲裁/法院判决为准")
    print("=" * 70)
    print()
    print("祝维权顺利！💪")


def calculate_compensation(start_date_str, end_date_str, monthly_salary, illegal_termination=True):
    """
    非交互式计算接口，供 Claude 直接调用。

    参数：
        start_date_str: 入职日期 "YYYY-MM-DD"
        end_date_str: 离职日期 "YYYY-MM-DD"
        monthly_salary: 月薪（元）
        illegal_termination: 是否违法解除（True=2N，False=N）

    返回：
        dict 包含所有计算结果
    """
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    work_years = calculate_work_years(start_date, end_date)
    is_high_income = monthly_salary > SHANGHAI_TRIPLE_CAP

    n_amount, effective_salary, effective_years = calculate_n(monthly_salary, work_years)
    n_double = n_amount * 2

    result = {
        "work_years": work_years,
        "is_high_income": is_high_income,
        "monthly_salary": monthly_salary,
        "effective_salary": effective_salary,
        "effective_years": effective_years,
        "n": n_amount,
        "n_plus_1": n_amount + effective_salary,
        "two_n": n_double,
        "shanghai_avg_salary": SHANGHAI_AVG_SALARY,
        "shanghai_triple_cap": SHANGHAI_TRIPLE_CAP,
    }

    if illegal_termination:
        result["recommended"] = n_double
        result["recommended_label"] = "违法解除赔偿金（2N）"
    else:
        result["recommended"] = n_amount
        result["recommended_label"] = "经济补偿金（N）"

    return result


def cli_mode():
    """命令行模式：python calculator.py --start 2020-03-15 --end 2025-03-15 --salary 25000 --illegal"""
    import argparse
    parser = argparse.ArgumentParser(description="上海劳动仲裁赔偿计算器")
    parser.add_argument("--start", help="入职日期 YYYY-MM-DD")
    parser.add_argument("--end", help="离职日期 YYYY-MM-DD")
    parser.add_argument("--salary", type=float, help="月薪（元）")
    parser.add_argument("--illegal", action="store_true", default=True, help="违法解除（默认2N）")
    parser.add_argument("--legal", action="store_true", help="合法解除（N）")
    args = parser.parse_args()

    if not all([args.start, args.end, args.salary]):
        parser.print_help()
        print("\n示例：python calculator.py --start 2020-03-15 --end 2025-03-15 --salary 25000 --illegal")
        return

    illegal = not args.legal
    result = calculate_compensation(args.start, args.end, args.salary, illegal)

    print("=" * 50)
    print("上海劳动仲裁赔偿计算结果")
    print("=" * 50)
    print(f"入职日期：{args.start}")
    print(f"离职日期：{args.end}")
    print(f"工作年限：{result['work_years']:.1f} 年")
    print(f"月薪：{result['monthly_salary']:,.0f} 元")
    if result['is_high_income']:
        print(f"⚠️ 月薪超过三倍封顶（{result['shanghai_triple_cap']:,}元），按封顶计算")
        print(f"  有效年限：{result['effective_years']:.1f} 年（最高12年）")
    print(f"经济补偿金（N）：{result['n']:,.2f} 元")
    print(f"N+1：{result['n_plus_1']:,.2f} 元")
    print(f"违法解除赔偿金（2N）：{result['two_n']:,.2f} 元")
    print(f"推荐主张：{result['recommended_label']} = {result['recommended']:,.2f} 元")
    print("=" * 50)


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            cli_mode()
        else:
            main()
    except KeyboardInterrupt:
        print("\n\n已退出计算器。")
        sys.exit(0)
    except Exception as e:
        print(f"\n发生错误：{e}")
        sys.exit(1)
