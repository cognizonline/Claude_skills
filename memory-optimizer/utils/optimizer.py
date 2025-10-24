"""
Memory Optimizer for Cogniz Memory Platform

Provides deterministic optimization algorithms for memory content compression,
metadata standardization, and quality improvements.
"""

import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import Counter


@dataclass
class MemoryItem:
    """Represents a single memory entry"""
    id: str
    content: str
    metadata: Dict[str, Any]
    compressed_size: Optional[int] = None
    project_id: str = "default"
    created_at: Optional[str] = None


@dataclass
class OptimizationResult:
    """Results from optimization operation"""
    status: str
    memories_processed: int
    memories_improved: int
    total_savings_bytes: int
    average_improvement_percent: float
    optimized_memories: List[Dict[str, Any]]

    def to_json(self) -> str:
        """Convert results to JSON string"""
        return json.dumps(asdict(self), indent=2)


class MemoryOptimizer:
    """Main optimizer class for memory content"""

    def __init__(self):
        self.stats = {
            'original_size': 0,
            'optimized_size': 0,
            'memories_processed': 0,
            'memories_improved': 0
        }

    def load_memories(self, source: str = 'json', data: Optional[List[Dict]] = None,
                     project_id: Optional[str] = None) -> List[MemoryItem]:
        """
        Load memories from various sources

        Args:
            source: Source type ('json', 'database', 'api')
            data: Memory data (for json source)
            project_id: Filter by project ID

        Returns:
            List of MemoryItem objects
        """
        if source == 'json' and data:
            return [MemoryItem(**item) for item in data]

        # For database/API sources, would need connection details
        # Placeholder for future implementation
        return []

    def optimize(self, memories: List[MemoryItem], mode: str = 'optimize',
                options: Optional[Dict[str, Any]] = None) -> OptimizationResult:
        """
        Main optimization entry point

        Args:
            memories: List of memory items to optimize
            mode: 'analyze', 'optimize', or 'report'
            options: Optimization configuration

        Returns:
            OptimizationResult with details
        """
        if options is None:
            options = {
                'normalize_whitespace': True,
                'standardize_metadata': True,
                'auto_categorize': True,
                'compression_level': 'high'
            }

        optimized = []
        total_savings = 0
        improvements = []

        for memory in memories:
            self.stats['memories_processed'] += 1
            original_size = len(memory.content.encode('utf-8'))
            self.stats['original_size'] += original_size

            # Apply optimizations
            optimized_content = memory.content
            changes = []

            if options.get('normalize_whitespace', True):
                optimized_content, whitespace_saved = self._normalize_whitespace(optimized_content)
                if whitespace_saved > 0:
                    changes.append(f"Removed {whitespace_saved} bytes of whitespace")

            if options.get('standardize_metadata', True):
                memory.metadata = self._standardize_metadata(memory.metadata)
                changes.append("Normalized metadata")

            if options.get('auto_categorize', True):
                category = self._auto_categorize(optimized_content)
                if category and not memory.metadata.get('category'):
                    memory.metadata['category'] = category
                    changes.append(f"Added category: {category}")

            optimized_size = len(optimized_content.encode('utf-8'))
            self.stats['optimized_size'] += optimized_size

            savings = original_size - optimized_size
            improvement_percent = (savings / original_size * 100) if original_size > 0 else 0

            if savings > 0:
                self.stats['memories_improved'] += 1
                total_savings += savings
                improvements.append(improvement_percent)

            optimized.append({
                'id': memory.id,
                'original_size': original_size,
                'optimized_size': optimized_size,
                'improvement_percent': round(improvement_percent, 1),
                'changes_applied': changes,
                'optimized_content': optimized_content if mode == 'optimize' else None,
                'metadata': memory.metadata
            })

        avg_improvement = sum(improvements) / len(improvements) if improvements else 0

        return OptimizationResult(
            status='success',
            memories_processed=self.stats['memories_processed'],
            memories_improved=self.stats['memories_improved'],
            total_savings_bytes=total_savings,
            average_improvement_percent=round(avg_improvement, 1),
            optimized_memories=optimized
        )

    def _normalize_whitespace(self, content: str) -> tuple[str, int]:
        """
        Remove redundant whitespace

        Returns:
            (optimized_content, bytes_saved)
        """
        original_size = len(content.encode('utf-8'))

        # Remove leading/trailing whitespace
        content = content.strip()

        # Normalize multiple spaces to single space
        content = re.sub(r' +', ' ', content)

        # Normalize multiple newlines to max 2
        content = re.sub(r'\n{3,}', '\n\n', content)

        # Remove trailing whitespace from lines
        content = '\n'.join(line.rstrip() for line in content.split('\n'))

        optimized_size = len(content.encode('utf-8'))
        bytes_saved = original_size - optimized_size

        return content, bytes_saved

    def _standardize_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Standardize metadata structure and keys

        Returns:
            Standardized metadata dictionary
        """
        standard = {}

        # Standardize common key variations
        key_mappings = {
            'cat': 'category',
            'cats': 'category',
            'tag': 'tags',
            'label': 'tags',
            'labels': 'tags',
            'type': 'category',
            'kind': 'category'
        }

        for key, value in metadata.items():
            # Normalize key names
            standard_key = key_mappings.get(key.lower(), key.lower())

            # Remove empty values
            if value is None or value == '' or value == []:
                continue

            # Standardize tag format
            if standard_key == 'tags':
                if isinstance(value, str):
                    value = [tag.strip() for tag in value.split(',')]
                elif isinstance(value, list):
                    value = [str(tag).strip() for tag in value]

            standard[standard_key] = value

        return standard

    def _auto_categorize(self, content: str) -> Optional[str]:
        """
        Automatically categorize content based on keywords

        Returns:
            Category name or None
        """
        content_lower = content.lower()

        # Define category keywords
        categories = {
            'documentation': ['docs', 'guide', 'tutorial', 'documentation', 'readme', 'manual'],
            'code': ['function', 'class', 'import', 'const', 'var', 'def', 'return'],
            'meeting': ['meeting', 'agenda', 'minutes', 'attendees', 'action items'],
            'research': ['research', 'analysis', 'study', 'findings', 'hypothesis'],
            'planning': ['roadmap', 'milestone', 'deadline', 'project plan', 'sprint'],
            'communication': ['email', 'message', 'conversation', 'chat', 'discussion'],
            'data': ['dataset', 'metrics', 'analytics', 'statistics', 'numbers'],
            'idea': ['idea', 'brainstorm', 'concept', 'proposal', 'suggestion']
        }

        # Count keyword matches per category
        category_scores = {}
        for category, keywords in categories.items():
            score = sum(1 for keyword in keywords if keyword in content_lower)
            if score > 0:
                category_scores[category] = score

        # Return highest scoring category
        if category_scores:
            return max(category_scores.items(), key=lambda x: x[1])[0]

        return None

    def analyze(self, memories: List[MemoryItem]) -> Dict[str, Any]:
        """
        Analyze memories and provide optimization recommendations

        Returns:
            Analysis report dictionary
        """
        total_size = sum(len(m.content.encode('utf-8')) for m in memories)
        avg_size = total_size / len(memories) if memories else 0

        # Find optimization opportunities
        opportunities = {
            'redundant_content': 0,
            'metadata_issues': 0,
            'categorization_missing': 0,
            'encoding_inefficient': 0
        }

        for memory in memories:
            # Check for excessive whitespace
            if len(memory.content) != len(memory.content.strip()):
                opportunities['redundant_content'] += 1

            # Check metadata quality
            if not memory.metadata or len(memory.metadata) == 0:
                opportunities['metadata_issues'] += 1

            # Check categorization
            if not memory.metadata.get('category'):
                opportunities['categorization_missing'] += 1

        # Estimate potential savings (conservative 25% average)
        potential_savings = int(total_size * 0.25)

        recommendations = []
        if opportunities['redundant_content'] > 0:
            recommendations.append(
                f"Remove redundant whitespace in {opportunities['redundant_content']} memories"
            )
        if opportunities['metadata_issues'] > 0:
            recommendations.append(
                f"Add metadata to {opportunities['metadata_issues']} memories"
            )
        if opportunities['categorization_missing'] > 0:
            recommendations.append(
                f"Categorize {opportunities['categorization_missing']} uncategorized memories"
            )

        return {
            'status': 'success',
            'analysis': {
                'total_memories': len(memories),
                'total_size_bytes': total_size,
                'average_size_bytes': int(avg_size),
                'optimization_opportunities': opportunities
            },
            'recommendations': recommendations,
            'potential_savings': {
                'storage_reduction_percent': 25,
                'estimated_bytes_saved': potential_savings
            }
        }


# Example usage for testing
if __name__ == '__main__':
    # Sample data
    sample_memories = [
        {
            'id': 'mem_001',
            'content': '  This is a test memory   with excessive   whitespace.  \n\n\n\n  ',
            'metadata': {'cat': 'test', 'label': 'example'},
            'project_id': 'test-project'
        },
        {
            'id': 'mem_002',
            'content': 'Meeting notes from today. Discussed the new feature roadmap and sprint planning.',
            'metadata': {},
            'project_id': 'test-project'
        }
    ]

    # Initialize optimizer
    optimizer = MemoryOptimizer()

    # Load memories
    memories = optimizer.load_memories(source='json', data=sample_memories)

    # Run optimization
    results = optimizer.optimize(memories, mode='optimize')

    print(results.to_json())
