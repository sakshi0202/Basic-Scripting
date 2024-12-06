import re
import subprocess
LOG_FILE = "/var/log/auth.log"  # Path to the log file
THRESHOLD = 5  # Number of failed attempts before blocking
BLOCKED_IPS_FILE = "/var/log/blocked_ips.txt"  # File to keep track of blocked Ips
def get_failed_login_ips():
    """Parse the log file and return a dictionary of IPs with failed login attempts."""
    failed_ips = {}
    with open(LOG_FILE, "r") as file:
        for line in file:
            ip = line.split()[0]  # Extract IP address            # Detect failed login attempts due to "unknown user"
            if "wp-login.php" in line and "unknown user" in line:
                failed_ips[ip] = failed_ips.get(ip, 0) + 1            # Additional checks for "invalid username"
            elif "wp-login.php" in line and "invalid username" in line:
                failed_ips[ip] = failed_ips.get(ip, 0) + 1    return failed_ipsdef block_ip(ip):
    """Block an IP using iptables."""
    try:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        print(f"Blocked IP: {ip}")
        with open(BLOCKED_IPS_FILE, "a") as file:
            file.write(ip + "\n")
    except subprocess.CalledProcessError as e:
        print(f"Error blocking IP {ip}: {e}")def main():
    """Main function to monitor logs and block offending IPs."""
 failed_ips = get_failed_login_ips()    # Read already blocked IPs to avoid reblocking
    try:
        with open(BLOCKED_IPS_FILE, "r") as file:
            blocked_ips = set(file.read().splitlines())
    except FileNotFoundError:
        blocked_ips = set()    # Check and block IPs exceeding the threshold
    for ip, count in failed_ips.items():
        if count >= THRESHOLD and ip not in blocked_ips:
            block_ip(ip)if __name__ == "__main__":
    main()
