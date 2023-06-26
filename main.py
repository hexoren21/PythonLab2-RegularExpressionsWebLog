import paramiko
import re
# Dane do logowania do serwera
host = ''
username = ''
password = ''

# Ścieżka do pliku dziennika
log_path = '/var/log/apache2/access.log.1'

# Tworzenie obiektu klienta SSH
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Tworzenie wyrazenia regularnego
ip_user = r'(?P<IP>\d+\.\d+\.\d+\.\d+)'
data_user = r'(?P<Time>\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})'


try:
    # logowanie do serwera
    client.connect(hostname=host, username=username, password=password)

    # Pobieranie pliku dziennika z serwera
    ftp = client.open_sftp()
    with ftp.file(log_path, 'r') as log_file:
        # Odczytanie linii z pliku dziennika
        for line in log_file: 
            m = re.search(ip_user, line)
            n = re.search(data_user, line)
            if m and n:
                ip = m.group('IP')
                time = n.group('Time')
                print(f'ip {ip} czas {time}')
            else:
                print('')

    # Zamykanie połączenia FTP
    ftp.close()

finally:
    # Zamykanie połączenia SSH
    client.close()