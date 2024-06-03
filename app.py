from flask import Flask, request, render_template
from whois_scraper import get_whois_info

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    whois_results = {}
    if request.method == 'POST':
        domains = request.form['domains']
        domain_list = [domain.strip() for domain in domains.split('\n') if domain.strip()]
        for domain in domain_list:
            whois_results[domain] = get_whois_info(domain)
    return render_template('index.html', whois_results=whois_results)

if __name__ == '__main__':
    app.run(debug=True)
