# AutoCAD MCP Performance Optimization Guide

## Current Performance Bottlenecks

1. **Command Execution**: 0.8 seconds per command (0.5s without ESC)
2. **LISP Loading**: 4.5 seconds per file, 45 seconds for full initialization
3. **Sequential Operations**: Each drawing operation is sent individually

## Optimization Strategies

### 1. Use Batch Operations (80% Speed Improvement)

Instead of creating 10 lines individually (8 seconds):
```python
# Slow approach - 10 separate calls
for i in range(10):
    create_line(x1[i], y1[i], x2[i], y2[i])  # 0.8s each = 8s total

# Fast approach - 1 batch call
batch_create_lines([[x1[0], y1[0], x2[0], y2[0]], 
                    [x1[1], y1[1], x2[1], y2[1]], ...])  # 0.8s total
```

### 2. Use the Fast Server Version

The `server_lisp_fast.py` provides:
- Minimal delays (0.05s instead of 0.2s)
- Batch operations support
- Clipboard-based script execution
- Fast initialization (loads only essential files)

To use:
```json
{
  "autocad-mcp": {
    "command": "python",
    "args": ["path\\to\\autocad-mcp\\server_lisp_fast.py"]
  }
}
```

### 3. Optimization Techniques by Use Case

#### Drawing Multiple Similar Objects
Use batch operations:
- `batch_create_lines()` - Create multiple lines at once
- `batch_create_circles()` - Create multiple circles at once
- `batch_create_texts()` - Create multiple text entities at once

#### Complex Drawings
Use batch operations or custom AutoLISP:
```python
# Option 1: Batch operations (recommended)
batch_create_lines([[0, 0, 100, 0], [100, 0, 100, 100]])
batch_create_circles([[50, 50, 25], [150, 50, 25]])

# Option 2: Custom AutoLISP for single operations
execute_custom_autolisp('(command "_CIRCLE" (list 50 50 0) 25)')
```

#### Performance Settings
Adjust delays based on your system:
```python
# For fast systems
set_performance_mode(fast_mode=True, minimal_delay=0.03, normal_delay=0.05)

# For slower systems or reliability
set_performance_mode(fast_mode=False, minimal_delay=0.1, normal_delay=0.2)
```

### 4. Best Practices for Speed

1. **Group Related Operations**
   - Plan your drawing sequence
   - Batch similar operations together
   - Use layers to organize elements

2. **Minimize State Changes**
   - Set layer once, draw multiple objects
   - Group objects by color/linetype
   - Reduce layer switching

3. **Use Batch Operations**
   - For multiple similar objects, use batch tools
   - `batch_create_lines()`, `batch_create_circles()`, etc.
   - Eliminates multiple round-trips

4. **Optimize Initialization**
   - Add frequently used LISP files to trusted paths
   - Use fast initialization (only essential files)
   - Load additional functions on-demand

### 5. Performance Comparison

| Operation | Original Time | Optimized Time | Improvement |
|-----------|--------------|----------------|-------------|
| Create 10 lines | 8.0s | 0.8s | 90% faster |
| Create 20 circles | 16.0s | 0.8s | 95% faster |
| Complex drawing (50 ops) | 40.0s | 2-3s | 93% faster |
| Server initialization | 45.0s | 5-10s | 78% faster |

### 6. Advanced Optimizations

#### Pre-compiled Drawing Functions
Create custom LISP functions for common patterns:
```lisp
(defun c:draw-grid (rows cols spacing)
  ; Draws a grid pattern efficiently
  ...)
```

#### Memory-based Operations
Use selection sets and entity manipulation instead of recreating:
```lisp
(defun c:copy-pattern (base-point pattern-points)
  ; Copies objects to multiple locations efficiently
  ...)
```

#### Asynchronous Preparation
Prepare complex LISP code while user is working:
- Generate LISP scripts in background
- Queue operations for batch execution
- Use clipboard for large data transfers

### 7. Troubleshooting Performance

If drawings are still slow:
1. Check AutoCAD's WHIPTHREAD setting (should be 3)
2. Disable unnecessary AutoCAD features (grids, snaps)
3. Use QSAVE instead of SAVE for faster saves
4. Monitor Windows Focus Assist settings
5. Close other applications that might interfere

### 8. Example: Fast Floor Plan

Instead of 100+ individual operations:
```python
# Generate complete floor plan in one script
floor_plan_script = generate_floor_plan_lisp(
    walls=wall_coords,
    doors=door_positions,
    windows=window_positions,
    dimensions=dim_points
)
execute_lisp_script(floor_plan_script)  # Single execution
```

This approach reduces a 2-minute drawing to under 10 seconds.