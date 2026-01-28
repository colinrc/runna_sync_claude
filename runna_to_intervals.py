#!/usr/bin/env python3
"""
Runna to Intervals.icu Workout Converter

This script reads a calendar ICS file from an HTTP location containing Runna workouts,
parses each workout, and converts them to intervals.icu workout format.

Can be run from:
- Command line/shell
- Cloudflare Workers (via scheduled trigger)
- Any Python environment
"""

import requests
from icalendar import Calendar
import re
import json
import logging
import sys
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum


class LogLevel(Enum):
    """Log level enumeration"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class StructuredLogger:
    """
    Structured logger compatible with Cloudflare Workers and standard logging
    Outputs JSON-formatted logs for easy parsing in cloud environments
    """
    
    def __init__(self, level: str = "INFO", use_json: bool = True):
        """
        Initialize structured logger
        
        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR)
            use_json: Whether to output JSON-formatted logs
        """
        self.level = LogLevel[level.upper()]
        self.use_json = use_json
        self._level_priority = {
            LogLevel.DEBUG: 0,
            LogLevel.INFO: 1,
            LogLevel.WARNING: 2,
            LogLevel.ERROR: 3
        }
    
    def _should_log(self, level: LogLevel) -> bool:
        """Check if message should be logged based on current level"""
        return self._level_priority[level] >= self._level_priority[self.level]
    
    def _log(self, level: LogLevel, message: str, **kwargs):
        """Internal log method"""
        if not self._should_log(level):
            return
        
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level.value,
            "message": message,
            **kwargs
        }
        
        if self.use_json:
            print(json.dumps(log_data), file=sys.stderr)
        else:
            extra_info = " ".join(f"{k}={v}" for k, v in kwargs.items() if k != "timestamp")
            log_line = f"[{log_data['timestamp']}] {level.value}: {message}"
            if extra_info:
                log_line += f" | {extra_info}"
            print(log_line, file=sys.stderr)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self._log(LogLevel.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self._log(LogLevel.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self._log(LogLevel.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self._log(LogLevel.ERROR, message, **kwargs)


class IntervalsICUAPI:
    """
    Intervals.icu API client for uploading workouts
    API Documentation: https://intervals.icu/api/
    """
    
    def __init__(self, athlete_id: str, api_key: str, logger: Optional[StructuredLogger] = None):
        """
        Initialize intervals.icu API client
        
        Args:
            athlete_id: Your intervals.icu athlete ID (e.g., 'i12345')
            api_key: Your API key from intervals.icu settings
            logger: Optional structured logger
        """
        self.athlete_id = athlete_id
        self.api_key = api_key
        self.base_url = "https://intervals.icu/api/v1"
        self.logger = logger or StructuredLogger()
        
        # Setup authentication
        self.session = requests.Session()
        self.session.auth = (f"API_KEY", api_key)
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
    
    def create_workout(self, workout: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a workout in intervals.icu
        
        Args:
            workout: Workout dictionary in intervals.icu format
            
        Returns:
            Created workout response or None on failure
        """
        url = f"{self.base_url}/athlete/{self.athlete_id}/workouts"
        
        self.logger.info("Creating workout in intervals.icu", 
                        name=workout.get('name'),
                        date=workout.get('workout_date'))
        
        try:
            response = self.session.post(url, json=workout)
            response.raise_for_status()
            
            result = response.json()
            self.logger.info("Workout created successfully", 
                           workout_id=result.get('id'),
                           name=workout.get('name'))
            return result
        
        except requests.exceptions.HTTPError as e:
            self.logger.error("Failed to create workout",
                            status_code=e.response.status_code,
                            error=str(e),
                            response=e.response.text)
            return None
        except Exception as e:
            self.logger.error("Unexpected error creating workout", error=str(e))
            return None
    
    def update_workout(self, workout_id: str, workout: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing workout
        
        Args:
            workout_id: ID of workout to update
            workout: Updated workout data
            
        Returns:
            Updated workout response or None on failure
        """
        url = f"{self.base_url}/athlete/{self.athlete_id}/workouts/{workout_id}"
        
        self.logger.info("Updating workout", workout_id=workout_id)
        
        try:
            response = self.session.put(url, json=workout)
            response.raise_for_status()
            
            result = response.json()
            self.logger.info("Workout updated successfully", workout_id=workout_id)
            return result
        
        except requests.exceptions.HTTPError as e:
            self.logger.error("Failed to update workout",
                            workout_id=workout_id,
                            status_code=e.response.status_code,
                            error=str(e))
            return None
        except Exception as e:
            self.logger.error("Unexpected error updating workout", error=str(e))
            return None
    
    def get_workouts(self, start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
        """
        Get workouts for date range
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            List of workouts
        """
        url = f"{self.base_url}/athlete/{self.athlete_id}/workouts"
        params = {}
        if start_date:
            params['oldest'] = start_date
        if end_date:
            params['newest'] = end_date
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error("Failed to get workouts", error=str(e))
            return []
    
    def delete_workout(self, workout_id: str) -> bool:
        """
        Delete a workout
        
        Args:
            workout_id: ID of workout to delete
            
        Returns:
            True if successful, False otherwise
        """
        url = f"{self.base_url}/athlete/{self.athlete_id}/workouts/{workout_id}"
        
        try:
            response = self.session.delete(url)
            response.raise_for_status()
            self.logger.info("Workout deleted successfully", workout_id=workout_id)
            return True
        except Exception as e:
            self.logger.error("Failed to delete workout", workout_id=workout_id, error=str(e))
            return False


class RunnaWorkoutConverter:
    """Converts Runna workouts to intervals.icu format"""
    
    # Pace/intensity mappings
    INTENSITY_MAP = {
        'easy': 1,
        'moderate': 2,
        'steady': 3,
        'tempo': 4,
        'threshold': 5,
        'interval': 6,
        'vo2max': 7,
        'race pace': 4,
        'marathon pace': 4,
        'half marathon pace': 5,
        '10k pace': 6,
        '5k pace': 7,
    }
    
    def __init__(self, ics_url: str, logger: Optional[StructuredLogger] = None, 
                 api_client: Optional[IntervalsICUAPI] = None):
        """
        Initialize converter with ICS URL
        
        Args:
            ics_url: HTTP URL to the ICS calendar file
            logger: Optional structured logger instance
            api_client: Optional intervals.icu API client for direct upload
        """
        self.ics_url = ics_url
        self.workouts = []
        self.logger = logger or StructuredLogger()
        self.api_client = api_client
    
    def fetch_calendar(self) -> Calendar:
        """
        Fetch ICS calendar from HTTP location
        
        Returns:
            Calendar object
        """
        self.logger.info("Fetching calendar", url=self.ics_url)
        
        try:
            response = requests.get(self.ics_url, timeout=30)
            response.raise_for_status()
            
            self.logger.debug("Calendar fetched successfully", 
                            status_code=response.status_code,
                            content_length=len(response.content))
            
            cal = Calendar.from_ical(response.content)
            return cal
        except requests.RequestException as e:
            self.logger.error("Failed to fetch calendar", error=str(e), url=self.ics_url)
            raise
    
    def parse_duration(self, duration_text: str) -> int:
        """
        Parse duration text to seconds
        
        Args:
            duration_text: Duration string (e.g., "30min", "1h 15min", "45 minutes")
            
        Returns:
            Duration in seconds
        """
        duration_text = duration_text.lower().strip()
        total_seconds = 0
        
        # Match hours
        hours_match = re.search(r'(\d+)\s*h(?:our)?s?', duration_text)
        if hours_match:
            total_seconds += int(hours_match.group(1)) * 3600
        
        # Match minutes
        minutes_match = re.search(r'(\d+)\s*m(?:in)?(?:ute)?s?', duration_text)
        if minutes_match:
            total_seconds += int(minutes_match.group(1)) * 60
        
        # Match seconds
        seconds_match = re.search(r'(\d+)\s*s(?:ec)?(?:ond)?s?', duration_text)
        if seconds_match:
            total_seconds += int(seconds_match.group(1))
        
        result = total_seconds if total_seconds > 0 else 1800  # Default 30 min
        self.logger.debug("Parsed duration", text=duration_text, seconds=result)
        return result
    
    def parse_distance(self, distance_text: str) -> float:
        """
        Parse distance text to meters
        
        Args:
            distance_text: Distance string (e.g., "5km", "10k", "400m")
            
        Returns:
            Distance in meters
        """
        distance_text = distance_text.lower().strip()
        
        # Match kilometers
        km_match = re.search(r'(\d+\.?\d*)\s*k(?:m)?', distance_text)
        if km_match:
            return float(km_match.group(1)) * 1000
        
        # Match miles
        mile_match = re.search(r'(\d+\.?\d*)\s*mi(?:le)?s?', distance_text)
        if mile_match:
            return float(mile_match.group(1)) * 1609.34
        
        # Match meters
        meter_match = re.search(r'(\d+)\s*m(?:eter)?s?', distance_text)
        if meter_match:
            return float(meter_match.group(1))
        
        return 0
    
    def extract_intensity(self, text: str) -> int:
        """
        Extract intensity/pace from workout description
        
        Args:
            text: Workout description text
            
        Returns:
            Intensity level (1-7)
        """
        text_lower = text.lower()
        
        for pace_key, intensity in self.INTENSITY_MAP.items():
            if pace_key in text_lower:
                self.logger.debug("Matched intensity", pace=pace_key, level=intensity)
                return intensity
        
        # Default to moderate
        self.logger.debug("Using default intensity", level=2)
        return 2
    
    def parse_workout_description(self, description: str, summary: str) -> List[Dict[str, Any]]:
        """
        Parse workout description into intervals
        
        Args:
            description: Full workout description
            summary: Workout summary/title
            
        Returns:
            List of interval dictionaries
        """
        self.logger.debug("Parsing workout", summary=summary)
        intervals = []
        
        # Common patterns in Runna workouts
        # Example: "Warm up 10min easy, 5x(1km @ tempo, 2min recovery), Cool down 10min easy"
        
        lines = description.split('\n')
        text = ' '.join(lines)
        
        # Try to find structured intervals
        # Pattern: Number x (duration/distance @ intensity, rest)
        interval_pattern = r'(\d+)\s*x\s*\(([^)]+)\)'
        matches = re.finditer(interval_pattern, text, re.IGNORECASE)
        
        has_structured_intervals = False
        for match in matches:
            has_structured_intervals = True
            reps = int(match.group(1))
            interval_text = match.group(2)
            
            self.logger.debug("Found structured interval", reps=reps, text=interval_text)
            
            # Parse the interval components
            parts = re.split(r',|and', interval_text)
            
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                
                duration = self.parse_duration(part) if 'min' in part or 'hour' in part else 0
                distance = self.parse_distance(part) if 'km' in part or 'm' in part or 'k ' in part else 0
                intensity = self.extract_intensity(part)
                
                if 'recovery' in part.lower() or 'rest' in part.lower():
                    interval_type = 'recovery'
                    intensity = 1
                else:
                    interval_type = 'work'
                
                intervals.append({
                    'repeat': reps,
                    'duration': duration,
                    'distance': distance,
                    'intensity': intensity,
                    'type': interval_type,
                    'text': part
                })
        
        # If no structured intervals found, create a simple workout
        if not has_structured_intervals:
            self.logger.debug("No structured intervals found, creating simple workout")
            
            # Look for warm up
            warmup_match = re.search(r'warm\s*up\s+(\d+(?:\s*min)?)', text, re.IGNORECASE)
            if warmup_match:
                duration = self.parse_duration(warmup_match.group(1))
                intervals.append({
                    'repeat': 1,
                    'duration': duration,
                    'distance': 0,
                    'intensity': 1,
                    'type': 'warmup',
                    'text': 'Warm up'
                })
            
            # Main work
            main_intensity = self.extract_intensity(text)
            main_duration = self.parse_duration(summary) if 'min' in summary else 1800
            intervals.append({
                'repeat': 1,
                'duration': main_duration,
                'distance': 0,
                'intensity': main_intensity,
                'type': 'work',
                'text': summary
            })
            
            # Look for cool down
            cooldown_match = re.search(r'cool\s*down\s+(\d+(?:\s*min)?)', text, re.IGNORECASE)
            if cooldown_match:
                duration = self.parse_duration(cooldown_match.group(1))
                intervals.append({
                    'repeat': 1,
                    'duration': duration,
                    'distance': 0,
                    'intensity': 1,
                    'type': 'cooldown',
                    'text': 'Cool down'
                })
        
        self.logger.info("Parsed workout intervals", summary=summary, interval_count=len(intervals))
        return intervals
    
    def convert_to_intervals_icu(self, event) -> Dict[str, Any]:
        """
        Convert a calendar event to intervals.icu workout format
        
        Args:
            event: iCalendar event object
            
        Returns:
            Dictionary in intervals.icu workout format
        """
        summary = str(event.get('summary', 'Runna Workout'))
        description = str(event.get('description', ''))
        start_date = event.get('dtstart').dt if event.get('dtstart') else datetime.now()
        
        self.logger.debug("Converting event to intervals.icu format", summary=summary)
        
        # Parse intervals from description
        intervals = self.parse_workout_description(description, summary)
        
        # Build intervals.icu workout format
        workout = {
            'name': summary,
            'description': description,
            'workout_date': start_date.strftime('%Y-%m-%d') if isinstance(start_date, datetime) else str(start_date),
            'steps': []
        }
        
        # Convert intervals to steps
        for interval in intervals:
            step = {
                'repeat': interval['repeat'],
                'steps': []
            }
            
            # Determine step type
            if interval['duration'] > 0:
                step_data = {
                    'duration': interval['duration'],
                    'durationType': 'time',
                    'targetType': 'pace',
                    'target': interval['intensity'],
                    'text': interval['text']
                }
            elif interval['distance'] > 0:
                step_data = {
                    'distance': interval['distance'],
                    'durationType': 'distance',
                    'targetType': 'pace',
                    'target': interval['intensity'],
                    'text': interval['text']
                }
            else:
                # Default to time-based
                step_data = {
                    'duration': 1800,
                    'durationType': 'time',
                    'targetType': 'pace',
                    'target': interval['intensity'],
                    'text': interval['text']
                }
            
            if interval['repeat'] > 1:
                step['steps'].append(step_data)
                workout['steps'].append(step)
            else:
                workout['steps'].append(step_data)
        
        return workout
    
    def process_calendar(self, upload_to_api: bool = False) -> List[Dict[str, Any]]:
        """
        Process entire calendar and convert all workouts
        
        Args:
            upload_to_api: If True and api_client is set, upload workouts directly to intervals.icu
        
        Returns:
            List of intervals.icu workout dictionaries
        """
        self.logger.info("Starting calendar processing", upload_to_api=upload_to_api)
        
        cal = self.fetch_calendar()
        workouts = []
        event_count = 0
        uploaded_count = 0
        
        for component in cal.walk():
            if component.name == "VEVENT":
                event_count += 1
                summary = str(component.get('summary', ''))
                
                # Filter for Runna workouts (adjust this filter as needed)
                if 'run' in summary.lower() or 'workout' in summary.lower():
                    workout = self.convert_to_intervals_icu(component)
                    workouts.append(workout)
                    self.logger.info("Converted workout", 
                                   name=workout['name'], 
                                   date=workout['workout_date'],
                                   steps=len(workout['steps']))
                    
                    # Upload to API if requested
                    if upload_to_api and self.api_client:
                        result = self.api_client.create_workout(workout)
                        if result:
                            uploaded_count += 1
        
        self.workouts = workouts
        
        if upload_to_api and self.api_client:
            self.logger.info("Calendar processing complete with API upload", 
                            total_events=event_count,
                            workouts_converted=len(workouts),
                            workouts_uploaded=uploaded_count)
        else:
            self.logger.info("Calendar processing complete", 
                            total_events=event_count,
                            workouts_converted=len(workouts))
        
        return workouts
    
    def save_workouts(self, output_file: str = 'intervals_icu_workouts.json'):
        """
        Save converted workouts to JSON file
        
        Args:
            output_file: Output filename
        """
        self.logger.info("Saving workouts", filename=output_file, count=len(self.workouts))
        
        with open(output_file, 'w') as f:
            json.dump(self.workouts, f, indent=2)
        
        self.logger.info("Workouts saved successfully", filename=output_file)


# ============================================================================
# Cloudflare Worker Handler
# ============================================================================

async def cloudflare_scheduled_handler(event, env, ctx):
    """
    Cloudflare Workers scheduled event handler
    
    This function is called by Cloudflare Workers cron trigger.
    
    Environment variables expected:
    - ICS_URL: URL to the Runna calendar ICS file
    - OUTPUT_PATH: (Optional) Path to save output JSON
    - LOG_LEVEL: (Optional) Logging level (DEBUG, INFO, WARNING, ERROR)
    - LOG_JSON: (Optional) Use JSON logging (true/false)
    
    Args:
        event: Cloudflare scheduled event
        env: Environment variables
        ctx: Execution context
    """
    # Get configuration from environment variables
    ics_url = env.get('ICS_URL')
    output_path = env.get('OUTPUT_PATH', 'intervals_icu_workouts.json')
    log_level = env.get('LOG_LEVEL', 'INFO')
    log_json = env.get('LOG_JSON', 'true').lower() == 'true'
    
    # Initialize logger
    logger = StructuredLogger(level=log_level, use_json=log_json)
    
    logger.info("Cloudflare scheduled handler triggered", 
                cron=event.cron if hasattr(event, 'cron') else 'unknown')
    
    if not ics_url:
        logger.error("ICS_URL environment variable not set")
        return {
            'success': False,
            'error': 'ICS_URL environment variable not set'
        }
    
    try:
        # Run conversion
        converter = RunnaWorkoutConverter(ics_url, logger=logger)
        workouts = converter.process_calendar()
        
        # Save workouts
        converter.save_workouts(output_path)
        
        logger.info("Scheduled conversion completed successfully",
                   workouts_processed=len(workouts))
        
        return {
            'success': True,
            'workouts_processed': len(workouts),
            'output_file': output_path
        }
    
    except Exception as e:
        logger.error("Scheduled conversion failed", 
                    error=str(e),
                    error_type=type(e).__name__)
        return {
            'success': False,
            'error': str(e)
        }


def cloudflare_fetch_handler(request, env, ctx):
    """
    Cloudflare Workers HTTP fetch handler
    
    Allows triggering conversion via HTTP request.
    
    Args:
        request: HTTP request object
        env: Environment variables
        ctx: Execution context
    """
    ics_url = env.get('ICS_URL')
    log_level = env.get('LOG_LEVEL', 'INFO')
    log_json = env.get('LOG_JSON', 'true').lower() == 'true'
    
    logger = StructuredLogger(level=log_level, use_json=log_json)
    logger.info("HTTP fetch handler triggered")
    
    if not ics_url:
        return Response(
            json.dumps({'success': False, 'error': 'ICS_URL not configured'}),
            status=500,
            headers={'Content-Type': 'application/json'}
        )
    
    try:
        converter = RunnaWorkoutConverter(ics_url, logger=logger)
        workouts = converter.process_calendar()
        
        return Response(
            json.dumps({
                'success': True,
                'workouts': workouts,
                'count': len(workouts)
            }),
            status=200,
            headers={'Content-Type': 'application/json'}
        )
    
    except Exception as e:
        logger.error("HTTP handler failed", error=str(e))
        return Response(
            json.dumps({'success': False, 'error': str(e)}),
            status=500,
            headers={'Content-Type': 'application/json'}
        )


# ============================================================================
# Shell/CLI Entry Point
# ============================================================================

def main():
    """Main execution function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Convert Runna workouts from ICS to intervals.icu format'
    )
    parser.add_argument(
        '--url',
        help='ICS calendar URL (or set ICS_URL environment variable)',
        default=os.environ.get('ICS_URL')
    )
    parser.add_argument(
        '--output',
        help='Output JSON file path',
        default='intervals_icu_workouts.json'
    )
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default=os.environ.get('LOG_LEVEL', 'INFO'),
        help='Logging level'
    )
    parser.add_argument(
        '--log-json',
        action='store_true',
        default=os.environ.get('LOG_JSON', 'false').lower() == 'true',
        help='Output logs in JSON format'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Prompt for URL if not provided'
    )
    parser.add_argument(
        '--api-upload',
        action='store_true',
        help='Upload workouts directly to intervals.icu via API'
    )
    parser.add_argument(
        '--athlete-id',
        help='intervals.icu athlete ID (or set INTERVALS_ATHLETE_ID env var)',
        default=os.environ.get('INTERVALS_ATHLETE_ID')
    )
    parser.add_argument(
        '--api-key',
        help='intervals.icu API key (or set INTERVALS_API_KEY env var)',
        default=os.environ.get('INTERVALS_API_KEY')
    )
    
    args = parser.parse_args()
    
    # Initialize logger
    logger = StructuredLogger(level=args.log_level, use_json=args.log_json)
    
    # Get ICS URL
    ics_url = args.url
    if not ics_url and args.interactive:
        ics_url = input("Enter the ICS calendar URL: ").strip()
    
    if not ics_url:
        logger.error("No ICS URL provided. Use --url or set ICS_URL environment variable")
        sys.exit(1)
    
    # Setup API client if credentials provided
    api_client = None
    if args.api_upload:
        if not args.athlete_id or not args.api_key:
            logger.error("API upload requires --athlete-id and --api-key")
            sys.exit(1)
        
        logger.info("Initializing intervals.icu API client", athlete_id=args.athlete_id)
        api_client = IntervalsICUAPI(args.athlete_id, args.api_key, logger)
    
    try:
        logger.info("Starting conversion", url=ics_url, api_upload=args.api_upload)
        
        converter = RunnaWorkoutConverter(ics_url, logger=logger, api_client=api_client)
        workouts = converter.process_calendar(upload_to_api=args.api_upload)
        
        if workouts:
            if args.api_upload:
                logger.info("Workouts uploaded to intervals.icu",
                           workouts=len(workouts))
                print(f"\n✅ Uploaded {len(workouts)} workouts to intervals.icu")
            else:
                converter.save_workouts(args.output)
                
                logger.info("Conversion completed successfully",
                           workouts=len(workouts),
                           output_file=args.output)
                
                # Print summary to stdout
                print(f"\nConverted {len(workouts)} workouts")
                print(f"Output saved to: {args.output}")
            
            if args.log_level == 'DEBUG':
                print("\n=== Sample Workout ===")
                print(json.dumps(workouts[0], indent=2))
        else:
            logger.warning("No workouts found in calendar")
            print("No workouts found in calendar")
    
    except Exception as e:
        logger.error("Conversion failed", error=str(e), error_type=type(e).__name__)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
