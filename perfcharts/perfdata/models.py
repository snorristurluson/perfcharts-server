from django.db import models


class Repo(models.Model):
    name = models.CharField(unique=True, max_length=42)
    default_branch = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=32)
    repo = models.ForeignKey(
        Repo, on_delete=models.CASCADE, related_name="branches")

    def __str__(self):
        return self.repo.name + ":" + self.name

    class Meta:
        unique_together = ("name", "repo")
        verbose_name_plural = "branches"


class Revision(models.Model):
    commitid = models.CharField(max_length=42)
    tag = models.CharField(max_length=64, blank=True, null=True)
    date = models.DateTimeField(null=True)
    title = models.CharField(max_length=64, blank=True)
    message = models.TextField(blank=True)

    author = models.CharField(max_length=100, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="revisions")

    def __str__(self):
        if self.date is None:
            date = None
        else:
            date = self.date.strftime("%b %d, %H:%M")
        string = " - ".join(filter(None, (date, self.commitid, self.tag)))
        if self.branch.name != self.branch.repo.default_branch:
            string += " - " + self.branch.name
        return string

    class Meta:
        unique_together = ("commitid", "branch")


class Executable(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200, blank=True)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE, related_name="executables")

    class Meta:
        unique_together = ('name', 'repo')

    def __str__(self):
        return self.name


class Benchmark(models.Model):
    name = models.CharField(max_length=100)
    executable = models.ForeignKey(Executable, on_delete=models.CASCADE, related_name="benchmarks")
    description = models.CharField(max_length=300, blank=True)
    checksum = models.CharField(max_length=40, blank=True)
    reference = models.ForeignKey(Revision, on_delete=models.SET_NULL, null=True, related_name="benchmarks")

    class Meta:
        unique_together = ('name', 'executable')

    def __str__(self):
        return self.name


class Metric(models.Model):
    name = models.CharField(unique=True, max_length=32)
    description = models.CharField(max_length=300, blank=True)
    unit = models.CharField(max_length=20, default="seconds")

    def __str__(self):
        return self.name


class Environment(models.Model):
    name = models.CharField(unique=True, max_length=100)
    description = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.name


class Result(models.Model):
    value = models.FloatField()
    date = models.DateTimeField(blank=True, null=True)
    revision = models.ForeignKey(Revision, on_delete=models.CASCADE, related_name="results")
    executable = models.ForeignKey(Executable, on_delete=models.CASCADE, related_name="results")
    benchmark = models.ForeignKey(Benchmark, on_delete=models.CASCADE, related_name="results")
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE, related_name="results")
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE, related_name="results")
    checksum = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return u"%s - %s: %s" % (self.benchmark.name, self.metric, self.value)

    class Meta:
        unique_together = ("revision", "executable", "benchmark", "metric", "environment")

