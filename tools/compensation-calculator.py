#!/usr/bin/env python3
"""
上海劳动仲裁赔偿计算器
版本：1.0
作者：Socialist-Workers-Power项目
功能：计算经济补偿金（N）、违法解除赔偿金（2N）、加班费、年假补偿等
"""

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import sys

# 上海2024年度标准（2025年7月-2026年6月执行）
SHANGHAI_AVG_SALARY = 12434  # 月平均工资（元）
SHANGHAI_TRIPLE_CAP = 37302  # 三倍封顶（元）
SHANGHAI_MIN_WAGE = 2690  # 最低工资（元）


def calculate_work_years(start_date, end_date):
    """计算工作年限（精确到月）"""
    delta = relativedelta(end_date, start_date)
    years = delta.years
    months = delta.months

    # 超过6个月按1年算，不满6个月按0.5年算
    if months >= 6:
        years += 1
    elif months > 0:
        years += 0.5

    return years


def calculate_n(monthly_salary, work_years):
    """计算经济补偿金（N）"""
    # 超过三倍封顶的按三倍封顶计算
    effective_salary = min(monthly_salary, SHANGHAI_TRIPLE_CAP)

    # 高收入者工作年限最高12年
    if monthly_salary > SHANGHAI_TRIPLE_CAP:
        work_years = min(work_years, 12)

    return effective_salary * work_years


def calculate_overtime(hourly_wage, weekday_hours=0, weekend_hours=0, holiday_hours=0):
    """计算加班费"""
    weekday_pay = hourly_wage * 1.5 * weekday_hours
    weekend_pay = hourly_wage * 2 * weekend_hours
    holiday_pay = hourly_wage * 3 * holiday_hours

    return {
        "weekday": weekday_pay,
        "weekend": weekend_pay,
        "holiday": holiday_pay,
        "total": weekday_pay + weekend_pay + holiday_pay,
    }


def calculate_annual_leave(monthly_salary, unused_days):
    """计算未休年假补偿（3倍日工资）"""
    daily_wage = monthly_salary / 21.75
    return daily_wage * unused_days * 3


def main():
    print("=" * 60)
    print("  上海劳动仲裁赔偿计算器 v1.0")
    print("  Socialist-Workers-Power 项目")
    print("=" * 60)
    print()

    # 输入基本信息
    print("【基本信息】")
    start_date_str = input("请输入入职日期（格式：YYYY-MM-DD）：")
    end_date_str = input("请输入离职日期（格式：YYYY-MM-DD）：")
    monthly_salary = float(input("请输入月薪（元）："))

    # 解析日期
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("日期格式错误！请使用 YYYY-MM-DD 格式。")
        return

    # 计算工作年限
    work_years = calculate_work_years(start_date, end_date)

    print()
    print("【工作年限计算】")
    print(f"  入职日期：{start_date}")
    print(f"  离职日期：{end_date}")
    print(f"  工作年限：{work_years:.1f} 年")

    # 判断是否为高收入
    is_high_income = monthly_salary > SHANGHAI_TRIPLE_CAP
    if is_high_income:
        print(f"  ⚠️ 您的月薪超过上海三倍封顶（{SHANGHAI_TRIPLE_CAP:,}元）")
        print(f"     按三倍封顶计算，工作年限最高12年")

    print()
    print("【赔偿计算结果】")
    print("-" * 60)

    # 计算N（经济补偿金）
    n_amount = calculate_n(monthly_salary, work_years)
    print(f"1. 经济补偿金（N）")
    print(
        f"   计算方式：{min(monthly_salary, SHANGHAI_TRIPLE_CAP):,.0f}元 × {work_years:.1f}年"
    )
    print(f"   金额：{n_amount:,.2f} 元")

    # 计算N+1（代通知金）
    n_plus_1 = n_amount + min(monthly_salary, SHANGHAI_TRIPLE_CAP)
    print()
    print(f"2. 经济补偿金+代通知金（N+1）")
    print(f"   适用场景：公司未提前30天通知解除")
    print(f"   金额：{n_plus_1:,.2f} 元")

    # 计算2N（违法解除赔偿金）
    n_double = n_amount * 2
    print()
    print(f"3. 违法解除赔偿金（2N）⭐推荐主张")
    print(f"   适用场景：公司违法解除（如停岗、关闭权限、不让进门）")
    print(f"   计算方式：{n_amount:,.2f}元 × 2")
    print(f"   金额：{n_double:,.2f} 元")

    # 加班费估算
    print()
    print("4. 加班费估算（可选）")
    calc_overtime = input("   是否计算加班费？（y/n）：").lower()
    if calc_overtime == "y":
        hourly_wage = monthly_salary / 21.75 / 8
        print(f"   小时工资：{hourly_wage:.2f} 元")

        weekday_hours = float(input("   工作日加班小时数（1.5倍）：") or 0)
        weekend_hours = float(input("   休息日加班小时数（2倍）：") or 0)
        holiday_hours = float(input("   法定假日加班小时数（3倍）：") or 0)

        overtime = calculate_overtime(
            hourly_wage, weekday_hours, weekend_hours, holiday_hours
        )
        print(f"   工作日加班费：{overtime['weekday']:,.2f} 元")
        print(f"   休息日加班费：{overtime['weekend']:,.2f} 元")
        print(f"   法定假日加班费：{overtime['holiday']:,.2f} 元")
        print(f"   加班费合计：{overtime['total']:,.2f} 元")

    # 未休年假
    print()
    print("5. 未休年假补偿（可选）")
    calc_leave = input("   是否计算未休年假？（y/n）：").lower()
    if calc_leave == "y":
        unused_days = int(input("   未休年假天数：") or 0)
        leave_compensation = calculate_annual_leave(monthly_salary, unused_days)
        print(f"   日工资：{monthly_salary / 21.75:.2f} 元")
        print(f"   未休年假补偿：{leave_compensation:,.2f} 元")

    # 总计
    print()
    print("=" * 60)
    print("【总结】")
    print(f"  经济补偿金（N）：{n_amount:,.2f} 元")
    print(f"  违法解除赔偿金（2N）：{n_double:,.2f} 元 ⭐")
    print()
    print("【重要提示】")
    print("  1. 仲裁时效为1年，从离职之日起算")
    print("  2. 劳动仲裁免费，无需支付任何费用")
    print("  3. 建议咨询专业劳动法律师获取针对性建议")
    print()
    print("【参考标准】")
    print(f"  上海2024年度月平均工资：{SHANGHAI_AVG_SALARY:,}元")
    print(f"  三倍封顶：{SHANGHAI_TRIPLE_CAP:,}元")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已退出计算器。")
        sys.exit(0)
    except Exception as e:
        print(f"\n发生错误：{e}")
        sys.exit(1)
