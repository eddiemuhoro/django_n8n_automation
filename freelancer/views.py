from django.shortcuts import render
from rest_framework.views import APIView
from django.conf import settings
import requests
from datetime import datetime, timezone
from rest_framework.response import Response
from .models import Project

# Create your views here.
class ProjectsToBid(APIView):
    def get(self, request):
        token = settings.FREELANCER_TOKEN
        headers = {
            'Authorization': f'Bearer {token}',
        }

        url = 'https://www.freelancer.com/api/projects/0.1/projects/active/?compact=&limit=10&project_types[]=fixed&query=react&full_description'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            projects = data.get('result', {}).get('projects', [])
            now = datetime.now(timezone.utc)
            filtered = []

            for project in projects:
                created = datetime.fromtimestamp(project['time_submitted'], timezone.utc)
                age_minutes = (now - created).total_seconds() / 60
                bid_count = project.get("bid_stats", {}).get("bid_count", 0)
                url = project.get("url", "")
                final_url = f'https://www.freelancer.com/projects/{url}/details' if url else ""

                if age_minutes < 160 and bid_count < 40:
                    filtered.append({
                        'id': project['id'],
                        'owner_id': project['owner_id'],
                        'title': project['title'],
                        'url': final_url,
                        'description': project['description'],
                        'currency': project['currency']['sign'],
                        'created': created,
                        'age_minutes': age_minutes,
                        'bid_count': bid_count,
                        'bid_avg': project.get("bid_stats", {}).get("bid_avg", 0),
                    })

                    ## Save the project to the database
                    Project.objects.update_or_create(
                        id=project['id'],
                        defaults={
                            'owner_id': project['owner_id'],
                            'title': project['title'],
                            'url': final_url,
                            'description': project['description'],
                            'currency': project['currency']['sign'],
                            'created': created,
                            'age_minutes': age_minutes,
                            'bid_count': bid_count,
                            'bid_avg': project.get("bid_stats", {}).get("bid_avg", 0),
                        }
                    )
            
            return Response({'projects_to_bid': filtered}, status=200)

        else:
            return render(request, 'projects_to_bid.html', {'error': 'Failed to fetch projects'})