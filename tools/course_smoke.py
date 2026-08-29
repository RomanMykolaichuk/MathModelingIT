from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

EXPECTED_LESSONS = [
    't1_l1','t1_l2','t1_l3','t1_l4',
    't2_l1','t2_l2','t2_l3','t2_l4','t2_l5','t2_l6','t2_l7',
]
REQUIRED_FILES = [
    'README.md',
    'assignment.md',
    'instructor_notes.md',
    'notebooks/demo.ipynb',
    'notebooks/practice.ipynb',
    'src/model.py',
]


def run(cmd: list[str], cwd: Path, env: dict[str, str] | None = None) -> dict:
    merged_env = os.environ.copy()
    merged_env.setdefault('MPLBACKEND', 'Agg')
    if env:
        merged_env.update(env)
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        env=merged_env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return {'returncode': proc.returncode, 'output': proc.stdout}


def check_structure(root: Path) -> list[dict]:
    results = []
    lessons_root = root / 'lessons'
    existing = sorted(p.name for p in lessons_root.iterdir() if p.is_dir()) if lessons_root.exists() else []
    for lesson in EXPECTED_LESSONS:
        lesson_root = lessons_root / lesson
        missing = [rel for rel in REQUIRED_FILES if not (lesson_root / rel).exists()]
        has_tests = (lesson_root / 'tests').is_dir() and any((lesson_root / 'tests').glob('test_*.py'))
        has_experiment = (lesson_root / 'src' / 'experiment.py').exists()
        results.append({
            'lesson': lesson,
            'exists': lesson in existing,
            'missing_required': missing,
            'has_tests': has_tests,
            'has_experiment': has_experiment,
            'ok': lesson in existing and not missing and has_tests and has_experiment,
        })

    manifest = (root / 'course_manifest.yaml').read_text(encoding='utf-8')
    stable_count = len(re.findall(r'^\s*status:\s*content_stable\s*$', manifest, flags=re.MULTILINE))
    results.append({'check': 'manifest_content_stable_count', 'value': stable_count, 'expected': 11, 'ok': stable_count == 11})

    capstone_required = [
        'README.md','CAPSTONE_TASK.md','RUBRIC.md','RESEARCH_PROTOCOL.md',
        'experiment_config.json','data/observations.csv','notebooks/capstone_demo.ipynb',
        'src/model.py','src/experiment.py','tests/test_capstone.py',
    ]
    capstone_missing = [rel for rel in capstone_required if not (root / 'capstone' / rel).exists()]
    results.append({'check': 'capstone_structure', 'missing': capstone_missing, 'ok': not capstone_missing})
    return results


def run_tests(root: Path) -> list[dict]:
    results = []
    targets = [root / 'lessons' / x / 'tests' for x in EXPECTED_LESSONS] + [root / 'capstone' / 'tests']
    for target in targets:
        result = run([sys.executable, '-m', 'pytest', '-q', str(target)], cwd=root)
        results.append({
            'target': str(target.relative_to(root)),
            'returncode': result['returncode'],
            'ok': result['returncode'] == 0,
            'output': result['output'][-5000:],
        })
    return results


def execute_notebook(path: Path, root: Path, timeout: int) -> dict:
    import nbformat
    from nbclient import NotebookClient

    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name='python3',
        resources={'metadata': {'path': str(path.parent)}},
        allow_errors=False,
    )
    old_backend = os.environ.get('MPLBACKEND')
    old_pythonpath = os.environ.get('PYTHONPATH')
    os.environ['MPLBACKEND'] = 'Agg'
    os.environ['PYTHONPATH'] = str(root) + (os.pathsep + old_pythonpath if old_pythonpath else '')
    try:
        client.execute()
        return {'notebook': str(path.relative_to(root)), 'ok': True, 'error': None}
    except Exception as exc:
        return {'notebook': str(path.relative_to(root)), 'ok': False, 'error': repr(exc)}
    finally:
        if old_backend is None:
            os.environ.pop('MPLBACKEND', None)
        else:
            os.environ['MPLBACKEND'] = old_backend
        if old_pythonpath is None:
            os.environ.pop('PYTHONPATH', None)
        else:
            os.environ['PYTHONPATH'] = old_pythonpath


def run_notebooks(root: Path, timeout: int) -> list[dict]:
    paths = [root / 'lessons' / x / 'notebooks' / 'demo.ipynb' for x in EXPECTED_LESSONS]
    paths.append(root / 'capstone' / 'notebooks' / 'capstone_demo.ipynb')
    return [execute_notebook(path, root, timeout) for path in paths]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--skip-tests', action='store_true')
    parser.add_argument('--skip-notebooks', action='store_true')
    parser.add_argument('--timeout', type=int, default=180)
    parser.add_argument('--report', type=Path, default=Path('course_smoke_report.json'))
    args = parser.parse_args()
    root = args.root.resolve()

    report = {'root': str(root)}
    report['structure'] = check_structure(root)
    if not args.skip_tests:
        report['tests'] = run_tests(root)
    if not args.skip_notebooks:
        report['notebooks'] = run_notebooks(root, args.timeout)

    failures = []
    for item in report['structure']:
        if not item.get('ok', False):
            failures.append(item)
    for group in ('tests', 'notebooks'):
        for item in report.get(group, []):
            if not item.get('ok', False):
                failures.append(item)

    report['ok'] = not failures
    report['failure_count'] = len(failures)
    report_path = args.report if args.report.is_absolute() else root / args.report
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f"Course smoke: {'PASS' if report['ok'] else 'FAIL'}; failures={len(failures)}")
    for item in failures:
        print(json.dumps(item, ensure_ascii=False)[:2000])
    print(f"Report: {report_path}")
    return 0 if report['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
