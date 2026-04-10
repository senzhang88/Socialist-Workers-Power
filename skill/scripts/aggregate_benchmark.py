#!/usr/bin/env python3
"""
劳动维权技能评估结果聚合脚本
用法: python scripts/aggregate_benchmark.py logs/iteration-1/*.json
"""

import json
import sys
import glob
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict


def load_result_files(pattern: str) -> List[Dict]:
    """加载所有评估结果文件"""
    results = []
    for path in glob.glob(pattern):
        with open(path) as f:
            data = json.load(f)
            data["_source_file"] = path
            results.append(data)
    return results


def aggregate_scores(results: List[Dict]) -> Dict:
    """聚合各维度分数"""
    dimensions = ["actionability", "accuracy", "completeness", "stance", "tool_usage"]
    scores = defaultdict(list)

    for r in results:
        dims = r.get("dimension_scores", {})
        for d in dimensions:
            if d in dims:
                scores[d].append(dims[d])

    stats = {}
    for d in dimensions:
        if scores[d]:
            stats[d] = {
                "avg": round(sum(scores[d]) / len(scores[d]), 2),
                "min": min(scores[d]),
                "max": max(scores[d]),
                "count": len(scores[d]),
            }
    return stats


def count_pass_fail(results: List[Dict]) -> Dict:
    """统计通过/失败"""
    passed = sum(1 for r in results if r.get("passed", False))
    return {
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "pass_rate": round(passed / len(results) * 100, 1) if results else 0,
    }


def identify_common_issues(results: List[Dict]) -> List[Dict]:
    """识别常见问题"""
    issue_counts = defaultdict(lambda: {"count": 0, "examples": []})

    for r in results:
        for issue in r.get("issues", []):
            # 简化issue用于聚类
            key = issue[:50]  # 取前50字符作为key
            issue_counts[key]["count"] += 1
            if len(issue_counts[key]["examples"]) < 3:
                issue_counts[key]["examples"].append(
                    {"issue": issue, "source": r.get("_source_file", "unknown")}
                )

    # 按频次排序
    sorted_issues = sorted(
        issue_counts.items(), key=lambda x: x[1]["count"], reverse=True
    )
    return [
        {"issue_pattern": k, "frequency": v["count"], "examples": v["examples"]}
        for k, v in sorted_issues[:5]  # 前5个常见问题
    ]


def generate_report(results: List[Dict]) -> Dict:
    """生成评估报告"""
    return {
        "summary": count_pass_fail(results),
        "dimension_stats": aggregate_scores(results),
        "common_issues": identify_common_issues(results),
        "detailed_results": [
            {
                "file": r.get("_source_file", "unknown"),
                "query": r.get("query", "unknown"),
                "passed": r.get("passed", False),
                "total_score": r.get("total_score", 0),
                "issues_count": len(r.get("issues", [])),
            }
            for r in results
        ],
    }


def main():
    if len(sys.argv) < 2:
        print("用法: python aggregate_benchmark.py logs/iteration-1/*.json")
        print("   或: python aggregate_benchmark.py 'logs/**/*.json'")
        sys.exit(1)

    pattern = sys.argv[1]
    results = load_result_files(pattern)

    if not results:
        print(f"未找到匹配文件: {pattern}")
        sys.exit(1)

    report = generate_report(results)

    # 输出JSON
    print(json.dumps(report, indent=2, ensure_ascii=False))

    # 输出摘要
    print(f"\n=== 评估摘要 ===", file=sys.stderr)
    print(f"总测试数: {report['summary']['total']}", file=sys.stderr)
    print(
        f"通过: {report['summary']['passed']} ({report['summary']['pass_rate']}%)",
        file=sys.stderr,
    )
    print(f"失败: {report['summary']['failed']}", file=sys.stderr)
    print(f"\n各维度平均分:", file=sys.stderr)
    for dim, stats in report["dimension_stats"].items():
        print(
            f"  {dim}: {stats['avg']}/5 (范围: {stats['min']}-{stats['max']})",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
