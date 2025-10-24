---
name: memory-optimizer
description: Optimize memory compression and reduce storage costs through content analysis and deduplication
---

# Memory Optimizer

Analyzes stored memories to identify compression opportunities, remove redundant content, and improve storage efficiency. Best for projects with 100+ memories needing optimization.

## When to use this skill

Use this skill when:
- Storage costs are increasing and need to be reduced
- Memory retrieval performance is degrading
- Projects have many similar or duplicate memories
- Preparing to archive old project data
- Running monthly or quarterly maintenance optimization

## Instructions

1. **Load project memories**

Load the target memories from database or API:

```python
from utils.optimizer import MemoryOptimizer

optimizer = MemoryOptimizer()
memories = optimizer.load_project(project_id='docs-2024')
```

2. **Analyze optimization potential**

Run analysis to identify opportunities without making changes:

```python
analysis = optimizer.analyze(memories)
print(f"Potential savings: {analysis['potential_savings_percent']}%")
```

This identifies redundant content, metadata issues, and compression opportunities.

3. **Apply optimizations**

Execute optimization transformations:

```python
results = optimizer.optimize(
    memories=memories,
    mode='optimize',
    options={
        'normalize_whitespace': True,
        'auto_categorize': True,
        'compression_level': 'high'
    }
)
```

4. **Report savings**

Show the user clear before/after metrics:
- Storage reduction percentage
- Total bytes saved
- Number of memories improved
- Processing time

## Examples

### Example 1: Optimize Project

**User**: "Optimize all memories in my documentation project"

**Output**:
```json
{
  "memories_optimized": 150,
  "storage_saved_bytes": 146800,
  "improvement_percent": 28,
  "categories_added": 23,
  "processing_time_seconds": 1.8
}
```

### Example 2: Analysis Only

**User**: "How much could I save by optimizing project ABC?"

**Output**:
```
Analysis Results for Project ABC:
- 150 memories analyzed
- Potential savings: 28% (143 KB)
- Recommended actions:
  1. Remove excess whitespace (45 memories) - 15% savings
  2. Standardize metadata format (12 memories) - 8% savings
  3. Add missing categories (23 memories) - 5% savings
  4. Optimize encoding (8 memories) - 12% savings

Estimated processing time: 2 seconds
```

### Example 3: Batch Optimization

**User**: "Optimize all memories older than 30 days"

**Output**:
```
Batch Optimization Complete:
- 487 memories processed
- 156 memories optimized (32%)
- 412 KB saved (24% reduction)
- Processing time: 3.2 seconds

Top improvements:
- mem_abc123: 42% reduction
- mem_def456: 38% reduction
- mem_ghi789: 35% reduction
```

## Guidelines

- **Preserve content**: Never modify semantic meaning or delete user content
- **Safety first**: Always validate optimized content matches original meaning
- **Performance**: Process maximum 500 memories per batch for optimal speed
- **Backup**: Recommend user backup before bulk optimization
- **Transparency**: Show detailed before/after comparisons
- **Quality target**: Aim for 40-50% compression ratio (lower is better)

## Technical Details

**Performance**:
- ~0.5 seconds per 100 memories
- Memory limit: 100MB for analysis
- Batch size: 500 memories maximum

**Compression Targets**:
- Original typical ratio: 0.65 (65% of original size)
- Target ratio: 0.45 (45% of original size)
- Expected improvement: 20-30% additional compression

**Quality Metrics**:
- Semantic preservation: 100%
- Metadata preservation: 100%
- Lossless compression: Yes
