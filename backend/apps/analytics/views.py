from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Count, Q
from django.db import connection
from apps.applications.models import Application
from apps.officers.models import Officer
from datetime import datetime, timedelta
from django.conf import settings

class AnalyticsDashboardView(APIView):
    """Admin analytics dashboard"""
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        # Total applications
        total_applications = Application.objects.count()
        
        # Status breakdown
        status_breakdown = Application.objects.values('status').annotate(count=Count('id'))
        
        # Applications by service category
        category_breakdown = Application.objects.values('service_category').annotate(count=Count('id'))
        
        # Officer workload distribution
        officer_workload = Officer.objects.filter(is_active=True).values(
            'user__username', 'department', 'hierarchy_level', 'workload_count'
        )
        
        # Recent applications (last 7 days)
        week_ago = datetime.now() - timedelta(days=7)
        recent_apps = Application.objects.filter(created_at__gte=week_ago).count()
        
        # Approval/Rejection rates
        approved = Application.objects.filter(status='APPROVED').count()
        rejected = Application.objects.filter(status='REJECTED').count()
        
        # Department-wise distribution
        dept_breakdown = Officer.objects.filter(is_active=True).values('department').annotate(
            officer_count=Count('id')
        )
        
        return Response({
            'total_applications': total_applications,
            'status_breakdown': list(status_breakdown),
            'category_breakdown': list(category_breakdown),
            'officer_workload': list(officer_workload),
            'recent_applications': recent_apps,
            'approval_rate': round((approved / total_applications * 100) if total_applications > 0 else 0, 2),
            'rejection_rate': round((rejected / total_applications * 100) if total_applications > 0 else 0, 2),
            'department_breakdown': list(dept_breakdown)
        })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    """Health check endpoint for load balancer"""
    health_status = {
        'status': 'healthy',
        'database': 'unknown',
        'redis': 'unknown'
    }
    
    # Check database connection
    try:
        connection.ensure_connection()
        health_status['database'] = 'connected'
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['database'] = f'error: {str(e)}'
    
    # Check Redis connection (optional - don't fail if Redis not configured)
    try:
        if hasattr(settings, 'CACHES') and 'default' in settings.CACHES:
            import redis
            redis_url = settings.CACHES['default'].get('LOCATION', '')
            if redis_url:
                r = redis.from_url(redis_url)
                r.ping()
                health_status['redis'] = 'connected'
            else:
                health_status['redis'] = 'not_configured'
        else:
            health_status['redis'] = 'not_configured'
    except ImportError:
        health_status['redis'] = 'redis_not_installed'
    except Exception as e:
        # Don't fail health check if Redis is down
        health_status['redis'] = f'unavailable: {str(e)}'
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return Response(health_status, status=status_code)

get_dashboard_stats = AnalyticsDashboardView.as_view()
