import xlsxwriter

# Initialize workbook
def init():
    workbook = xlsxwriter.Workbook('fantasy_adds.xlsx')
    overview = workbook.add_worksheet()
    return workbook,overview


def writeToExcel(teams, workbook, overview):
    # Initializing Workbook and Overview sheet
   
    bold = workbook.add_format({'bold': True})
    money_format = workbook.add_format({'num_format': '$0.00'})
    row, col = 0, 0 

    overview.set_column(col, col, 19)

    # Adding Team Names and
    for team in teams: 
        overview.write(row, col, team['name'], bold)
        value = len(team['transactions']) * .25
        overview.write(row, col+1, value, money_format)
        row += 1

    str_format = workbook.add_format({'bold': True})
    str_format.set_align('center')
    overview.write(row+3, col, 'TOTAL:', str_format)
    total = getTotal(teams)

    total_format = workbook.add_format({'num_format': '$#0.00', 'bold': True})
    total_format.set_align('center')
    overview.write(row+3, col+1, total, total_format)
    workbook.close()

