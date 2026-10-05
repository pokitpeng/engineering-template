"""Checker tests use isolated fixtures, never modify project documents."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_project import REQUIRED_FILES, check  # noqa: E402


class ProjectCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in REQUIRED_FILES:
            self.put(name, "fixture\n")
        self.put(".github/CODEOWNERS", "* @example\n")

    def put(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_valid_structure(self):
        self.assertEqual(check(self.root), [])
        self.assertEqual(check(self.root, initialized=True), [])

    def test_missing_file(self):
        (self.root / "docs/product/goals.md").unlink()
        self.assertIn("missing required file: docs/product/goals.md", check(self.root))

    def test_empty_file(self):
        self.put("docs/product/goals.md", " \n")
        self.assertIn("empty required file: docs/product/goals.md", check(self.root))

    def test_relative_link_and_fragment(self):
        self.put("docs/specs/sample.md", "[goals](../product/goals.md#users)\n")
        self.assertEqual(check(self.root), [])

    def test_encoded_path_and_title(self):
        self.put("docs/a b.md", "# Target\n")
        self.put("README.md", '[target](docs/a%20b.md "title")\n')
        self.assertEqual(check(self.root), [])

    def test_missing_link(self):
        self.put("README.md", "[missing](docs/specs/missing.md)\n")
        self.assertTrue(any("missing local link target" in e for e in check(self.root)))

    def test_root_relative_link(self):
        self.put("docs/sample.md", "[goals](/docs/product/goals.md)\n")
        self.assertEqual(check(self.root), [])

    def test_escape_link(self):
        self.put("README.md", "[outside](../outside.md)\n")
        self.assertTrue(any("escapes repository" in e for e in check(self.root)))

    def test_external_anchor_and_code_are_ignored(self):
        self.put("README.md", """# Fixture
[web](https://example.com/)
[mail](mailto:example@example.com)
[anchor](#fixture)
`[inline](missing.md)`
```markdown
[example](missing.md)
```
~~~~
[example](missing.md)
~~~~
""")
        self.assertEqual(check(self.root), [])

    def test_link_after_fence_is_checked(self):
        self.put("README.md", "```md\n[example](missing.md)\n```\n[real](missing.md)\n")
        errors = check(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("README.md:4", errors[0])

    def test_initialized_rejects_project_placeholders(self):
        self.put("docs/product/goals.md", "{{PROJECT_NAME}}\n")
        self.assertEqual(check(self.root), [])
        self.assertTrue(any("unresolved project placeholder" in e
                            for e in check(self.root, initialized=True)))

    def test_template_placeholders_remain_allowed(self):
        self.put("docs/templates/feature-spec.md", "{{FEATURE_NAME}}\n")
        self.put("docs/templates/runbook.md", "{{RUNBOOK_OWNER}}\n")
        self.assertEqual(check(self.root, initialized=True), [])

    def test_observability_assets_are_required(self):
        for name in ("docs/specs/observability.md", "docs/architecture/observability.md",
                     "docs/acceptance/observability.md", "docs/templates/runbook.md",
                     "docs/operations/runbooks/README.md"):
            with self.subTest(name=name):
                (self.root / name).unlink()
                self.assertIn(f"missing required file: {name}", check(self.root))
                self.put(name, "fixture\n")

    def test_initialized_rejects_observability_placeholders(self):
        for name in ("docs/architecture/observability.md", "docs/acceptance/observability.md",
                     "docs/operations/runbooks/test-alert.md"):
            with self.subTest(name=name):
                self.put(name, "{{OBS_OWNER}}\n")
                self.assertEqual(check(self.root), [])
                self.assertIn(f"{name}:1: unresolved project placeholder",
                              check(self.root, initialized=True))
                self.put(name, "configured\n")

    def test_observability_document_links_are_checked(self):
        for name in ("docs/operations/runbooks/test-alert.md",
                     "docs/acceptance/test-flow.md", "tests/acceptance/test-flow.md"):
            with self.subTest(name=name):
                self.put(name, "[missing](missing.md)\n")
                self.assertTrue(any(f"{name}:1: missing local link target" in e
                                    for e in check(self.root)))
                self.put(name, "fixture\n")

    def test_documentation_indexes_are_required(self):
        for name in ("docs/README.md", "docs/acceptance/README.md"):
            with self.subTest(name=name):
                (self.root / name).unlink()
                self.assertIn(f"missing required file: {name}", check(self.root))
                self.put(name, "fixture\n")

    def test_old_layout_does_not_satisfy_required_files(self):
        (self.root / "docs/product/goals.md").unlink()
        self.put("product/goals.md", "legacy document\n")
        self.assertIn("missing required file: docs/product/goals.md", check(self.root))

    def test_links_between_docs_contracts_and_tests(self):
        self.put("docs/acceptance/example.md",
                 "[tests](../../tests/acceptance/README.md)\n"
                 "[contract](../../contracts/api/README.md)\n")
        self.put("tests/acceptance/README.md",
                 "[plan](../../docs/acceptance/example.md)\n")
        self.assertEqual(check(self.root), [])

    def test_initialized_checks_test_directory_readmes(self):
        self.put("tests/acceptance/README.md", "{{TEST_COMMAND}}\n")
        self.assertIn("tests/acceptance/README.md:1: unresolved project placeholder",
                      check(self.root, initialized=True))

    def test_commented_owners_do_not_count(self):
        self.put(".github/CODEOWNERS", "# * @someone\n")
        self.assertEqual(check(self.root), [])
        self.assertTrue(any("active owner rule" in e
                            for e in check(self.root, initialized=True)))

    def test_cli_failure_exit_status(self):
        (self.root / "docs/product/goals.md").unlink()
        script = Path(__file__).resolve().parents[1] / "check_project.py"
        result = subprocess.run([sys.executable, str(script), "--root", str(self.root)],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing required file", result.stderr)


if __name__ == "__main__":
    unittest.main()
