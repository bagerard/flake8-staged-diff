from unittest.mock import patch

from flake8_staged_diff.main import find_between, git_diff_upsert_lines, main


git_diff_staged_sample = """diff --git a/.pre-commit-config.yaml b/.pre-commit-config.yaml
index 6e6605037e..ced2675a60 100644
--- a/.pre-commit-config.yaml
+++ b/.pre-commit-config.yaml
@@ -288,0 +289,12 @@ repos:
+
+  - repo: https://github.com/pycqa/flake8
+    rev: 3.9.2
+    hooks:
+      - id: flake8
+        name: flake8-diff-annotations
+        entry: python flake8diff.py
+        args:
+          - "--select=AN"
+          - "--ignore=ANN1"
+        additional_dependencies:
+          - flake8-annotations
diff --git a/src/databasemanager/database_manager.py b/src/databasemanager/database_manager.py
index 524b3cfa7c..74b84e7e56 100644
--- a/src/databasemanager/database_manager.py
+++ b/src/databasemanager/database_manager.py
@@ -26 +26,2 @@ class DatabaseManager(SynchronousWorker, DatabaseManagerInterface):
-    def _get_database(self, database_id):
+    def _get_database(self, database_id, test: str) -> None:
+        _ = "d"
    """


flake8_sample_output = """src/databasemanager/database_manager.py:21:18: ANN101 Missing type annotation for self in method
src/databasemanager/database_manager.py:21:25: ANN002 Missing type annotation for *args
src/databasemanager/database_manager.py:21:33: ANN003 Missing type annotation for **kwargs
src/databasemanager/database_manager.py:21:40: ANN204 Missing return type annotation for special method
src/databasemanager/database_manager.py:26:23: ANN101 Missing type annotation for self in method
src/databasemanager/database_manager.py:26:29: ANN001 Missing type annotation for function argument 'database_id'
src/databasemanager/database_manager.py:26:42: ANN001 Missing type annotation for function argument 'test'
src/databasemanager/database_manager.py:26:47: ANN202 Missing return type annotation for protected function
src/databasemanager/database_manager.py:30:28: ANN101 Missing type annotation for self in method
src/databasemanager/database_manager.py:30:34: ANN001 Missing type annotation for function argument 'database_id'
src/databasemanager/database_manager.py:30:46: ANN201 Missing return type annotation for public function
src/databasemanager/database_manager.py:34:28: ANN101 Missing type annotation for self in method
src/databasemanager/database_manager.py:34:34: ANN001 Missing type annotation for function argument 'db_type'
"""


def test_find_between():
    line = "@@ -26 +26,2 @@ class DatabaseManager(SynchronousWorker, DatabaseManagerInterface):"
    assert find_between(line, "+", "@@") == "26,2 "


def test_git_diff_upsert_lines():
    assert git_diff_upsert_lines(git_diff_staged_sample) == {
        ".pre-commit-config.yaml:289",
        ".pre-commit-config.yaml:290",
        ".pre-commit-config.yaml:291",
        ".pre-commit-config.yaml:292",
        ".pre-commit-config.yaml:293",
        ".pre-commit-config.yaml:294",
        ".pre-commit-config.yaml:295",
        ".pre-commit-config.yaml:296",
        ".pre-commit-config.yaml:297",
        ".pre-commit-config.yaml:298",
        ".pre-commit-config.yaml:299",
        ".pre-commit-config.yaml:300",
        "src/databasemanager/database_manager.py:26",
        "src/databasemanager/database_manager.py:27",
    }


def test_main__findings__return_1(capsys):
    with patch("flake8_staged_diff.main.get_diff_staged") as m_get_diff_staged:
        with patch("flake8_staged_diff.main.run_flake8") as m_run_flake8:
            m_get_diff_staged.return_value = git_diff_staged_sample
            m_run_flake8.return_value = flake8_sample_output

            assert main() == 1

            captured = capsys.readouterr()
            assert captured.out == (
                "src/databasemanager/database_manager.py:26:23: ANN101 Missing type annotation for self in method\n"
                "src/databasemanager/database_manager.py:26:29: ANN001 Missing type annotation for function argument 'database_id'\n"
                "src/databasemanager/database_manager.py:26:42: ANN001 Missing type annotation for function argument 'test'\n"
                "src/databasemanager/database_manager.py:26:47: ANN202 Missing return type annotation for protected function\n"
            )


def test_main__no_flake8_findings__return_0(capsys):
    with patch("flake8_staged_diff.main.get_diff_staged") as m_get_diff_staged:
        with patch("flake8_staged_diff.main.run_flake8") as m_run_flake8:
            m_get_diff_staged.return_value = git_diff_staged_sample
            m_run_flake8.return_value = ""

            assert main() == 0
            captured = capsys.readouterr()
            assert captured.out == ""


def test_main__no_staged_files__skip_call_flake8(capsys):
    with patch("flake8_staged_diff.main.get_diff_staged") as m_get_diff_staged:
        with patch("flake8_staged_diff.main.run_flake8") as m_run_flake8:
            m_get_diff_staged.return_value = ""

            assert main() == 0
            m_run_flake8.assert_not_called()
            captured = capsys.readouterr()
            assert captured.out == "No diff - Skip flake8 call\n"
