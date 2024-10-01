import subprocess
import re
import csv
import time

def parse_tegrastats(output):
    """Parse the tegrastats output to extract CPU, GPU, and temperature information."""
    # Match CPU usage
    cpu_usage = re.findall(r'CPU \[(.*?)\]', output)
    
    # Match GPU frequency and temperature
    gpu_freq = re.search(r'GR3D_FREQ (\d+)%', output)
    gpu_temp = re.search(r'GPU@(\d+\.\d+)C', output)
    
    # Match CPU temperature
    cpu_temp = re.search(r'CPU@(\d+\.\d+)C', output)

    # Get all CPU usages
    cpu_percentages = ', '.join(cpu_usage) if cpu_usage else "N/A"
    gpu_percentage = gpu_freq.group(1) if gpu_freq else "N/A"
    gpu_temp_value = gpu_temp.group(1) if gpu_temp else "N/A"
    cpu_temp_value = cpu_temp.group(1) if cpu_temp else "N/A"

    return cpu_percentages, gpu_percentage, gpu_temp_value, cpu_temp_value

def log_to_csv(file_name, interval=5):
    """Log GPU, CPU usage, and temperatures to a CSV file."""
    with open(file_name, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write the header
        csvwriter.writerow(['Timestamp', 'CPU Usage', 'GPU Usage (%)', 'GPU Temp (C)', 'CPU Temp (C)'])

        # Start the tegrastats process
        process = subprocess.Popen(['tegrastats', '--interval', '1000'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        try:
            while True:
                # Read line-by-line output from tegrastats
                output = process.stdout.readline()

                # Parse the output
                cpu_usage, gpu_usage, gpu_temp, cpu_temp = parse_tegrastats(output)

                # Write data to CSV
                csvwriter.writerow([time.strftime('%Y-%m-%d %H:%M:%S'), cpu_usage, gpu_usage, gpu_temp, cpu_temp])
                
                print(f"Logged at {time.strftime('%Y-%m-%d %H:%M:%S')} -> CPU: {cpu_usage}, GPU Usage: {gpu_usage}%, GPU Temp: {gpu_temp}C, CPU Temp: {cpu_temp}C")
                
                # Wait for the next interval
                time.sleep(interval)

        except KeyboardInterrupt:
            print("Logging stopped.")
        finally:
            # Terminate tegrastats process on exit
            process.terminate()

# Call the function to log data to CSV file
log_to_csv('gpu_cpu_stats.csv', interval=1)  # Logging every 5 seconds
