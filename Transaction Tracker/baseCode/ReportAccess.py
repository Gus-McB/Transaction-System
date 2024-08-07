import csv, TransactionInfo, datetime, ReportData, ReportInterface

class ReportAccess(ReportInterface.ReportInterface):
    """
    The report access component allows the user to access all clasified
    data. The addReportData method allows the user to write to the internal 
    storage for the system. GetReport returns the specified data between the 
    given parameters.
    """
    def __init__(self):
        self.__reportPath = "transactionReport.csv"

    def addReportData(self, clasifiedData: list) -> bool:
        # Opens the transactionReport file.
        try:
            with open(self.__reportPath, "w", newline='') as report: 
                writer = csv.writer(report)
                # Loops over the clasifiedData list
                for transaction in clasifiedData: 
                    # Format row
                    row = [str(transaction[0].date), transaction[0].description, transaction[0].amount, transaction[1]] 
                    writer.writerow(row) 
        except ValueError:
            print("Incorrect value passed in as a parameter.")
        except TypeError:
            print("Parameter type invalid.")
        except Exception:
            print("An error has occured.")
    
    def getReport(self, startDate: datetime.datetime, endDate: datetime.datetime, label='') -> list:
        try:
            reportDataList = []
            with open(self.__reportPath, 'r') as report:
                reader = csv.reader(report)
                for transaction in reader:
                    # Checks date is within the date parameters
                    transactionDate = transaction[0].split("-")
                    transactionDate = datetime.datetime(int(transactionDate[0]), int(transactionDate[1]), int(transactionDate[2]))
                    if transactionDate >= startDate and transactionDate <= endDate: 
                        if label == 'Unclassified':
                            if transaction[3] == 'Unclassified':
                                # Appends unclasified ReportData
                                reportDataList.append(ReportData.ReportData(transaction[0], transaction[1], transaction[2], ""))
                        elif label == '':
                            reportDataList.append(ReportData.ReportData(transaction[0], transaction[1], transaction[2], transaction[3]))
                        else:
                            if transaction[3] == label:
                                # Appends the ReportData that has a matching label
                                reportDataList.append(ReportData.ReportData(transaction[0], transaction[1], transaction[2], transaction[3])) 
                            elif label == None: 
                                # Appends all ReportData if label is None.
                                reportDataList.append(ReportData.ReportData(transaction[0], transaction[1], transaction[2], transaction[3])) 

            return reportDataList
        except FileNotFoundError as e:
            print("File path is invalid.", e)
        except Exception as e:
            print("An error has occured.", e)