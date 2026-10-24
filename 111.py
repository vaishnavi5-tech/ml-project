import subprocess
import re

# Run smartctl command
cmd = ["smartctl", "-a", "/dev/sda"]  # change to /dev/nvme0 if needed

result = subprocess.run(
    cmd,
    capture_output=True,
    text=True,
    shell=False
)

# Combine outputs (important for Windows)
output = result.stdout + result.stderr
print(output)
exit(1)