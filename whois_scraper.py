import subprocess

def get_whois_info(domain):
    result = subprocess.run(['whois', domain], capture_output=True, text=True)
    output = result.stdout

    whois_data = {
        "Registrar Info": {},
        "Important Dates": {},
        "Name Servers": [],
        "Updated Date": "",
        "Status Notes": [],
    }

    for line in output.splitlines():
        line = line.strip()
        if line.startswith("Registrar:"):
            whois_data["Registrar Info"]["Name"] = line.split(":")[1].strip()
        elif line.startswith("Updated Date:"):
            whois_data["Important Dates"]["Updated On"] = line.split(":")[1].strip()
        elif line.startswith("Creation Date:"):
            whois_data["Important Dates"]["Registered On"] = line.split(":")[1].strip()
        elif line.startswith("Registry Expiry Date:"):
            whois_data["Important Dates"]["Expires On"] = line.split(":")[1].strip()
        elif line.startswith("Name Server:"):
            whois_data["Name Servers"].append(line.split(":")[1].strip())
        elif line.startswith("Domain Status:"):
            status = line.split(":")[1].strip()
            if status.startswith("clientHold"):
                whois_data["Status Notes"].append("網域過期或網域有異常")
            elif status.startswith("serverHold"):
                whois_data["Status Notes"].append("禁止解析該域名")
            if "Status" not in whois_data["Registrar Info"]:
                whois_data["Registrar Info"]["Status"] = []
            whois_data["Registrar Info"]["Status"].append(status)
        elif line.startswith(">>> Last update of whois database:"):
            whois_data["Updated Date"] = line.split(":")[1].strip()

    if "Status" in whois_data["Registrar Info"]:
        whois_data["Registrar Info"]["Status"] = ", ".join(whois_data["Registrar Info"]["Status"])

    return whois_data
