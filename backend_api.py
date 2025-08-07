#!/usr/bin/env python3
"""
Prosora Intelligence Engine - FastAPI Backend
Production-ready API backend for multi-user support and scaling
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import asyncio
import uuid
from datetime import datetime
import json
import os
from contextlib import asynccontextmanager

# Import your intelligence engines
from phase5_self_improving_intelligence import Phase5SelfImprovingIntelligence

# Pydantic models
class QueryRequest(BaseModel):
    query: str = Field(..., description="The intelligence query to process")
    user_id: str = Field(..., description="User identifier")
    options: Dict = Field(default_factory=dict, description="Processing options")
    enable_learning: bool = Field(default=True, description="Enable learning loop")
    simulate_performance: bool = Field(default=False, description="Simulate performance feedback")

class QueryResponse(BaseModel):
    query_id: str
    query: str
    user_id: str
    results: Dict
    processing_time: float
    status: str
    created_at: datetime
    phases_completed: int

class UserHistoryResponse(BaseModel):
    user_id: str
    queries: List[QueryResponse]
    total_queries: int
    avg_processing_time: float

class SystemMetricsResponse(BaseModel):
    total_queries: int
    active_users: int
    avg_processing_time: float
    system_health: str
    learning_insights: int
    uptime: str

class PerformanceFeedback(BaseModel):
    query_id: str
    actual_engagement: float
    platform: str = "linkedin"
    additional_metrics: Dict = Field(default_factory=dict)

# Global variables
intelligence_engine = None
query_history = {}
system_metrics = {
    "total_queries": 0,
    "active_users": set(),
    "start_time": datetime.now()
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    global intelligence_engine
    
    # Startup
    print("🚀 Initializing Prosora Intelligence Engine...")
    intelligence_engine = Phase5SelfImprovingIntelligence()
    print("✅ Intelligence Engine ready")
    
    yield
    
    # Shutdown
    print("👋 Shutting down Prosora Intelligence Engine...")

# Create FastAPI app
app = FastAPI(
    title="Prosora Intelligence API",
    description="Production-ready API for the Prosora Intelligence Engine",
    version="1.0.0",
    lifespan=lifespan
)

# Security
security = HTTPBearer(auto_error=False)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication dependency (simplified)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Simple authentication - replace with proper auth in production"""
    if not credentials:
        return "anonymous"
    
    # In production, validate JWT token here
    return credentials.credentials

# Background task for processing
async def process_query_background(query_request: QueryRequest, query_id: str):
    """Process query in background"""
    try:
        response, metrics = intelligence_engine.process_query_with_self_improvement(query_request.query)
        
        # Store results
        result = {
            "query_id": query_id,
            "query": query_request.query,
            "user_id": query_request.user_id,
            "results": response,
            "processing_time": metrics.total_latency,
            "status": "completed",
            "created_at": datetime.now(),
            "phases_completed": 5
        }
        
        # Update history
        if query_request.user_id not in query_history:
            query_history[query_request.user_id] = []
        query_history[query_request.user_id].append(result)
        
        # Update system metrics
        system_metrics["total_queries"] += 1
        system_metrics["active_users"].add(query_request.user_id)
        
        print(f"✅ Query {query_id} completed for user {query_request.user_id}")
        
    except Exception as e:
        print(f"❌ Query {query_id} failed: {e}")
        # Store error result
        error_result = {
            "query_id": query_id,
            "query": query_request.query,
            "user_id": query_request.user_id,
            "results": {"error": str(e)},
            "processing_time": 0,
            "status": "failed",
            "created_at": datetime.now(),
            "phases_completed": 0
        }
        
        if query_request.user_id not in query_history:
            query_history[query_request.user_id] = []
        query_history[query_request.user_id].append(error_result)

# API Routes

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Prosora Intelligence API",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "intelligence_engine": "online" if intelligence_engine else "offline",
        "uptime": str(datetime.now() - system_metrics["start_time"])
    }

@app.post("/api/v1/process-query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    background_tasks: BackgroundTasks,
    current_user: str = Depends(get_current_user)
):
    """Process intelligence query through all 5 phases"""
    
    query_id = str(uuid.uuid4())
    
    # For demo, process synchronously
    # In production, use background_tasks.add_task() for async processing
    
    try:
        print(f"🔍 Processing query: {request.query}")
        
        response, metrics = intelligence_engine.process_query_with_self_improvement(request.query)
        
        # Simulate performance feedback if requested
        performance_feedback = None
        if request.simulate_performance and 'error' not in response:
            content_id = response.get('self_improving_content', {}).get('performance_tracking_id', 'test')
            predicted = response.get('learning_summary', {}).get('max_learning_enhanced_engagement', 0.5)
            performance_feedback = intelligence_engine.simulate_performance_feedback(
                content_id, 'analytical', predicted
            )
        
        # Create response
        result = QueryResponse(
            query_id=query_id,
            query=request.query,
            user_id=request.user_id,
            results={
                **response,
                "performance_feedback": performance_feedback
            },
            processing_time=metrics.total_latency,
            status="completed",
            created_at=datetime.now(),
            phases_completed=5
        )
        
        # Store in history
        if request.user_id not in query_history:
            query_history[request.user_id] = []
        query_history[request.user_id].append(result.dict())
        
        # Update metrics
        system_metrics["total_queries"] += 1
        system_metrics["active_users"].add(request.user_id)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/api/v1/user/{user_id}/history", response_model=UserHistoryResponse)
async def get_user_history(
    user_id: str,
    limit: int = 10,
    current_user: str = Depends(get_current_user)
):
    """Get user's query history"""
    
    user_queries = query_history.get(user_id, [])
    
    # Limit results
    limited_queries = user_queries[-limit:] if limit > 0 else user_queries
    
    # Calculate metrics
    avg_time = 0
    if limited_queries:
        avg_time = sum(q.get("processing_time", 0) for q in limited_queries) / len(limited_queries)
    
    return UserHistoryResponse(
        user_id=user_id,
        queries=[QueryResponse(**q) for q in limited_queries],
        total_queries=len(user_queries),
        avg_processing_time=avg_time
    )

@app.get("/api/v1/analytics/system", response_model=SystemMetricsResponse)
async def get_system_metrics(current_user: str = Depends(get_current_user)):
    """Get system-wide analytics"""
    
    # Calculate average processing time
    all_queries = []
    for user_queries in query_history.values():
        all_queries.extend(user_queries)
    
    avg_time = 0
    if all_queries:
        avg_time = sum(q.get("processing_time", 0) for q in all_queries) / len(all_queries)
    
    # Get learning insights
    learning_insights = 0
    try:
        insights = intelligence_engine.learning_engine.get_learning_insights(7)
        learning_insights = len(insights)
    except:
        pass
    
    uptime = str(datetime.now() - system_metrics["start_time"])
    
    return SystemMetricsResponse(
        total_queries=system_metrics["total_queries"],
        active_users=len(system_metrics["active_users"]),
        avg_processing_time=avg_time,
        system_health="healthy",
        learning_insights=learning_insights,
        uptime=uptime
    )

@app.post("/api/v1/feedback/performance")
async def submit_performance_feedback(
    feedback: PerformanceFeedback,
    current_user: str = Depends(get_current_user)
):
    """Submit actual performance feedback for learning"""
    
    try:
        # Find the query
        query_found = False
        for user_queries in query_history.values():
            for query in user_queries:
                if query["query_id"] == feedback.query_id:
                    # Add feedback to query
                    query["actual_performance"] = {
                        "engagement": feedback.actual_engagement,
                        "platform": feedback.platform,
                        "metrics": feedback.additional_metrics,
                        "submitted_at": datetime.now().isoformat()
                    }
                    query_found = True
                    break
            if query_found:
                break
        
        if not query_found:
            raise HTTPException(status_code=404, detail="Query not found")
        
        # Feed back to learning engine (simplified)
        # In production, this would update the learning models
        
        return {
            "status": "success",
            "message": "Performance feedback recorded",
            "query_id": feedback.query_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback submission failed: {str(e)}")

@app.get("/api/v1/learning/insights")
async def get_learning_insights(
    days: int = 7,
    current_user: str = Depends(get_current_user)
):
    """Get learning insights and patterns"""
    
    try:
        insights = intelligence_engine.learning_engine.get_learning_insights(days)
        
        return {
            "insights": insights,
            "total_insights": len(insights),
            "days_analyzed": days,
            "generated_at": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get insights: {str(e)}")

@app.get("/api/v1/sources/status")
async def get_sources_status(current_user: str = Depends(get_current_user)):
    """Get status of real sources"""
    
    try:
        # Test source fetching
        test_sources = intelligence_engine.real_source_fetcher.fetch_sources_for_query(['tech'], ['test'])
        
        return {
            "status": "online",
            "sources_available": len(test_sources),
            "last_check": datetime.now(),
            "source_types": ["RSS", "Web Scraping"],
            "cache_status": "active"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "last_check": datetime.now()
        }

# WebSocket endpoint for real-time updates (optional)
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket, user_id: str):
    """WebSocket for real-time query updates"""
    await websocket.accept()
    
    try:
        while True:
            # Send periodic updates
            await asyncio.sleep(5)
            
            user_queries = query_history.get(user_id, [])
            latest_query = user_queries[-1] if user_queries else None
            
            if latest_query:
                await websocket.send_json({
                    "type": "status_update",
                    "latest_query": latest_query,
                    "total_queries": len(user_queries)
                })
                
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Endpoint not found", "status_code": 404}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "status_code": 500}

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Prosora Intelligence API...")
    uvicorn.run(
        "backend_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )