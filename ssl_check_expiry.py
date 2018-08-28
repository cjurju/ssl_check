import ssl
import socket
import OpenSSL
import time
import os
import shutil
import difflib
import filecmp
from utils.utils_file import FileUtils

# Input file - format <domain>:<port>
file_input_domains = 'in/endpoints'
# Output file: expiration date of cert. from current day
file_out_today = 'out/today'
# Output file: expiration date of cert. from day before (useful for comparison)
file_out_yesterday = 'out/yesterday'


u = FileUtils()

# Backup file from yesterday for comparison
u.remove_file(file_out_yesterday)
u.rename_file(file_out_today, file_out_yesterday)

# Open files
f_input = u.open_file(file_input_domains, "r")
f_output_today = u.open_file(file_out_today, "w")
f_output_yesterday = u.open_file(file_out_yesterday, "r")

# Prepare format of output
u.format_file(f_output_today)


# Parse domains from input file
for domain in f_input.readlines():
    if domain == "":
        continue

    # Get certificate
    cert = ssl.get_server_certificate((domain.strip(), 443))
    x509 = OpenSSL.crypto.load_certificate(
        OpenSSL.crypto.FILETYPE_PEM, cert)

    # Format date of expiry
    struct_time = time.strptime(x509.get_notAfter().decode('ascii'),'%Y%m%d%H%M%SZ')
    time_formatted = time.strftime("%d %b %Y %H:%M:%S", struct_time)

    # Write expiry data to file
    f_output_today.write(domain.strip().ljust(60, ' ') + time_formatted + '\n')


# Close file descriptor opened in write mode
f_output_today.close()

# Compare content of files 'today' and 'yesterday'
f_output_today_read = u.open_file(file_out_today, "r")

# Comparison between 'today' and 'yesterday', to see if a certificate has changed
file_today_text = f_output_today_read.readlines()
file_yesterday_text = f_output_yesterday.readlines()
u.compare_content(file_yesterday_text, file_today_text)


# Close file descriptors
f_output_today_read.close()
f_output_yesterday.close()


