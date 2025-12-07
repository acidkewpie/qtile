import os
import re
import subprocess
import sys


def run_identify_output(backend_name, env=None):
    cmd = os.path.join(os.path.dirname(__file__), "..", "libqtile", "scripts", "main.py")
    argv = [sys.executable, cmd, "identify-output", "--backend", backend_name]

    if env is None:
        env = os.environ.copy()

    proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0, f"Command failed with stderr: {stderr.decode()}"
    stdout = stdout.decode()
    stderr = stderr.decode()
    return (stdout, stderr)


def check_identify_output(stdout, output_name, resolution):
    assert re.search(r"Output 0:", stdout)
    assert re.search(rf"Name:\s+{output_name}", stdout)
    assert re.search(r"Position:\s+\(0,\s*0\)", stdout)
    assert re.search(rf"Resolution:\s+{resolution}", stdout)


def test_identify_output(manager_nospawn):
    backend = manager_nospawn.backend
    stdout, _ = run_identify_output(backend.name, env=backend.env)
    if backend.name == "x11":
        name = "Unknown"
        resolution = "800x600"
    elif backend.name == "wayland":
        name = "HEADLESS-1"
        resolution = "1280x720"
    check_identify_output(stdout, name, resolution)
