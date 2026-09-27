# ©️ Codrago, 2024-2030
# This file is a part of Pixelazer Userbot
# 🌐 https://github.com/coddrago/Pixelazer
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

import logging
import os
import subprocess
from typing import Literal

import git
import pixelazertl

from .. import version

parser = pixelazertl.utils.sanitize_parse_mode("html")
logger = logging.getLogger(__name__)


def _is_no_git() -> bool:
    return os.environ.get("PIXELAZER_NO_GIT") == "1"


# GeekTG Compatibility
def get_git_info() -> tuple[str, str]:
    """
    Get git info
    :return: Git info
    """
    if _is_no_git():
        return ("", "")
    hash_ = get_git_hash() or ""
    return (
        hash_,
        f"https://github.com/gardenyab/pixelazer/commit/{hash_}" if hash_ else "",
    )


def get_git_hash() -> str | Literal[False]:
    """
    Get current Pixelazer git hash
    :return: Git commit hash
    """
    if _is_no_git():
        return False
    try:
        with git.Repo() as repo:
            return repo.head.commit.hexsha
    except Exception:
        return False


def get_commit_url() -> str:
    """
    Get current Pixelazer git commit url
    :return: Git commit url
    """
    if _is_no_git():
        return "Unknown"
    try:
        hash_ = get_git_hash()
        if not hash_:
            return "Unknown"
        return f'<a href="https://github.com/gardenyab/Pixelazer/commit/{hash_}">#{hash_[:7]}</a>'
    except Exception:
        return "Unknown"


def get_git_status() -> str:
    """
    :return: 'Clean' or 'X files modified'.
    """
    if _is_no_git():
        return "Git disabled"
    try:
        process = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=5,
        )

        if process.returncode != 0:
            return "Not a Git repo"

        output = process.stdout.strip()

        if not output:
            return "Clean"

        count = len(output.splitlines())
        word = "file" if count == 1 else "files"
        return f"{count} {word} modified"

    except subprocess.TimeoutExpired:
        return "Unknown"
    except Exception:
        return "Unknown"


def get_last_commit_message() -> str:
    """
    Get the message of the last commit
    :return: Last commit message
    """
    if _is_no_git():
        return "Unknown"
    try:
        with git.Repo() as repo:
            message = repo.head.commit.message
            if isinstance(message, bytes):
                return message.decode(errors="replace").strip()
            return message.strip()
    except Exception:
        return "Unknown"


def get_commit_count() -> int:
    """
    Get the total number of commits in the repository
    :return: Number of commits
    """
    if _is_no_git():
        return 0
    try:
        with git.Repo() as repo:
            return len(list(repo.iter_commits()))
    except Exception:
        return 0


def is_up_to_date():
    with git.Repo(search_parent_directories=True) as repo:
        diff = any(repo.iter_commits(f"HEAD..origin/{version.branch}", max_count=1))
        return not diff

def get_added_lines_by_file(commit_ref="HEAD", as_string: bool = False):
    added_by_file = {}

    with git.Repo(search_parent_directories=True) as repo:
        commit = repo.commit(commit_ref)
        parent = commit.parents[0] if commit.parents else None

        for diff in commit.diff(parent, create_patch=True):
            if diff.diff is None:
                continue

            file_path = diff.b_path or diff.a_path
            patch_text = diff.diff.decode("utf-8", errors="replace")

            file_added_lines = [
                line[1:]
                for line in patch_text.splitlines()
                if line.startswith("+") and not line.startswith("+++")
            ]

            if file_added_lines:
                added_by_file[file_path] = file_added_lines

    if as_string:
        all_lines = []
        for lines in added_by_file.values():
            all_lines.extend(lines)
        return "\n".join(all_lines)

    return added_by_file
