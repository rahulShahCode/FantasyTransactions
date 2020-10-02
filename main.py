from yahoo_oauth import OAuth2
import xml.etree.ElementTree as ET 
import pandas as pd 

def getXML(oauth, url, xpath):
    teams = []
    r = oauth.session.get(url)
    print(r.status_code)
    root = ET.fromstring(r.text)
    return root.findall(xpath)

def getTeams(xml, ns):
    teams = {} 
    for t in xml:
        teams[t.find(f'.//{ns}name').text] = 0
    return teams

def processTransactions(teams, xml, ns):
    total = 0
    for t in xml:
        if t[0].text == 'add':
            teams[t[4].text] += 1
    for team in teams: 
       teams[team] = '{:.2f}'.format(teams[team] * .25 )
       total += float(teams[team])
    return total

def swap(teams, j):
    temp = teams[j]
    teams[j] = teams[j+1]
    teams[j+1] = temp

# Sort by Team Name 
def alphabetize(teams):
    n = len(teams)
    for i in range(n-1):
        for j in range(n-i-1):
            if teams[j] > teams[j+1]:
                swap(teams, j)
    return teams
def write(names, values):
    df = pd.DataFrame(values, index=pd.Index(names), columns=[''])
    print(df)
        
def getVals(teams, names):
    values = []
    for name in names:
        values.append('$' + teams[name])
    return values
# URLs for API Requests
league_id = 'nfl.l.925422'
url = f'https://fantasysports.yahooapis.com/fantasy/v2/leagues;league_keys={league_id}'
transactions_url = '/transactions;type=add'
teams_url = '/teams'

# OAuth Initialization 
oauth = OAuth2(None, None, from_file='oauth2.json')

# XML Parsing 
ns = '{http://fantasysports.yahooapis.com/fantasy/v2/base.rng}'
teams = f'.//{ns}league/{ns}teams//{ns}team'
transactions = f'.//{ns}league/{ns}transactions//{ns}transaction//{ns}players//{ns}transaction_data'

teams_xml = getXML(oauth, url + teams_url, teams)
transactions_xml = getXML(oauth, url + transactions_url, transactions)

# More XML parsing to gather team names and transaction details 
teams = getTeams(teams_xml, ns)
total = processTransactions(teams, transactions_xml, ns)


names = alphabetize(list(teams.keys()))
values = getVals(teams, names)

write(names, values)
print('\tTOTAL: ' + '${:.2f}'.format(total))