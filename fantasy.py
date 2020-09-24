# This program reads in a transaction table from Yahoo Fantasy Football
# to process and track the # of transactions by each team.
from bs4 import BeautifulSoup
import xlsxwriter

# FIltering specified html tags for BS4
def playerOrTeam(tag):
    return tag.name == 'a' and (tag.has_attr('class') ^ tag.has_attr('target'))

# Initialize the list with team names
def collectTeamNames():
    with open('teams.html', 'r') as f: 
        contents = f.read()
        soup = BeautifulSoup(contents,'html.parser')
        tags = soup.find_all('option')
        [addTeam(tag.string) for tag in tags[1:]]
def addTeam(team):
    ele = {'name': team, 'transactions': []}
    teams.append(ele)

# Collect all transactions from HTML doc 
def getAllTransactions(soup):
    rows = soup.find_all('tr')
    transactions = []
    # iterating through transactions
    for row in rows:
        # Rows are divided into 3 parts, separated by <td> tags:
        # 1. Plus Image
        # 2. The player(s) being added/dropped
        # 3. Team Name and date of transaction
        row_data = [x for x in row.contents if x != '\n']

        # There will only be two iterations, the first 
        contents = str(row_data[1]) + str(row_data[2])
        soup = BeautifulSoup(contents, 'html.parser')
        tags = soup.find_all(playerOrTeam)[:2]
        transactions.append({'player': tags[0].string, 'team': tags[1].string})
    return transactions

def addToTeamLst(teams, transaction):
    for team in teams: 
        if team['name'] == transaction['team']:
            team['transactions'].append(transaction['player'])
            return teams

def assignTransactions(teams, transactions):
    for t in transactions:
        addToTeamLst(teams, t)
    return teams

def getTotal(teams):
    total = 0
    for team in teams:
       total += len(team['transactions'])
    return (total * .25)

def start(files):
    teams = []
    collectTeamNames()
    for file in files: 
        with open('file', 'r') as f:
            # Reading in and parsing the html.
            contents = f.read()
            soup = BeautifulSoup(contents, 'html.parser')
            transactions = getAllTransactions(soup)
            assignTransactions(teams, transactions)
    print(teams['transactions'])
            # Transactions are separated by table row <tr> tag
    
   

