# Pace Targets System

This document explains how the converter handles pace targets for intervals.icu.

## Overview

The converter uses **actual pace targets** rather than perceived effort zones. This provides more precise workout guidance and better matches how Runna structures workouts.

## Pace Parsing

### Supported Formats

The converter recognizes these pace formats:
- `4:50/km` - Standard format
- `4:50 /km` - With space
- `4:50/k` - Short format
- `4:50km` - No slash

### Examples

```python
"1km at 4:50/km"     → 290 seconds/km
"200m at 4:20/km"    → 260 seconds/km
"15s at 3:45/km"     → 225 seconds/km
```

## Pace Target Types

### 1. Specific Pace (Work Intervals)

Used for main work intervals with explicit paces.

**Runna Format:**
```
• 1km at 4:50/km
• 200m at 4:20/km
```

**intervals.icu Output:**
```json
{
  "distance": 1000,
  "durationType": "distance",
  "targetType": "pace",
  "pace": 290,
  "paceType": "target",
  "text": "1km at 4:50/km"
}
```

**Display:**
- `1km @ 4:50/km Pace`

### 2. Z1 Recovery Range (Rest/Recovery)

Used for rest periods and recovery jogs.

**Calculation:**
- Based on workout pace (e.g., 4:50/km = 290 sec)
- Add 1:00 to 2:30 (60-150 seconds)
- Z1 Range: 5:50/km to 7:20/km

**Runna Format:**
```
• 120s walking rest
• 2min recovery jog
```

**intervals.icu Output:**
```json
{
  "duration": 120,
  "durationType": "time",
  "targetType": "pace",
  "pace": null,
  "paceMin": 350,
  "paceMax": 440,
  "paceType": "range",
  "text": "120s walking rest (5:50-7:20/km Z1)"
}
```

**Display:**
- `120s Z1 5:50-7:20/km (0.26km)`

### 3. Z1-Z3 Easy Range (Warm-up/Cool-down)

Used for warm-ups, cool-downs, and easy running.

**Calculation:**
- Based on workout pace (e.g., 4:50/km = 290 sec)
- Range: -30 seconds to +150 seconds
- Z1-Z3 Range: 4:20/km to 7:20/km

**Runna Format:**
```
• 3km warm up at conversational pace
• 2.2km cool down at a conversational pace
```

**intervals.icu Output:**
```json
{
  "distance": 3000,
  "durationType": "distance",
  "targetType": "pace",
  "pace": null,
  "paceMin": 260,
  "paceMax": 440,
  "paceType": "range",
  "text": "3km warm up (4:20-7:20/km Z1-Z3)"
}
```

**Display:**
- `3km Z1-Z3 4:20-7:20/km`

## Complete Workout Example

### Runna Workout (K200s)

```
3km warm up at a conversational pace, add 3x 15s fast bursts

4 reps of:
• 1km at 4:50/km
• 200m at 4:20/km, 120s walking rest

2.2km cool down at a conversational pace
```

### intervals.icu Conversion

```
Warm-up:
  * 3km Z1-Z3 Pace (5:37-8:33/km)

Strides: 3x
  * 15s @ 4:20/km Pace
  * 20s Easy (5:20-6:50/km)

Rest:
  * 90s Z1 Pace (5:50-8:33/km for 0.26km)

Main Set: 4x
  * 1km @ 4:50/km Pace
  * 0.2km @ 4:20/km Pace
  * 120s Z1 Pace (5:50-7:20/km for 0.26km)

Cool-down:
  * 2.2km Z1-Z3 Pace (4:20-7:20/km)
```

## Pace Calculation Formulas

### Z1 Recovery Range

```python
workout_pace = 290  # 4:50/km in seconds

z1_min = workout_pace + 60   # Add 1:00
z1_max = workout_pace + 150  # Add 2:30

# Result: 5:50/km to 7:20/km
```

### Z1-Z3 Easy Range

```python
workout_pace = 290  # 4:50/km in seconds

z2_z3_min = max(workout_pace - 30, workout_pace * 0.9)  # -0:30 or 90%
z2_z3_max = workout_pace + 150  # Add 2:30

# Result: 4:20/km to 7:20/km
```

### Distance Covered During Timed Recovery

```python
rest_duration = 120  # seconds
pace_avg = (z1_min + z1_max) / 2  # Average recovery pace

distance = rest_duration / pace_avg * 1000  # meters

# For 120s at 6:35/km avg: ~260m
```

## Workout Type Detection

### How the Converter Determines Type

**Recovery/Rest:**
- Contains: "recovery", "rest", "walking", "jog recovery"
- Gets Z1 recovery range

**Easy/Warm-up/Cool-down:**
- Contains: "warm up", "cool down", "easy", "conversational"
- Position: First or last segments
- Gets Z1-Z3 easy range

**Work Intervals:**
- Has specific pace (e.g., "4:50/km")
- Contains: "at", "@", "tempo", "threshold"
- Gets target pace

**Fast Bursts/Strides:**
- Contains: "fast", "stride", "burst", "surge"
- Short duration (typically <30s)
- Gets target pace if specified, otherwise interval intensity

## Benefits of Pace-Based Approach

✅ **More Precise:** Actual paces instead of vague zones
✅ **Runna-Compatible:** Matches how Runna structures workouts
✅ **Auto-Calculated:** Recovery ranges calculated from workout pace
✅ **Flexible:** Handles both specific and general descriptions
✅ **intervals.icu Native:** Uses intervals.icu's pace target system

## Fallback Behavior

If no pace can be parsed:
- Recovery: Defaults to Z1 zone
- Easy: Defaults to Z2 zone
- Work: Defaults to Z3 zone

This ensures every workout has appropriate guidance even without explicit paces.

## API Format

The intervals.icu API expects pace in seconds per kilometer:

```json
{
  "targetType": "pace",
  "pace": 290,           // 4:50/km (exact target)
  "paceType": "target"
}
```

Or for ranges:

```json
{
  "targetType": "pace",
  "pace": null,
  "paceMin": 350,        // 5:50/km (slowest)
  "paceMax": 440,        // 7:20/km (fastest)
  "paceType": "range"
}
```

## Testing

Test the pace parsing:

```bash
python3 test_pace_simple.py
```

This will show:
- Pace parsing from different formats
- Zone range calculations
- Expected output for each workout type

## Customization

To adjust zone ranges, modify in `runna_to_intervals.py`:

```python
def pace_to_zone_range(self, pace_seconds: float) -> tuple:
    # Adjust these values:
    z1_min = pace_seconds + 60   # Change recovery offset
    z1_max = pace_seconds + 150  # Change recovery range
    
    z2_z3_min = max(pace_seconds - 30, pace_seconds * 0.9)
    z2_z3_max = pace_seconds + 150
    
    return (z1_min, z1_max, z2_z3_min, z2_z3_max)
```

## Common Patterns

### Pattern 1: Interval Session
```
Runna: "5x(1km at 4:50/km, 2min recovery)"
Output:
  5x
    - 1km @ 4:50/km
    - 2min Z1 5:50-7:20/km
```

### Pattern 2: Tempo Run
```
Runna: "10min warm up, 20min at 4:45/km, 10min cool down"
Output:
  - 10min Z1-Z3 4:15-7:15/km
  - 20min @ 4:45/km
  - 10min Z1-Z3 4:15-7:15/km
```

### Pattern 3: Progressive Run
```
Runna: "3km at 5:30/km, 3km at 5:00/km, 3km at 4:30/km"
Output:
  - 3km @ 5:30/km
  - 3km @ 5:00/km
  - 3km @ 4:30/km
```

## Troubleshooting

**Issue:** Pace not detected
```bash
# Enable debug logging
python3 runna_to_intervals.py --log-level DEBUG

# Look for "Parsed pace" messages
```

**Issue:** Incorrect range calculations
```bash
# Check the pace_to_zone_range function
# Verify workout has base pace to calculate from
```

**Issue:** Wrong workout type assigned
```bash
# Check keyword detection in convert_to_intervals_icu
# Look for "is_recovery" and "is_easy" logic
```

---

**This pace-based system provides precise, actionable workout guidance that matches Runna's training methodology!**
