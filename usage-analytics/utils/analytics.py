"""
Usage Analytics Reporter for Cogniz Memory Platform

Generates comprehensive usage reports and analytics from database queries.
Calculates KPIs, trends, and provides business intelligence insights.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class UsageMetrics:
    """Container for usage metrics"""
    total_memories: int
    storage_bytes: int
    active_users: int
    api_requests: int
    dau: int  # Daily Active Users
    wau: int  # Weekly Active Users
    mau: int  # Monthly Active Users


@dataclass
class CategoryStats:
    """Statistics for a memory category"""
    name: str
    count: int
    storage_bytes: int
    avg_size_bytes: int


class UsageAnalytics:
    """Main analytics engine for usage reporting"""

    def __init__(self, db_config: Optional[Dict] = None):
        """
        Initialize analytics engine

        Args:
            db_config: Database connection configuration (optional for testing)
        """
        self.db_config = db_config or {}
        self.stats = {
            'queries_executed': 0,
            'metrics_calculated': 0,
            'reports_generated': 0
        }

    def generate_report(self, report_type: str = 'usage_summary',
                       time_period: str = 'last_30_days',
                       filters: Optional[Dict] = None,
                       output_format: str = 'markdown') -> str:
        """
        Generate analytics report

        Args:
            report_type: Type of report to generate
            time_period: Time range for analysis
            filters: Optional filtering criteria
            output_format: Output format (markdown, json, csv)

        Returns:
            Generated report as string
        """
        # Parse time period
        start_date, end_date = self._parse_time_period(time_period)

        # Get data (would query database in real implementation)
        data = self._get_sample_data(start_date, end_date, filters)

        # Generate report based on type
        if report_type == 'usage_summary':
            report = self._generate_usage_summary(data, output_format)
        elif report_type == 'storage_analysis':
            report = self._generate_storage_analysis(data, output_format)
        elif report_type == 'api_metrics':
            report = self._generate_api_metrics(data, output_format)
        else:
            report = self._generate_custom_report(data, output_format)

        self.stats['reports_generated'] += 1
        return report

    def _parse_time_period(self, time_period: str) -> Tuple[datetime, datetime]:
        """
        Parse time period string into date range

        Returns:
            (start_date, end_date) tuple
        """
        end_date = datetime.now()

        if time_period == 'last_7_days':
            start_date = end_date - timedelta(days=7)
        elif time_period == 'last_30_days':
            start_date = end_date - timedelta(days=30)
        elif time_period == 'last_quarter':
            start_date = end_date - timedelta(days=90)
        elif time_period == 'last_year':
            start_date = end_date - timedelta(days=365)
        else:
            # Default to last 30 days
            start_date = end_date - timedelta(days=30)

        return start_date, end_date

    def _get_sample_data(self, start_date: datetime, end_date: datetime,
                        filters: Optional[Dict]) -> Dict[str, Any]:
        """
        Get analytics data (sample data for testing)

        In production, this would execute database queries.
        For now, returns realistic sample data.

        Returns:
            Dictionary with analytics data
        """
        self.stats['queries_executed'] += 1

        # Calculate days in period
        days = (end_date - start_date).days

        # Generate sample metrics
        return {
            'metrics': UsageMetrics(
                total_memories=15847,
                storage_bytes=2417483648,  # ~2.3 GB
                active_users=234,
                api_requests=47392,
                dau=87,
                wau=156,
                mau=234
            ),
            'operations': {
                'store': 12456,
                'search': 2891,
                'delete': 500
            },
            'categories': [
                CategoryStats('Documentation', 5234, 897581056, 171520),
                CategoryStats('Meeting Notes', 3891, 443596800, 114048),
                CategoryStats('Code Snippets', 2456, 327155712, 133120),
                CategoryStats('Research', 1789, 466616320, 260864),
                CategoryStats('Other', 2477, 276889600, 111744)
            ],
            'top_projects': [
                {'name': 'engineering-docs', 'count': 3456, 'percentage': 21.8},
                {'name': 'meeting-notes-2024', 'count': 2891, 'percentage': 18.2},
                {'name': 'research-archive', 'count': 1987, 'percentage': 12.5}
            ],
            'growth': {
                'memory_growth_percent': 23,
                'user_growth_percent': 15,
                'storage_growth_percent': 18,
                'api_growth_percent': 31
            },
            'period': {
                'start': start_date.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d'),
                'days': days
            }
        }

    def _generate_usage_summary(self, data: Dict[str, Any],
                                output_format: str) -> str:
        """Generate usage summary report"""
        self.stats['metrics_calculated'] += 10

        if output_format == 'json':
            return self._format_json(data)
        elif output_format == 'csv':
            return self._format_csv(data)
        else:  # markdown
            return self._format_markdown_summary(data)

    def _format_markdown_summary(self, data: Dict[str, Any]) -> str:
        """Format usage summary as markdown"""
        metrics = data['metrics']
        operations = data['operations']
        categories = data['categories']
        projects = data['top_projects']
        growth = data['growth']
        period = data['period']

        # Calculate percentages
        total_ops = sum(operations.values())
        storage_gb = metrics.storage_bytes / (1024 ** 3)
        dau_mau_ratio = (metrics.dau / metrics.mau * 100) if metrics.mau > 0 else 0

        md = []
        md.append("# Cogniz Memory Platform Usage Report")
        md.append(f"**Period**: {period['start']} to {period['end']}\n")

        # Executive Summary
        md.append("## Executive Summary")
        md.append(f"- Total Memories: {metrics.total_memories:,} (+{growth['memory_growth_percent']}% from previous period)")
        md.append(f"- Storage Used: {storage_gb:.1f} GB (+{growth['storage_growth_percent']}% from previous period)")
        md.append(f"- Active Users: {metrics.active_users:,} (+{growth['user_growth_percent']}% from previous period)")
        md.append(f"- API Requests: {metrics.api_requests:,} (+{growth['api_growth_percent']}% from previous period)\n")

        # Key Metrics
        md.append("## Key Metrics\n")

        # Operations
        md.append("### Memory Operations")
        md.append("| Operation | Count | % of Total |")
        md.append("|-----------|-------|------------|")
        for op, count in operations.items():
            percentage = (count / total_ops * 100) if total_ops > 0 else 0
            md.append(f"| {op.capitalize()} | {count:,} | {percentage:.1f}% |")
        md.append("")

        # Categories
        md.append("### Storage by Category")
        md.append("| Category | Memories | Storage (MB) | Avg Size (KB) |")
        md.append("|----------|----------|--------------|---------------|")
        for cat in categories:
            storage_mb = cat.storage_bytes / (1024 ** 2)
            avg_size_kb = cat.avg_size_bytes / 1024
            md.append(f"| {cat.name} | {cat.count:,} | {storage_mb:.0f} | {avg_size_kb:.0f} |")
        md.append("")

        # User Engagement
        md.append("### User Engagement")
        md.append(f"- Daily Active Users (DAU): {metrics.dau}")
        md.append(f"- Weekly Active Users (WAU): {metrics.wau}")
        md.append(f"- Monthly Active Users (MAU): {metrics.mau}")
        md.append(f"- DAU/MAU Ratio: {dau_mau_ratio:.1f}%\n")

        # Top Projects
        md.append("### Top Projects")
        for i, proj in enumerate(projects, 1):
            md.append(f"{i}. **{proj['name']}** - {proj['count']:,} memories ({proj['percentage']}%)")
        md.append("")

        # Growth Trends
        md.append("## Growth Trends")
        md.append(f"- Memory Growth: +{growth['memory_growth_percent']}% MoM")
        md.append(f"- User Growth: +{growth['user_growth_percent']}% MoM")
        md.append(f"- Storage Growth: +{growth['storage_growth_percent']}% MoM")
        md.append(f"- API Usage Growth: +{growth['api_growth_percent']}% MoM\n")

        # Insights
        md.append("## Insights & Recommendations")
        md.append(f"1. **High Engagement**: DAU/MAU ratio of {dau_mau_ratio:.0f}% indicates strong user retention")
        md.append(f"2. **API Growth**: {growth['api_growth_percent']}% increase in API usage suggests platform adoption")
        md.append(f"3. **Storage Distribution**: Top category ({categories[0].name}) represents {categories[0].count/metrics.total_memories*100:.1f}% of memories")

        if operations.get('delete', 0) > 0:
            md.append(f"4. **Memory Cleanup**: {operations['delete']:,} deletions suggest active memory management\n")

        # Action Items
        md.append("## Action Items")
        md.append("- Monitor API growth for capacity planning")
        md.append("- Analyze user engagement patterns for retention strategies")
        md.append("- Consider storage optimization opportunities")

        return "\n".join(md)

    def _generate_storage_analysis(self, data: Dict[str, Any],
                                   output_format: str) -> str:
        """Generate storage analysis report"""
        self.stats['metrics_calculated'] += 5

        categories = data['categories']
        total_storage = sum(cat.storage_bytes for cat in categories)

        md = []
        md.append("# Storage Analysis Report\n")

        md.append("## Storage Distribution")
        md.append("| Category | Storage (GB) | % of Total | Avg Size (KB) | Optimization Potential |")
        md.append("|----------|-------------|------------|---------------|------------------------|")

        for cat in sorted(categories, key=lambda x: x.storage_bytes, reverse=True):
            storage_gb = cat.storage_bytes / (1024 ** 3)
            percentage = (cat.storage_bytes / total_storage * 100) if total_storage > 0 else 0
            avg_kb = cat.avg_size_bytes / 1024
            # Simple heuristic: larger avg size = more optimization potential
            opt_potential = "High" if avg_kb > 150 else "Medium" if avg_kb > 100 else "Low"
            md.append(f"| {cat.name} | {storage_gb:.2f} | {percentage:.1f}% | {avg_kb:.0f} | {opt_potential} |")

        md.append(f"\n**Total Storage**: {total_storage / (1024**3):.2f} GB")

        return "\n".join(md)

    def _generate_api_metrics(self, data: Dict[str, Any],
                              output_format: str) -> str:
        """Generate API metrics report"""
        self.stats['metrics_calculated'] += 3

        operations = data['operations']
        total = sum(operations.values())

        md = []
        md.append("# API Metrics Report\n")

        md.append("## Endpoint Usage")
        md.append("| Endpoint | Requests | % of Total | Avg/Day |")
        md.append("|----------|----------|------------|---------|")

        days = data['period']['days'] or 30
        for endpoint, count in sorted(operations.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total * 100) if total > 0 else 0
            avg_per_day = count / days
            md.append(f"| /memory/v1/{endpoint} | {count:,} | {percentage:.1f}% | {avg_per_day:.0f} |")

        md.append(f"\n**Total API Requests**: {total:,}")

        return "\n".join(md)

    def _generate_custom_report(self, data: Dict[str, Any],
                                output_format: str) -> str:
        """Generate custom report"""
        return self._format_json(data)

    def _format_json(self, data: Dict[str, Any]) -> str:
        """Format data as JSON"""
        # Convert dataclasses to dicts
        json_data = {
            'metrics': asdict(data['metrics']),
            'operations': data['operations'],
            'categories': [asdict(cat) for cat in data['categories']],
            'top_projects': data['top_projects'],
            'growth': data['growth'],
            'period': data['period']
        }
        return json.dumps(json_data, indent=2)

    def _format_csv(self, data: Dict[str, Any]) -> str:
        """Format data as CSV"""
        lines = []
        lines.append("Metric,Value")

        metrics = data['metrics']
        lines.append(f"Total Memories,{metrics.total_memories}")
        lines.append(f"Storage Bytes,{metrics.storage_bytes}")
        lines.append(f"Active Users,{metrics.active_users}")
        lines.append(f"API Requests,{metrics.api_requests}")
        lines.append(f"DAU,{metrics.dau}")
        lines.append(f"WAU,{metrics.wau}")
        lines.append(f"MAU,{metrics.mau}")

        return "\n".join(lines)


# Example usage
if __name__ == '__main__':
    analytics = UsageAnalytics()

    # Generate usage summary
    report = analytics.generate_report(
        report_type='usage_summary',
        time_period='last_30_days',
        output_format='markdown'
    )

    print(report)
    print(f"\n--- Stats ---")
    print(f"Metrics calculated: {analytics.stats['metrics_calculated']}")
