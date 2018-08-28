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
FILE_INPUT_DOMAINS = 'in/proxy_endpoints'
# Output file: expiration date of cert. from current day
FILE_OUT_TODAY = 'out/proxy_today'
# Output file: expiration date of cert. from day before (useful for comparison)
FILE_OUT_YESTERDAY = 'out/proxy_yesterday'

proxy = 'http://SVCESBTST:6FPD1KIc@bluecoat.media-saturn.com:80'

os.environ['http_proxy'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['HTTPS_PROXY'] = proxy

"""
PROXY_HOST = 'bluecoat.media-saturn.com'
PROXY_PORT = 80
PROXY_USER = 'SVCESBTST'
PROXY_PASS = '6FPD1KIc'
"""

u = FileUtils()

# Backup file from yesterday for comparison
u.remove_file(FILE_OUT_YESTERDAY)
u.rename_file(FILE_OUT_TODAY, FILE_OUT_YESTERDAY)

# Open files
f_input = u.open_file(FILE_INPUT_DOMAINS, "r")
f_output_today = u.open_file(FILE_OUT_TODAY, "w")
f_output_yesterday = u.open_file(FILE_OUT_YESTERDAY, "r")

# Prepare format of output
u.format_file(f_output_today)


# Parse domains from input file
for domain in f_input.readlines():

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
f_output_today_read = u.open_file(FILE_OUT_TODAY, "r")

# Comparison between 'today' and 'yesterday', to see if a certificate has changed
file_today_text = f_output_today_read.readlines()
file_yesterday_text = f_output_yesterday.readlines()
u.compare_content(file_yesterday_text, file_today_text)


# Close file descriptors
f_output_today_read.close()
f_output_yesterday.close()

os.environ['http_proxy'] = ""
os.environ['https_proxy'] = ""
os.environ['HTTP_PROXY'] = ""
os.environ['HTTPS_PROXY'] = ""


