import TransactionAccess, ReportAccess, RuleAccess, datetime, Classification, ReportData, csv

class ReportManager:
    """
    The ReportManager object performs the flow control of all usecases for the system.
    """
    def __init__(self, transactions: TransactionAccess, 
                 rule: RuleAccess, report: ReportAccess, clasify: Classification):
        self.__transactions = transactions
        self.__rule = rule
        self.__report = report
        self.__clasify = clasify
    
    def importTransactions(self, filePath: str) -> bool:
        return self.__transactions.importTransactions(filePath)
    
    def clasifyTransactions(self, startDate: datetime, 
                            endDate: datetime, ruleFileName: str) -> int:
        # Sets the pattern file to the userdefined one.
        self.__rule.importRules(ruleFileName) 
        # Clasifies transactions
        clasifiedData = self.__clasify.clasifyTransactions(
            self.__transactions.getTransactions(startDate, endDate), self.__rule.getRules()) 
        # Adds the clasified data to the report file
        self.__report.addReportData(clasifiedData) 
        totalClasified = 0
        for data in clasifiedData:
            totalClasified += 1
        return totalClasified
    
    def listTransactions(self, startDate: datetime, endDate: datetime, label='') -> int:
        return self.__report.getReport(startDate, endDate, label)
    
    def expenditure(self, startDate: datetime, endDate: datetime) -> dict:
        # Returns all report data within the time parameters.
        reportData = self.__report.getReport(startDate, endDate) 
        expenditureTotal = dict()
        for data in reportData:
            if data.label == '':
                if "Other" not in expenditureTotal:
                    # Creates a new key and value
                    expenditureTotal["Other"] = float(data.amount) 
                else:
                    # Adds to the corresponding key.
                    expenditureTotal["Other"] += float(data.amount) 
            elif data.label == 'Unclassified':
                if "Other" not in expenditureTotal:
                    expenditureTotal["Other"] = float(data.amount)
                else:
                    expenditureTotal["Other"] += float(data.amount)
            else:
                if data.label not in expenditureTotal:
                    expenditureTotal[data.label] = float(data.amount)
                else:
                    expenditureTotal[data.label] += float(data.amount)
        return expenditureTotal