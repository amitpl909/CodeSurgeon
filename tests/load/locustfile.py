"""Load test using Locust."""

from locust import HttpUser, task, between


class CodeSurgeonUser(HttpUser):
    """Simulated user of CodeSurgeon API."""

    wait_time = between(1, 3)

    @task(1)
    def health_check(self):
        """Simulate health check."""
        self.client.get("/api/v1/health")

    @task(4)
    def analyze_code(self):
        """Simulate code analysis."""
        self.client.post(
            "/api/v1/analyze",
            json={
                "code": "x = 1 || 2\nif y == None: pass",
                "language": "python",
            },
            timeout=30,
        )

    @task(1)
    def analyze_clean_code(self):
        """Simulate analysis of clean code."""
        self.client.post(
            "/api/v1/analyze",
            json={
                "code": "x = 1 or 2\nif y is None: pass",
                "language": "python",
            },
            timeout=30,
        )
