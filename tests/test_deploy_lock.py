"""Execute the exact remote deployment script against a fake Docker binary."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]


def remote_script():
    workflow = (ROOT / '.github/workflows/deploy-service.yml').read_text()
    return textwrap.dedent(workflow.split("<<'REMOTE_SCRIPT'\n", 1)[1].split('          REMOTE_SCRIPT', 1)[0])


@unittest.skipUnless(shutil.which('flock'), 'requires Linux flock (run in CI or Linux container)')
class DeployLock(unittest.TestCase):
    def test_parallel_deploys_preserve_tags_private_permissions_and_serialize_compose(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            script = root / 'remote.sh'
            script.write_text(remote_script())
            subprocess.run(['bash', '-n', str(script)], check=True)
            (root / '.env').write_text('OTHER=keep\nONE_TAG=old\n')
            # A second Docker invocation while one is active makes the test fail.
            binary = root / 'docker'
            binary.write_text('#!/bin/bash\nset -eu\nmkdir active\ntrap "rmdir active" EXIT\nsleep .1\nprintf "%s\\n" "$*" >> calls\n')
            binary.chmod(0o755)
            env = {**os.environ, 'PATH': str(root) + ':' + os.environ['PATH']}
            commands = [
                ['bash', str(script), directory, 'compose.prod.yaml', 'ONE_TAG', 'sha-one', 'one', 'reader'],
                ['bash', str(script), directory, 'compose.prod.yaml', 'TWO_TAG', 'sha-two', 'two', ''],
            ]
            jobs = [subprocess.Popen(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for command in commands]
            for job in jobs:
                _, stderr = job.communicate(timeout=20)
                self.assertEqual(job.returncode, 0, stderr)
            self.assertEqual(set((root / '.env').read_text().splitlines()), {'OTHER=keep', 'ONE_TAG=sha-one', 'TWO_TAG=sha-two'})
            self.assertEqual((root / '.env').stat().st_mode & 0o777, 0o600)
            self.assertFalse(list(root.glob('.env.*')))
            calls = (root / 'calls').read_text().splitlines()
            self.assertEqual(len(calls), 5)
            self.assertTrue(any('run --rm --no-deps reader' in line for line in calls))


if __name__ == '__main__':
    unittest.main()
