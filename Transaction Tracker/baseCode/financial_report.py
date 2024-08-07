import click, ReportManager, TransactionAccess, ReportAccess, RuleAccess, Classification
from datetime import datetime


DATE_FORMAT='%Y-%m-%d'

arg_start_date = click.argument('start_date', type=click.DateTime(formats=[DATE_FORMAT]), metavar='START_DATE')
arg_end_date   = click.argument('end_date', type=click.DateTime(formats=[DATE_FORMAT]), metavar='END_DATE', 
                                default=datetime.now().strftime(DATE_FORMAT))
reportManager = ReportManager.ReportManager(
    TransactionAccess.TransactionAccess(), 
    RuleAccess.RuleAccess(), ReportAccess.ReportAccess(), Classification.Classification())
@click.group()
def cli():
    pass

#
# Each of the functions below is the entry point of a use case for the command line application.
# Call your code from each of these functions, but do not include all of your code in the functions
# in this file.
#

@cli.command(name='import')
@click.argument('transactions_file', type=click.Path(exists=True, dir_okay=False))
def transactions_import_command(transactions_file):
    """Imports the transactions from a file."""

    # TODO add your code here   
    try:
        total = reportManager.importTransactions(transactions_file)
    except:
        raise NotImplementedError
    print("Imported ", total, " transactions.")

@cli.command(name='classify')
@click.option('--rules', type=click.Path(exists=True, dir_okay=False), 
              help='CSV file containing the classification rules')
@arg_start_date
@arg_end_date
def classify_command(rules, start_date, end_date):
    """Classifies each transaction in a time period."""

    # TODO add your code here   
    try:
       clasify = Classification.Classification()
       total = reportManager.clasifyTransactions(start_date, end_date, rules)
       clasifiedData = reportManager.listTransactions(start_date, end_date)
       for data in clasifiedData:
            if data.label != ' ' and data.label != 'Unclassified':
                print(f"{data.date} {data.description}: {data.amount} clasified as {data.label}")
            else: 
                print(f"{data.date} {data.description}: {data.amount} unable to clasify") 
    except:
        raise NotImplementedError
    print(total, " transactions processed.")
    
    

@cli.command(name='list')
@click.option('--label',
              help=("Output transactions corresponding to this label only. " 
                    "Use 'None' to show unlabelled transactions. "
                    "If not set, all transactions are shown."))
@arg_start_date
@arg_end_date
def list_command(label, start_date, end_date):
    """Lists transactions corresponding to a given label in a time period."""

    # TODO add your code here
    try:
        listData = reportManager.listTransactions(start_date, end_date, label)
        for data in listData:
            if data.label != ' ' and data.label != 'Unclassified':
                print(f"{data.date} {data.description}: {data.amount} [{data.label}]")
            else:
                print(f"{data.date} {data.description}: {data.amount} []")
    except:
        raise NotImplementedError

@cli.command(name='report')
@arg_start_date
@arg_end_date
def report_command(start_date, end_date):
    """Summarises expenditure in a period of time."""

    # TODO add your code here  
    try:
        reportTotal = reportManager.expenditure(start_date, end_date)
        for report in reportTotal:
            print(f"{report}: {reportTotal[report]}")
    except:
        raise NotImplementedError

if __name__ == '__main__':
    cli()
