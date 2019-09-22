import datetime
from collections import OrderedDict

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import *


class RepoList(generics.ListCreateAPIView):
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer


class RepoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer


class BranchList(generics.ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class BranchDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class BranchesForRepoList(generics.ListAPIView):
    serializer_class = BranchSerializer

    def get_queryset(self):
        repo_name = self.kwargs["repo"]
        repo = Repo.objects.get(name=repo_name)

        qs = Branch.objects.filter(repo=repo.id)
        return qs


class RevisionList(generics.ListCreateAPIView):
    queryset = Revision.objects.all()
    serializer_class = RevisionSerializer


class RevisionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Revision.objects.all()
    serializer_class = RevisionSerializer


class ExecutableList(generics.ListCreateAPIView):
    queryset = Executable.objects.all()
    serializer_class = ExecutableSerializer


class ExecutableDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Executable.objects.all()
    serializer_class = ExecutableSerializer


class ExecutableForRepoList(generics.ListAPIView):
    serializer_class = ExecutableSerializer

    def get_queryset(self):
        repo_name = self.kwargs["repo"]
        repo = Repo.objects.get(name=repo_name)

        qs = Executable.objects.filter(repo=repo.id)
        return qs


class BenchmarkList(generics.ListCreateAPIView):
    queryset = Benchmark.objects.all()
    serializer_class = BenchmarkSerializer


class BenchmarkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Benchmark.objects.all()
    serializer_class = BenchmarkSerializer


class MetricList(generics.ListCreateAPIView):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer


class MetricDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer


class EnvironmentList(generics.ListCreateAPIView):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer


class EnvironmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer


class ResultList(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class ResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class ChartDataList(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        exe_name = kwargs["exe"]
        repo_name = kwargs["repo"]
        branch_name = kwargs["branch"]
        benchmark_names = kwargs["benchmarks"].split("|")
        metric_names = kwargs["metrics"].split("|")

        print(exe_name, repo_name, branch_name, benchmark_names, metric_names)

        repo = Repo.objects.get(name=repo_name)
        exe = Executable.objects.get(name=exe_name, repo=repo)
        branch = Branch.objects.get(name=branch_name, repo=repo)
        benchmarks = Benchmark.objects.filter(name__in=benchmark_names).values("id")
        metrics = Metric.objects.filter(name__in=metric_names).values("id")

        results = Result.objects \
            .filter(executable=exe) \
            .filter(revision__branch=branch) \
            .filter(benchmark_id__in=benchmarks) \
            .filter(metric_id__in=metrics) \
            .order_by("date")

        by_sha = OrderedDict()
        revisions = {}
        for r in results:
            sha = r.revision.commitid
            revisions[sha] = r.revision
            results_for_sha = by_sha.get(sha, [])

            results_for_sha.append({
                "value": r.value,
                "benchmark": r.benchmark.name,
                "metric": r.metric.name
            })
            by_sha[sha] = results_for_sha

        data = []
        for sha, results_for_sha in by_sha.items():
            data.append({
                "sha": sha,
                "title": revisions[sha].title,
                "author": revisions[sha].author,
                "date": revisions[sha].date,
                "results": results_for_sha
            })

        return Response(data)


class RefDataList(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        exe_name = kwargs["exe"]
        repo_name = kwargs["repo"]
        revision_name = kwargs["revision"]

        print(exe_name, repo_name, revision_name)

        repo = Repo.objects.get(name=repo_name)
        exe = Executable.objects.get(name=exe_name, repo=repo)
        revision = Revision.objects.filter(commitid=revision_name)[0]

        query_results = Result.objects \
            .filter(executable=exe) \
            .filter(executable=exe) \
            .filter(revision=revision)

        results = []

        for r in query_results:
            results.append({
                "value": r.value,
                "benchmark": r.benchmark.name,
                "metric": r.metric.name
            })

        data = {
            "commitid": revision.commitid,
            "title": revision.title,
            "author": revision.author,
            "date": revision.date,
            "results": results
        }

        return Response(data)


class BranchCompareList(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        exe_name = kwargs["exe"]
        repo_name = kwargs["repo"]
        branch_names = kwargs["branches"].split("|")
        benchmark_names = kwargs["benchmarks"].split("|")
        metric_names = kwargs["metrics"].split("|")

        repo = Repo.objects.get(name=repo_name)
        exe = Executable.objects.get(name=exe_name, repo=repo)
        benchmarks = Benchmark.objects.filter(name__in=benchmark_names).values("id")
        metrics = Metric.objects.filter(name__in=metric_names).values("id")

        # There may be a better way to do this, but for now I'm doing multiple queries.
        # Get the latest commit per branch, then get all results for that commit
        latest_commits = {}
        for branch in branch_names:
            results = Result.objects.filter(executable=exe).filter(revision__branch__name=branch).order_by("-date")
            latest_commits[branch] = results[0].revision.commitid

        combined_results = []
        for branch, commit in latest_commits.items():
            results = Result.objects \
                .filter(revision__commitid=commit) \
                .filter(benchmark_id__in=benchmarks) \
                .filter(metric_id__in=metrics)
            per_branch = {
                "branch": branch,
                "sha": commit,
                "results": [{"value": x.value, "benchmark": x.benchmark.name, "metric": x.metric.name} for x in results]
            }
            combined_results.append(per_branch)

        print(combined_results)
        return Response(combined_results)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'repos': reverse('repo-list', request=request, format=format),
        'branches': reverse('branch-list', request=request, format=format),
        'revisions': reverse('revision-list', request=request, format=format),
        'executables': reverse('executable-list', request=request, format=format),
        'benchmarks': reverse('benchmark-list', request=request, format=format),
        'metrics': reverse('metric-list', request=request, format=format),
        'environments': reverse('environment-list', request=request, format=format),
        'results': reverse('result-list', request=request, format=format),
        'result': reverse('result', request=request, format=format),
        'revision': reverse('revision', request=request, format=format),
    })


@api_view(['POST'])
def post_revision(request, format=None):
    revision = request.data
    save_revision(revision)
    return Response()


def save_revision(revision):
    print(revision)
    repo, _ = Repo.objects.get_or_create(name=revision["repo"])
    branch, _ = Branch.objects.get_or_create(name=revision["branch"], repo=repo)
    try:
        r = Revision.objects.get(commitid=revision["sha"], branch=branch)
    except Revision.DoesNotExist:
        r = Revision(commitid=revision["sha"], branch=branch)
    if "author" in revision:
        r.author = revision.get("author")[:64]
    r.date = revision.get("date")
    if "tag" in revision:
        r.tag = revision.get("tag")[:64]
    if "title" in revision:
        r.title = revision.get("title")[:64]
    r.message = revision.get("message")
    r.save()


@api_view(['POST'])
def post_result(request, format=None):
    results = request.data
    for each in results:
        save_result(each)

    return Response()


def save_result(result):
    repo, _ = Repo.objects.get_or_create(name=result["repo"])
    branch, _ = Branch.objects.get_or_create(name=result["branch"], repo=repo)
    exe, _ = Executable.objects.get_or_create(name=result["executable"], repo=repo)
    env, _ = Environment.objects.get_or_create(name=result["environment"])
    benchmark, _ = Benchmark.objects.get_or_create(name=result["benchmark"])
    metric, _ = Metric.objects.get_or_create(name=result["metric"])
    revision, _ = Revision.objects.get_or_create(commitid=result["commitid"], branch=branch)
    try:
        r = Result.objects.get(revision=revision, executable=exe, benchmark=benchmark, metric=metric, environment=env)
        print("Result exists", r)
    except Result.DoesNotExist:
        r = Result(revision=revision, executable=exe, benchmark=benchmark, metric=metric, environment=env)
    r.value = result.get("result_value")
    if 'result_date' in result:
        r.date = result["result_date"]
    elif revision.date:
        r.date = revision.date
    else:
        r.date = datetime.datetime.now(datetime.timezone.utc)
    r.save()