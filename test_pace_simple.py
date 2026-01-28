#!/usr/bin/env python3
"""
Test pace parsing functions
"""

import re
from typing import Optional, Dict, Any

def parse_pace(text: str) -> Optional[float]:
    """Parse pace from text (e.g., "4:50/km" -> 290 seconds per km)"""
    pace_pattern = r'(\d+):(\d+)\s*/?k(?:m)?'
    match = re.search(pace_pattern, text)
    
    if match:
        minutes = int(match.group(1))
        seconds = int(match.group(2))
        pace_seconds = minutes * 60 + seconds
        return float(pace_seconds)
    
    return None

def format_pace(seconds: float) -> str:
    """Format pace in seconds to MM:SS format"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"

def pace_to_zone_range(pace_seconds: float) -> tuple:
    """Convert pace to zone range for recovery/easy efforts"""
    # Z1: slow recovery (add 1:00 to 2:30)
    z1_min = pace_seconds + 60
    z1_max = pace_seconds + 150
    
    # Z2-Z3: easy to moderate (subtract 0:30, add 2:30)
    z2_z3_min = max(pace_seconds - 30, pace_seconds * 0.9)
    z2_z3_max = pace_seconds + 150
    
    return (z1_min, z1_max, z2_z3_min, z2_z3_max)

print("=" * 80)
print("Testing Pace Parsing and Conversion")
print("=" * 80)
print()

# Test cases
test_cases = [
    "1km at 4:50/km",
    "200m at 4:20/km",
    "3km warm up at conversational pace",
    "120s walking rest",
    "2.2km cool down"
]

print("Test 1: Pace Parsing")
print("-" * 80)
for text in test_cases:
    pace = parse_pace(text)
    if pace:
        print(f"✓ '{text}' -> {format_pace(pace)}/km ({pace:.0f} seconds)")
    else:
        print(f"✗ '{text}' -> No pace found")
print()

print("Test 2: Expected K200s Workout Structure")
print("-" * 80)
print()

workout_parts = [
    ("Warm-up", "3km", None, "easy"),
    ("Strides", "3x15s", None, "fast"),
    ("Rest", "90s", None, "recovery"),
    ("Main 1km", "1km", 4*60+50, "threshold"),
    ("Main 200m", "200m", 4*60+20, "interval"),
    ("Recovery", "120s", 4*60+50, "recovery"),
    ("Cool-down", "2.2km", None, "easy")
]

for name, distance, pace_sec, effort in workout_parts:
    print(f"{name:15} {distance:8}", end="")
    
    if pace_sec:
        pace_str = format_pace(pace_sec)
        
        if effort == "recovery":
            z1_min, z1_max, _, _ = pace_to_zone_range(pace_sec)
            print(f" Z1 {format_pace(z1_min)}-{format_pace(z1_max)}/km", end="")
        elif effort == "easy":
            _, _, z2_z3_min, z2_z3_max = pace_to_zone_range(pace_sec)
            print(f" Z1-Z3 {format_pace(z2_z3_min)}-{format_pace(z2_z3_max)}/km", end="")
        else:
            print(f" {pace_str}/km", end="")
    else:
        if effort == "recovery":
            print(f" Z1 (recovery)", end="")
        elif effort == "easy":
            print(f" Z1-Z3 (easy)", end="")
        else:
            print(f" {effort}", end="")
    
    print()

print()
print("=" * 80)
print("Expected intervals.icu Output Format:")
print("=" * 80)
print()
print("Main Set 4x")
print("  * 1km at 4:50/km Pace")
print("  * 0.2km at 4:20/km Pace")
print("  * 120s Z1 6:50-8:23/km (for 0.26km)")
print()
print("Cool-down:")
print("  * 2.2km Z1-Z3 5:20-8:23/km")
print()
print("=" * 80)
print("✓ Test Complete!")
print("=" * 80)
