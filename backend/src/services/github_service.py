"""
GitHub API integration service.
"""

import time
from typing import Dict, List, Optional

import requests
from github import BadCredentialsException, Github, GithubException

from config import get_settings
from src.exceptions import GitHubAPIError
from src.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


class GitHubService:
    """Service for GitHub API interactions."""

    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub service.

        Args:
            token: GitHub personal access token
        """
        self.token = token or settings.github_token
        if not self.token:
            raise GitHubAPIError("GitHub token not configured")

        try:
            self.client = Github(self.token, timeout=settings.github_api_timeout)
            # Verify token works
            self.client.get_user().login
            logger.info("GitHub service initialized successfully")
        except BadCredentialsException as e:
            raise GitHubAPIError(f"Invalid GitHub token: {e}")
        except GithubException as e:
            raise GitHubAPIError(f"GitHub API error: {e}")

    def parse_pr_url(self, url: str) -> Dict[str, str]:
        """Parse GitHub PR URL.

        Args:
            url: PR URL like https://github.com/owner/repo/pull/123

        Returns:
            Dict with owner, repo, pr_number

        Raises:
            GitHubAPIError: If URL is invalid
        """
        try:
            parts = url.rstrip("/").split("/")
            if len(parts) < 7 or parts[-2] != "pull":
                raise ValueError("Invalid PR URL format")

            return {
                "owner": parts[3],
                "repo": parts[4],
                "pr_number": int(parts[6]),
            }
        except (IndexError, ValueError) as e:
            raise GitHubAPIError(f"Invalid GitHub PR URL: {e}")

    def get_pr_details(self, pr_url: str) -> Dict:
        """Get PR details from GitHub.

        Args:
            pr_url: GitHub PR URL

        Returns:
            Dict with PR information
        """
        try:
            parsed = self.parse_pr_url(pr_url)
            repo = self.client.get_repo(f"{parsed['owner']}/{parsed['repo']}")
            pr = repo.get_pull(parsed["pr_number"])

            logger.info(f"Fetched PR details: {pr.title}")

            return {
                "title": pr.title,
                "body": pr.body,
                "state": pr.state,
                "created_at": pr.created_at.isoformat(),
                "updated_at": pr.updated_at.isoformat(),
                "base_branch": pr.base.ref,
                "head_branch": pr.head.ref,
            }
        except GithubException as e:
            raise GitHubAPIError(f"Failed to get PR details: {e}")

    def get_pr_diff(self, pr_url: str) -> str:
        """Get PR diff (unified format).

        Args:
            pr_url: GitHub PR URL

        Returns:
            Unified diff format
        """
        try:
            parsed = self.parse_pr_url(pr_url)
            repo = self.client.get_repo(f"{parsed['owner']}/{parsed['repo']}")
            pr = repo.get_pull(parsed["pr_number"])

            diff_data = requests.get(
                pr.diff_url, timeout=settings.github_api_timeout, headers=self._get_headers()
            )

            if diff_data.status_code != 200:
                raise GitHubAPIError(f"Failed to fetch diff: HTTP {diff_data.status_code}")

            logger.info(f"Fetched diff for PR {parsed['pr_number']}")
            return diff_data.text

        except requests.RequestException as e:
            raise GitHubAPIError(f"Failed to fetch PR diff: {e}")
        except GithubException as e:
            raise GitHubAPIError(f"GitHub API error: {e}")

    def get_pr_files(self, pr_url: str) -> List[Dict]:
        """Get list of changed files in PR.

        Args:
            pr_url: GitHub PR URL

        Returns:
            List of dicts with file information
        """
        try:
            parsed = self.parse_pr_url(pr_url)
            repo = self.client.get_repo(f"{parsed['owner']}/{parsed['repo']}")
            pr = repo.get_pull(parsed["pr_number"])

            files = []
            for file in pr.get_files():
                files.append(
                    {
                        "name": file.filename,
                        "status": file.status,
                        "additions": file.additions,
                        "deletions": file.deletions,
                        "changes": file.changes,
                        "patch": file.patch,
                    }
                )

            logger.info(f"Fetched {len(files)} files from PR")
            return files

        except GithubException as e:
            raise GitHubAPIError(f"Failed to get PR files: {e}")

    def get_file_content(self, owner: str, repo: str, path: str, ref: str = "main") -> str:
        """Get file content from repository.

        Args:
            owner: Repository owner
            repo: Repository name
            path: File path
            ref: Branch/commit reference

        Returns:
            File content
        """
        try:
            repo_obj = self.client.get_repo(f"{owner}/{repo}")
            content = repo_obj.get_contents(path, ref=ref)
            return content.decoded_content.decode("utf-8")

        except GithubException as e:
            raise GitHubAPIError(f"Failed to get file content: {e}")

    def post_comment(self, pr_url: str, comment: str) -> bool:
        """Post comment on PR.

        Args:
            pr_url: GitHub PR URL
            comment: Comment text

        Returns:
            True if successful
        """
        try:
            parsed = self.parse_pr_url(pr_url)
            repo = self.client.get_repo(f"{parsed['owner']}/{parsed['repo']}")
            pr = repo.get_pull(parsed["pr_number"])

            pr.create_issue_comment(comment)
            logger.info(f"Posted comment on PR {parsed['pr_number']}")
            return True

        except GithubException as e:
            raise GitHubAPIError(f"Failed to post comment: {e}")

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        return {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3.raw+json",
        }
