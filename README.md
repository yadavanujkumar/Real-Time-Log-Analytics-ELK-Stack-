# Real-Time Log Analytics with ELK Stack

A complete real-time log analytics pipeline using the ELK Stack (Elasticsearch, Logstash, Kibana) for ingesting, parsing, and visualizing web server logs.

## Overview

This project provides a portfolio-ready setup for building a real-time log analytics pipeline that:
- Generates realistic Apache/Nginx format web server logs
- Parses unstructured logs into structured data using Logstash Grok filters
- Stages data for visualization in Kibana dashboards

## Project Structure

```
├── log_generator.py    # Python script to generate realistic web server logs
├── logstash.conf       # Logstash configuration for parsing logs
├── app.log             # Generated log file (created when running log_generator.py)
├── README.md           # Project documentation
└── LICENSE             # MIT License
```

## Prerequisites

- Python 3.6+
- Logstash 7.x or 8.x
- Elasticsearch 7.x or 8.x (optional, for production)
- Kibana 7.x or 8.x (optional, for visualization)

## Quick Start

### 1. Generate Sample Logs

Run the log generator script to create realistic web server logs:

```bash
python3 log_generator.py
```

This will:
- Create/append to `app.log` in the current directory
- Generate logs in Apache Combined Log Format
- Include randomized IP addresses, request methods, paths, and status codes
- Print logs to console for monitoring

Press `Ctrl+C` to stop log generation.

### 2. Run Logstash

Update the `logstash.conf` file to point to your `app.log` file path:

```bash
# Edit the input.file.path in logstash.conf
path => "/absolute/path/to/app.log"
```

Then run Logstash:

```bash
logstash -f logstash.conf
```

The parsed, structured JSON logs will be displayed in the console.

## Log Format

The generator produces logs in Apache Combined Log Format:

```
192.168.1.1 - - [29/Nov/2025:10:15:30 +0000] "GET /api/v1/users HTTP/1.1" 200 4523 "https://www.google.com" "Mozilla/5.0..."
```

### Fields Generated

| Field | Description | Example |
|-------|-------------|---------|
| IP Address | Client IP (IPv4) | `192.168.1.1` |
| Timestamp | Request timestamp | `29/Nov/2025:10:15:30 +0000` |
| Request Method | HTTP method | `GET`, `POST`, `PUT`, `DELETE` |
| Request Path | URL path | `/api/v1/users` |
| HTTP Version | Protocol version | `HTTP/1.1` |
| Status Code | HTTP response status | `200`, `404`, `500` |
| Response Size | Response body size in bytes | `4523` |
| Referrer | Referring URL | `https://www.google.com` |
| User Agent | Client browser/agent | `Mozilla/5.0...` |

## Logstash Configuration Details

The `logstash.conf` file includes:

### Input
- Reads from the local `app.log` file using the file input plugin

### Filter (Grok Pattern)
Parses the log line into structured fields:
- `client_ip` - Source IP address
- `request_method` - HTTP method (GET, POST, etc.)
- `request_path` - URL path
- `status_code` - HTTP status code (as integer)
- `response_bytes` - Response size (as integer)
- `status_category` - Categorized status (Success, Redirect, Client Error, Server Error)
- `user_agent_parsed` - Parsed user agent information

### Output
- Console output using `rubydebug` codec (structured JSON)
- Elasticsearch output (commented, ready for production)

## Kibana Visualization Plan

The following 5 key visualizations should be created in the Kibana dashboard:

### 1. Request Volume Over Time (Line Chart)
**Purpose:** Monitor traffic patterns and identify peak usage periods
- X-axis: @timestamp
- Y-axis: Count of requests
- Breakdown: By status_category

### 2. Top 10 Status Codes Distribution (Pie/Donut Chart)
**Purpose:** Quickly identify error rates and most common response types
- Metric: Count
- Split by: status_code
- Filter for: 4xx and 5xx errors for error-focused view

### 3. Top Requested Endpoints (Horizontal Bar Chart)
**Purpose:** Identify most accessed resources and potential hotspots
- Metric: Count
- Y-axis: request_path
- Sort: Descending by count

### 4. Geographic Map of Request Origins (Coordinate Map)
**Purpose:** Visualize geographic distribution of traffic
- Location: geoip.location
- Metric: Count
- Note: Requires GeoIP database enabled in Logstash

### 5. Error Rate Dashboard (Gauge + Data Table)
**Purpose:** Real-time error monitoring and alerting threshold
- Gauge: Percentage of 4xx/5xx responses
- Table: Latest errors with client_ip, request_path, status_code, timestamp

### Bonus Visualizations

6. **Request Method Distribution** - Pie chart showing GET vs POST vs other methods
7. **Browser/Device Analytics** - Based on user_agent_parsed fields
8. **Response Time Trends** - If response time is added to logs
9. **Top Client IPs** - Identify heavy users or potential bad actors
10. **Real-time Log Stream** - Discover view with saved search

## Enabling Elasticsearch Output

To send logs to Elasticsearch, uncomment the elasticsearch output in `logstash.conf`:

```ruby
output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "webserver-logs-%{+YYYY.MM.dd}"
    document_type => "_doc"
  }
}
```

## Enabling GeoIP

To enable geographic visualization:

1. Download the GeoLite2 database from MaxMind
2. Uncomment the geoip filter in `logstash.conf`
3. Update the database path if necessary

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details