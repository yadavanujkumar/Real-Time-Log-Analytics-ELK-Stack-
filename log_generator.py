#!/usr/bin/env python3
"""
Log Generator Script for Real-Time Log Analytics Pipeline
Generates realistic Apache/Nginx format web server logs continuously.
"""

import random
import time
from datetime import datetime


# Sample data for generating realistic logs
IP_ADDRESSES = [
    "192.168.1.1", "10.0.0.45", "172.16.0.100", "203.0.113.50",
    "198.51.100.25", "192.0.2.75", "8.8.8.8", "1.1.1.1",
    "45.33.32.156", "104.16.132.229", "151.101.1.69", "199.232.68.133",
    "185.199.108.154", "140.82.113.4", "52.216.17.225", "54.239.28.85"
]

REQUEST_METHODS = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"]

# Request paths with weighted probability
REQUEST_PATHS = [
    "/", "/index.html", "/about", "/contact", "/products",
    "/api/v1/users", "/api/v1/orders", "/api/v1/products",
    "/images/logo.png", "/css/style.css", "/js/app.js",
    "/login", "/logout", "/register", "/dashboard",
    "/admin", "/search?q=test", "/404", "/error"
]

# Status codes with weighted distribution (200 most common, some errors)
STATUS_CODES = [
    200, 200, 200, 200, 200, 200, 200, 200,  # 80% success
    201, 204, 301, 302, 304,  # Other success/redirects
    400, 401, 403, 404, 404, 404,  # Client errors
    500, 502, 503  # Server errors
]

# User agents for realistic logs
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Safari/605.1.15",
    "curl/7.88.1",
    "python-requests/2.31.0",
    "Googlebot/2.1 (+http://www.google.com/bot.html)"
]

# HTTP versions
HTTP_VERSIONS = ["HTTP/1.0", "HTTP/1.1", "HTTP/2"]


def get_response_size(status_code):
    """Generate a realistic response size based on status code."""
    if status_code in [204, 304]:
        return 0
    if status_code >= 400:
        return random.randint(100, 500)
    return random.randint(500, 50000)


def generate_log_line():
    """Generate a single Apache Combined Log Format line."""
    ip = random.choice(IP_ADDRESSES)
    timestamp = datetime.now().strftime("%d/%b/%Y:%H:%M:%S %z")
    # Add timezone offset if not present
    if not timestamp.endswith("+0000") and len(timestamp) < 26:
        timestamp = datetime.now().strftime("%d/%b/%Y:%H:%M:%S") + " +0000"
    
    method = random.choice(REQUEST_METHODS)
    path = random.choice(REQUEST_PATHS)
    http_version = random.choice(HTTP_VERSIONS)
    status_code = random.choice(STATUS_CODES)
    response_size = get_response_size(status_code)
    referrer = random.choice(["-", "https://www.google.com", "https://example.com"])
    user_agent = random.choice(USER_AGENTS)
    
    # Apache Combined Log Format
    log_line = (
        f'{ip} - - [{timestamp}] '
        f'"{method} {path} {http_version}" '
        f'{status_code} {response_size} '
        f'"{referrer}" "{user_agent}"'
    )
    
    return log_line


def main():
    """Main function to continuously generate logs."""
    log_file = "app.log"
    print(f"Starting log generation to {log_file}...")
    print("Press Ctrl+C to stop.")
    
    try:
        with open(log_file, "a", buffering=1) as f:  # Line buffering
            while True:
                log_line = generate_log_line()
                f.write(log_line + "\n")
                print(log_line)  # Also print to console for monitoring
                
                # Random delay between 0.1 and 2 seconds for realistic traffic
                time.sleep(random.uniform(0.1, 2.0))
                
    except KeyboardInterrupt:
        print("\nLog generation stopped.")


if __name__ == "__main__":
    main()
