"""
Cloudflare Workers Entry Point for Runna to Intervals.icu Converter

This file demonstrates how to integrate the converter with Cloudflare Workers.
For Python-based Cloudflare Workers, this would be adapted to the Workers runtime.

Note: Cloudflare Workers primarily support JavaScript/TypeScript. For Python,
you would need to use a Python-compatible runtime like:
- Pyodide (WebAssembly Python)
- External service triggered by the worker
- Cloudflare Pages Functions (which support Python)

This example shows the structure for reference.
"""

# For actual Cloudflare Workers deployment, you would typically:
# 1. Use the Python script as a scheduled task on a server
# 2. Or create a JavaScript wrapper that calls a Python service
# 3. Or use Cloudflare Durable Objects with external Python processing

# Example JavaScript wrapper (save as index.js for actual deployment):
"""
export default {
  async scheduled(event, env, ctx) {
    // Cloudflare Workers Scheduled Event Handler
    const icsUrl = env.ICS_URL;
    const logLevel = env.LOG_LEVEL || 'INFO';
    
    console.log(`[${new Date().toISOString()}] Scheduled task triggered`);
    
    if (!icsUrl) {
      console.error('ICS_URL environment variable not set');
      return;
    }
    
    try {
      // Call your Python service endpoint or run Python code
      // Option 1: Call external Python service
      const response = await fetch('https://your-python-service.com/convert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ics_url: icsUrl, log_level: logLevel })
      });
      
      const result = await response.json();
      console.log(`Conversion completed: ${result.workouts_processed} workouts`);
      
      // Option 2: Store results in KV or R2
      if (env.WORKOUTS_KV) {
        await env.WORKOUTS_KV.put(
          `workouts-${new Date().toISOString().split('T')[0]}`,
          JSON.stringify(result.workouts)
        );
      }
    } catch (error) {
      console.error('Conversion failed:', error);
    }
  },
  
  async fetch(request, env, ctx) {
    // HTTP Endpoint Handler
    const icsUrl = env.ICS_URL;
    
    if (!icsUrl) {
      return new Response(
        JSON.stringify({ error: 'ICS_URL not configured' }),
        { status: 500, headers: { 'Content-Type': 'application/json' } }
      );
    }
    
    try {
      // Trigger conversion via HTTP
      const response = await fetch('https://your-python-service.com/convert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ics_url: icsUrl })
      });
      
      const result = await response.json();
      
      return new Response(
        JSON.stringify({
          success: true,
          workouts: result.workouts,
          count: result.workouts.length
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } }
      );
    } catch (error) {
      return new Response(
        JSON.stringify({ success: false, error: error.message }),
        { status: 500, headers: { 'Content-Type': 'application/json' } }
      );
    }
  }
};
"""

# Alternative: Use Cloudflare Pages Functions with Python
# Create functions/convert.py:
"""
import json
from runna_to_intervals import RunnaWorkoutConverter, StructuredLogger

async def on_request(context):
    # Get environment variables
    ics_url = context.env.get('ICS_URL')
    log_level = context.env.get('LOG_LEVEL', 'INFO')
    
    # Initialize logger and converter
    logger = StructuredLogger(level=log_level, use_json=True)
    
    try:
        converter = RunnaWorkoutConverter(ics_url, logger=logger)
        workouts = converter.process_calendar()
        
        return Response(
            json.dumps({
                'success': True,
                'workouts': workouts,
                'count': len(workouts)
            }),
            headers={'Content-Type': 'application/json'}
        )
    except Exception as e:
        logger.error('Conversion failed', error=str(e))
        return Response(
            json.dumps({'success': False, 'error': str(e)}),
            status=500,
            headers={'Content-Type': 'application/json'}
        )
"""

# Recommended Approach for Production:
# 
# 1. Run Python script on a server/container with cron:
#    0 2 * * * /usr/bin/python3 /path/to/runna_to_intervals.py
#
# 2. Or deploy Python script as a serverless function:
#    - AWS Lambda
#    - Google Cloud Functions
#    - Azure Functions
#    
# 3. Use Cloudflare Workers to trigger the serverless function:
#    - Scheduled trigger in Cloudflare Workers
#    - Calls your Python serverless function
#    - Processes and stores results
#
# 4. Or use Cloudflare Durable Objects:
#    - Store state in Durable Objects
#    - Worker triggers Python service
#    - Results stored back in Durable Objects
