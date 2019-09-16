from rest_framework import serializers

from .models import Repo, Revision, Branch, Executable, Benchmark, Metric, Environment, Result


class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repo
        fields = ["name", "default_branch"]


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["name", "repo"]


class RevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revision
        fields = ["commitid", "tag", "date", "title", "message", "repo", "author", "branch"]


class ExecutableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Executable
        fields = ["name", "description", "repo"]
        depth = 1


class BenchmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benchmark
        fields = ["name", "description"]


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ["name", "description", "unit"]


class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = ["name", "description"]


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ["value", "std_dev", "val_min", "val_max", "q1", "q3", "date", "revision", "executable",
                  "benchmark", "metric", "environment"]
