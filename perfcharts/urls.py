"""perfcharts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .perfdata.views import *

urlpatterns = [
    path('', api_root),
    path('admin/', admin.site.urls),
    path('repos/', RepoList.as_view(), name="repo-list"),
    path('repos/<int:pk>', RepoDetail.as_view(), name="repo-detail"),
    path('branches/', BranchList.as_view(), name="branch-list"),
    path('branches/<int:pk>', BranchDetail.as_view(), name="branch-detail"),
    path('branches/<str:repo>', BranchesForRepoList.as_view(), name="branch-repo-list"),
    path('revisions/', RevisionList.as_view(), name="revision-list"),
    path('revisions/<int:pk>', RevisionDetail.as_view(), name="revision-detail"),
    path('executables/', ExecutableList.as_view(), name="executable-list"),
    path('executables/<int:pk>', ExecutableDetail.as_view(), name="executable-detail"),
    path('executables/<str:repo>', ExecutableForRepoList.as_view(), name="executable-repo-list"),
    path('benchmarks/', BenchmarkList.as_view(), name="benchmark-list"),
    path('benchmarks/<int:pk>', BenchmarkDetail.as_view(), name="benchmark-detail"),
    path('metrics/', MetricList.as_view(), name="metric-list"),
    path('metrics/<int:pk>', MetricDetail.as_view(), name="metric-detail"),
    path('environments/', EnvironmentList.as_view(), name="environment-list"),
    path('environments/<int:pk>', EnvironmentDetail.as_view(), name="environment-detail"),
    path('results/', ResultList.as_view(), name="result-list"),
    path('results/<int:pk>', ResultDetail.as_view(), name="result-detail"),
    path('result/', post_result, name='result'),
    path('revision/', post_revision, name='revision'),
    path('chartdata/<str:exe>/<str:repo>/<str:branch>/<str:benchmarks>/<str:metrics>/', ChartDataList.as_view(), name='chart-data'),
    path('refdata/<str:exe>/<str:repo>/<str:revision>', RefDataList.as_view(), name='ref-data'),
    path('comparebranches/<str:exe>/<str:repo>/<str:branches>/<str:benchmarks>/<str:metrics>/', BranchCompareList.as_view(), name='compare-branches'),
]

urlpatterns = format_suffix_patterns(urlpatterns)