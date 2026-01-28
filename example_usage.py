#!/usr/bin/env python3
"""
Example usage of the Runna to Intervals.icu converter
Demonstrates how to use the converter with sample workout descriptions
"""

from runna_to_intervals import RunnaWorkoutConverter
from datetime import datetime
from icalendar import Calendar, Event
import json


def create_sample_ics_file():
    """Create a sample ICS file for testing"""
    cal = Calendar()
    cal.add('prodid', '-//Runna Training Calendar//example.com//')
    cal.add('version', '2.0')
    
    # Sample workouts
    workouts = [
        {
            'summary': 'Easy Run',
            'description': 'Easy run for 30 minutes at conversational pace',
            'date': datetime(2026, 1, 27)
        },
        {
            'summary': 'Interval Workout',
            'description': 'Warm up 10min easy, 5x(1km @ tempo, 2min recovery), Cool down 10min easy',
            'date': datetime(2026, 1, 28)
        },
        {
            'summary': 'Tempo Run',
            'description': 'Warm up 15min, 20min @ threshold pace, Cool down 10min',
            'date': datetime(2026, 1, 29)
        },
        {
            'summary': 'Long Run',
            'description': '90 minutes at easy to moderate pace',
            'date': datetime(2026, 1, 30)
        },
        {
            'summary': 'Speed Work',
            'description': 'Warm up 10min, 8x(400m @ 5K pace, 90sec recovery), Cool down 10min',
            'date': datetime(2026, 1, 31)
        }
    ]
    
    for workout in workouts:
        event = Event()
        event.add('summary', workout['summary'])
        event.add('description', workout['description'])
        event.add('dtstart', workout['date'])
        event.add('dtstamp', datetime.now())
        cal.add_component(event)
    
    # Save to file
    with open('/home/claude/sample_runna_calendar.ics', 'wb') as f:
        f.write(cal.to_ical())
    
    print("Created sample ICS file: sample_runna_calendar.ics")


def test_workout_parsing():
    """Test workout parsing with sample descriptions"""
    print("\n=== Testing Workout Parsing ===\n")
    
    # Create sample calendar
    create_sample_ics_file()
    
    # Test parsing individual workout descriptions
    converter = RunnaWorkoutConverter('http://example.com/dummy.ics')
    
    test_cases = [
        {
            'description': 'Warm up 10min easy, 5x(1km @ tempo, 2min recovery), Cool down 10min easy',
            'summary': 'Interval Workout'
        },
        {
            'description': 'Easy run for 30 minutes at conversational pace',
            'summary': 'Easy Run'
        },
        {
            'description': 'Warm up 15min, 20min @ threshold pace, Cool down 10min',
            'summary': 'Tempo Run'
        },
        {
            'description': '8x(400m @ 5K pace, 90sec recovery)',
            'summary': 'Speed Work'
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test Case {i}: {test['summary']}")
        print(f"Description: {test['description']}")
        
        intervals = converter.parse_workout_description(
            test['description'], 
            test['summary']
        )
        
        print(f"Parsed {len(intervals)} intervals:")
        for j, interval in enumerate(intervals, 1):
            print(f"  {j}. {interval['text']}")
            print(f"     - Repeat: {interval['repeat']}x")
            print(f"     - Duration: {interval['duration']}s")
            print(f"     - Intensity: {interval['intensity']}")
            print(f"     - Type: {interval['type']}")
        print()


def example_convert_from_url():
    """Example of converting from a real URL (would need actual URL)"""
    print("\n=== Example: Convert from URL ===\n")
    print("To use this with a real Runna calendar:")
    print("1. Get your Runna calendar ICS URL")
    print("2. Run the converter:")
    print()
    print("  converter = RunnaWorkoutConverter('https://your-calendar-url.ics')")
    print("  workouts = converter.process_calendar()")
    print("  converter.save_workouts('my_runna_workouts.json')")
    print()


def example_custom_intensity_mapping():
    """Example of customizing intensity mappings"""
    print("\n=== Example: Custom Intensity Mapping ===\n")
    
    # Create custom converter
    converter = RunnaWorkoutConverter('http://example.com/dummy.ics')
    
    # Modify intensity map
    converter.INTENSITY_MAP['marathon pace'] = 3  # Change from 4 to 3
    converter.INTENSITY_MAP['lactate threshold'] = 5
    converter.INTENSITY_MAP['zone 2'] = 2
    
    print("Custom intensity mappings added:")
    for pace, intensity in converter.INTENSITY_MAP.items():
        print(f"  {pace}: {intensity}")


def example_intervals_icu_format():
    """Show example of intervals.icu format output"""
    print("\n=== Example: Intervals.icu Format ===\n")
    
    sample_workout = {
        "name": "Tempo Run",
        "description": "Warm up 10min easy, 20min @ tempo, Cool down 10min easy",
        "workout_date": "2026-01-27",
        "steps": [
            {
                "duration": 600,
                "durationType": "time",
                "targetType": "pace",
                "target": 1,
                "text": "Warm up"
            },
            {
                "duration": 1200,
                "durationType": "time",
                "targetType": "pace",
                "target": 4,
                "text": "Tempo"
            },
            {
                "duration": 600,
                "durationType": "time",
                "targetType": "pace",
                "target": 1,
                "text": "Cool down"
            }
        ]
    }
    
    print("Sample intervals.icu workout format:")
    print(json.dumps(sample_workout, indent=2))
    print()
    print("This can be imported into intervals.icu or used with their API")


def main():
    """Run all examples"""
    print("=" * 60)
    print("Runna to Intervals.icu Converter - Examples")
    print("=" * 60)
    
    # Run examples
    test_workout_parsing()
    example_convert_from_url()
    example_custom_intensity_mapping()
    example_intervals_icu_format()
    
    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
