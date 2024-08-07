import csv, TransactionInterface, TransactionInfo, datetime

class TransactionAccess(TransactionInterface.TransactionInterface):
    """
    Provides the functionality necessary to import and return transaction 
    data. The user provided data is stored in an internal csv file that
    is always accessible to the system.
    """
    def __init__(self):
        self.__transactionPath = 'transactionFile.csv'
        
    def importTransactions(self, filePath: str) -> bool:
        try:
            # Opens the users transaction file and the internal transaction file
            with open(filePath, "r") as transactionFile, open("transactionFile.csv", 'w', newline='') as newTransaction: 
                writer = csv.writer(newTransaction)
                reader = csv.reader(transactionFile)
                # Skips the header line
                next(reader, None) 
                totalTransactions = 0
                for transaction in reader:
                    totalTransactions += 1
                    writer.writerow(transaction)
            return totalTransactions
        except FileNotFoundError as e:
            print("File does not exist.", e)
        except Exception as e:
            print("An error has occured.", e)
        
    def getTransactions(self, startDate: datetime.datetime, endDate: datetime.datetime) -> list:
        try:
            transactionList = []
            # Opens the internal transaction file
            with open(self.__transactionPath, 'r') as transactions: 
                reader = csv.reader(transactions)
                for row in transactions:
                    # Splits the row 
                    splitRow = row.split(",") 
                    # Splits the date
                    dateSplit = splitRow[0].split("/") 
                    # Removes whitespace
                    splitRow[2] = splitRow[2].strip() 
                    # Creates date
                    dateCheck = datetime.datetime(int(dateSplit[2]), int(dateSplit[1]), int(dateSplit[0])) 
                    # Checks if the date is within the parameters
                    if dateCheck >= startDate and dateCheck <= endDate: 
                        # Creates TransactionInfo Object
                        transaction = TransactionInfo.TransactionInfo(dateCheck.date(), splitRow[1], splitRow[2]) 
                        transactionList.append(transaction)
            return transactionList
        except ValueError as e:
            print("Incorrect datetime parameter.", e)
        except TypeError as e:
            print("Incorrect parameter type.", e)
        except Exception as e:
            print("An error has occured.", e)