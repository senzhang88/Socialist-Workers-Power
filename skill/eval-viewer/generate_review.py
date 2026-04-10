#!/usr/bin/env python3
"""
评估结果可视化查看器
生成HTML报告便于查看对比
用法: python eval-viewer/generate_review.py logs/iteration-1/results.json
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>劳动维权技能评估报告 - {date}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .stats-grid {{ 
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .stat-card {{ 
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-card h3 {{ 
            font-size: 14px;
            color: #666;
            text-transform: uppercase;
            margin-bottom: 8px;
        }}
        .stat-card .value {{ 
            font-size: 32px;
            font-weight: bold;
            color: #333;
        }}
        .stat-card.pass .value {{ color: #22c55e; }}
        .stat-card.fail .value {{ color: #ef4444; }}
        .section {{ 
            background: white;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .section h2 {{ 
            font-size: 20px;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        .dimension-bar {{ 
            display: flex;
            align-items: center;
            margin: 10px 0;
        }}
        .dimension-bar .label {{ 
            width: 120px;
            font-weight: 500;
        }}
        .dimension-bar .bar-container {{ 
            flex: 1;
            height: 24px;
            background: #e5e7eb;
            border-radius: 12px;
            overflow: hidden;
        }}
        .dimension-bar .bar {{ 
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 12px;
            transition: width 0.3s ease;
        }}
        .dimension-bar .score {{ 
            width: 60px;
            text-align: right;
            font-weight: bold;
            margin-left: 10px;
        }}
        .result-item {{ 
            border-left: 4px solid #e5e7eb;
            padding: 15px;
            margin: 10px 0;
            background: #f9fafb;
            border-radius: 0 8px 8px 0;
        }}
        .result-item.passed {{ border-left-color: #22c55e; }}
        .result-item.failed {{ border-left-color: #ef4444; }}
        .result-item h4 {{ 
            font-size: 16px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
        }}
        .result-item .score-badge {{ 
            background: #667eea;
            color: white;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 14px;
        }}
        .result-item .issues {{ 
            margin-top: 10px;
            padding: 10px;
            background: #fef2f2;
            border-radius: 6px;
            font-size: 14px;
        }}
        .result-item .issues ul {{ 
            margin-left: 20px;
            margin-top: 5px;
        }}
        .issue-tag {{ 
            display: inline-block;
            background: #fee2e2;
            color: #991b1b;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            margin: 2px;
        }}
        .comparison-table {{ width: 100%; border-collapse: collapse; }}
        .comparison-table th,
        .comparison-table td {{ 
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }}
        .comparison-table th {{ 
            background: #f9fafb;
            font-weight: 600;
        }}
        .trend-up {{ color: #22c55e; }}
        .trend-down {{ color: #ef4444; }}
        .trend-neutral {{ color: #6b7280; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ 上海劳动维权技能评估报告</h1>
            <p>生成时间: {date}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>总测试数</h3>
                <div class="value">{total}</div>
            </div>
            <div class="stat-card pass">
                <h3>通过</h3>
                <div class="value">{passed}</div>
            </div>
            <div class="stat-card fail">
                <h3>失败</h3>
                <div class="value">{failed}</div>
            </div>
            <div class="stat-card">
                <h3>通过率</h3>
                <div class="value">{pass_rate}%</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 维度评分</h2>
            {dimension_bars}
        </div>
        
        <div class="section">
            <h2>⚠️ 常见问题</h2>
            {common_issues}
        </div>
        
        <div class="section">
            <h2>📝 详细结果</h2>
            {detailed_results}
        </div>
    </div>
</body>
</html>
"""


def generate_dimension_bars(stats: dict) -> str:
    """生成维度评分条"""
    bars = []
    dim_names = {
        "actionability": "可执行性",
        "accuracy": "准确性",
        "completeness": "完整性",
        "stance": "立场",
        "tool_usage": "工具使用",
    }

    for dim, data in stats.items():
        name = dim_names.get(dim, dim)
        avg = data.get("avg", 0)
        percentage = (avg / 5) * 100
        bars.append(f"""
        <div class="dimension-bar">
            <div class="label">{name}</div>
            <div class="bar-container">
                <div class="bar" style="width: {percentage}%"></div>
            </div>
            <div class="score">{avg}/5</div>
        </div>
        """)
    return "\n".join(bars)


def generate_common_issues(issues: list) -> str:
    """生成常见问题列表"""
    if not issues:
        return '<p style="color: #22c55e;">✅ 未发现系统性问题</p>'

    items = []
    for issue in issues:
        freq = issue.get("frequency", 0)
        pattern = issue.get("issue_pattern", "Unknown")
        items.append(f"""
        <div style="margin: 10px 0; padding: 15px; background: #fef2f2; border-radius: 6px;">
            <strong>{pattern}...</strong>
            <span style="float: right; background: #fee2e2; color: #991b1b; padding: 2px 8px; border-radius: 4px; font-size: 12px;">
                出现 {freq} 次
            </span>
        </div>
        """)
    return "\n".join(items)


def generate_detailed_results(results: list) -> str:
    """生成详细结果列表"""
    items = []
    for r in results:
        status_class = "passed" if r.get("passed") else "failed"
        status_icon = "✅" if r.get("passed") else "❌"
        score = r.get("total_score", 0)
        query = r.get("query", "Unknown")[:80] + "..."

        issues_html = ""
        if r.get("issues"):
            issues_list = "".join([f"<li>{issue}</li>" for issue in r["issues"][:3]])
            issues_html = f'<div class="issues"><strong>问题:</strong><ul>{issues_list}</ul></div>'

        items.append(f"""
        <div class="result-item {status_class}">
            <h4>
                <span>{status_icon} {query}</span>
                <span class="score-badge">{score}/25</span>
            </h4>
            {issues_html}
        </div>
        """)
    return "\n".join(items)


def generate_html_report(data: dict, output_path: str):
    """生成HTML报告"""
    summary = data.get("summary", {})
    stats = data.get("dimension_stats", {})
    issues = data.get("common_issues", [])
    results = data.get("detailed_results", [])

    html = HTML_TEMPLATE.format(
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total=summary.get("total", 0),
        passed=summary.get("passed", 0),
        failed=summary.get("failed", 0),
        pass_rate=summary.get("pass_rate", 0),
        dimension_bars=generate_dimension_bars(stats),
        common_issues=generate_common_issues(issues),
        detailed_results=generate_detailed_results(results),
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"报告已生成: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="生成劳动维权技能评估报告")
    parser.add_argument("input", help="评估结果JSON文件路径")
    parser.add_argument(
        "-o", "--output", default="eval-report.html", help="输出HTML文件路径"
    )
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    generate_html_report(data, args.output)


if __name__ == "__main__":
    main()
