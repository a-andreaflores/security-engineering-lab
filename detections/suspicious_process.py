import subprocess

result = subprocess.run(
    ["ps", "-eo", "user,pid,ppid,cmd"],
    capture_output=True,
    text=True
)

for line in result.stdout.splitlines():
    if "nc " in line:
        print("ALERT: Possible netcat process detected")
        print(f"Process details: {line}")
