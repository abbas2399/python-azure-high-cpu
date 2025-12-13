
# ============================================================================
# FOR DJANGO APP
# ============================================================================

# Add to your urls.py:

from django.urls import path
from . import views

urlpatterns = [
    path('cpu-stress/', views.cpu_stress, name='cpu_stress'),
    path('cpu-stress-async/', views.cpu_stress_async, name='cpu_stress_async'),
]


# Add to your views.py:

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import time
import math
from datetime import datetime
import threading

@require_http_methods(["GET"])
def cpu_stress(request):
    duration = int(request.GET.get('duration', 30))
    
    if duration > 120:
        return JsonResponse({
            'error': 'Duration too long. Max 120 seconds'
        }, status=400)
    
    start_time = datetime.now()
    end = time.time() + duration
    iterations = 0
    
    while time.time() < end:
        result = 0
        for i in range(100000):
            result += math.sqrt(i) * math.sin(i) * math.cos(i)
        iterations += 1
    
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    
    return JsonResponse({
        'status': 'completed',
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'duration_requested': duration,
        'duration_actual': elapsed,
        'iterations_completed': iterations
    })

@require_http_methods(["GET"])
def cpu_stress_async(request):
    duration = int(request.GET.get('duration', 30))
    
    if duration > 120:
        return JsonResponse({'error': 'Duration too long. Max 120 seconds'}, status=400)
    
    def background_stress():
        end = time.time() + duration
        while time.time() < end:
            result = sum(math.sqrt(i) * math.sin(i) for i in range(50000))
    
    thread = threading.Thread(target=background_stress)
    thread.daemon = True
    thread.start()
    
    return JsonResponse({
        'status': 'started',
        'message': f'CPU stress test running in background for {duration} seconds',
        'started_at': datetime.now().isoformat()
    })


# ============================================================================
# FOR FASTAPI APP
# ============================================================================

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import time
import math
from datetime import datetime
import asyncio

app = FastAPI()

@app.get("/cpu-stress")
async def cpu_stress(duration: int = Query(default=30, le=120)):
    start_time = datetime.now()
    end = time.time() + duration
    iterations = 0
    
    while time.time() < end:
        result = 0
        for i in range(100000):
            result += math.sqrt(i) * math.sin(i) * math.cos(i)
        iterations += 1
    
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    
    return {
        'status': 'completed',
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'duration_requested': duration,
        'duration_actual': elapsed,
        'iterations_completed': iterations
    }

@app.get("/cpu-stress-async")
async def cpu_stress_async(duration: int = Query(default=30, le=120)):
    async def background_stress():
        end = time.time() + duration
        while time.time() < end:
            result = sum(math.sqrt(i) * math.sin(i) for i in range(50000))
    
    asyncio.create_task(background_stress())
    
    return {
        'status': 'started',
        'message': f'CPU stress test running in background for {duration} seconds',
        'started_at': datetime.now().isoformat()
    }
