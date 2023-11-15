from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def get_recommendations(request):
    data = {'isbns': ['ISBN-10: 0-306-40615-2',
            'ISBN-10: 3-16-148410-0',
            'ISBN-13: 978-0-13-468602-4',
            'ISBN-13: 978-1-59059-356-9',
            'ISBN-10: 0-596-52068-9']}
    return JsonResponse(data)
