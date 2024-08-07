import pytest, ReportManager, Classification, TransactionAccess, ReportAccess, RuleAccess, csv, TransactionInfo, ReportData
from unittest.mock import mock_open, patch, MagicMock
from io import StringIO
from datetime import datetime

# Testing Classification Methods
def test_clasify():
    patterns = {"coffee": "Food", "shoe": "clothing"}
    transaciton1 = TransactionInfo.TransactionInfo(1/1/2023, "Ted's coffee", '6.5')
    transaciton2 = TransactionInfo.TransactionInfo(1/1/2023, "Moe's Shiny Shoes", '249.99')
    mockData = [transaciton1, transaciton2]
    classification = Classification.Classification()
    reportData = classification.clasifyTransactions(mockData, patterns)
    assert type(reportData) == list
    assert type(reportData[0][0]) == TransactionInfo.TransactionInfo
    assert len(reportData) == 2

# Testing ReportAccess Methods
@pytest.fixture
def fix_reportAcccess():
    return ReportAccess.ReportAccess()

def test_getReport(fix_reportAcccess):
    report = fix_reportAcccess
    mockCsv = """2023-01-10,Maccas,24.99,Unclassified
2023-02-03,Rent,950,Home"""
    mockFilePath = "transactionReport.csv"
    mockOpen = mock_open(read_data=mockCsv)
    with patch("builtins.open", mockOpen):
        reportData = report.getReport(datetime(2023,1,10), datetime(2023,2,3))
        mockOpen.assert_called_once_with(mockFilePath, 'r')

    assert type(reportData) == list
    assert type(reportData[0]) == ReportData.ReportData
    assert len(reportData) == 2
    assert reportData[0].label == "Unclassified"

def test_addReportData(fix_reportAcccess):
    report = fix_reportAcccess
    mockFilePath = "transactionReport.csv"
    mockClasifiedData = [[TransactionInfo.TransactionInfo('2023-02-03', "Moe's Shiny Shoes", '249.99'), "Unclassified"]]
    mockOpen = mock_open()
    with patch("builtins.open", mockOpen):
        report.addReportData(mockClasifiedData)
        mockOpen.assert_called_once_with(mockFilePath,'w', newline='')
        mockTest = mockOpen()
        csvData = ("2023-02-03,Moe's Shiny Shoes,249.99,Unclassified\r\n")

        mockTest.write.assert_called_with(csvData)
    
# Test RuleAccess
@pytest.fixture
def fix_RuleAccess():
    return RuleAccess.RuleAccess()

def test_getRules(fix_RuleAccess):
    rules = fix_RuleAccess
    mockFilePath = "patternFile.csv"
    mockPatterns = "coffee|food|bistro|restaurant|catering|coles|woolworths|iga,Food"
    mockOpen = mock_open(read_data=mockPatterns)
    with patch("builtins.open", mockOpen):
        rulesDict = rules.getRules()
        mockOpen.assert_called_once_with(mockFilePath, "r")

    assert type(rulesDict) == dict
    assert rulesDict["coffee"] == "Food"
    assert len(rulesDict) == 8

def test_importRules(fix_RuleAccess):
    rules = fix_RuleAccess
    inputFilePath = "mockFilePath.csv"
    outputFilePath = "patternFile.csv"
    patternData = ["coffee|food|bistro|restaurant|catering|coles|woolworths|iga,Food"]
    mockOpen = mock_open()
    with patch("builtins.open", mockOpen), patch("csv.reader") as reader, patch("csv.writer") as writer:
        reader.return_value = patternData
        result = rules.importRules(inputFilePath)
        mockOpen.assert_any_call(inputFilePath, "r")
        mockOpen.assert_any_call(outputFilePath, "w", newline='')
        reader.assert_called_once()
        assert result == True
    
# Test TransactionAccess
@pytest.fixture
def fix_transactionAccess():
    return TransactionAccess.TransactionAccess()

def test_getTransactions(fix_transactionAccess):
    transactions = fix_transactionAccess
    mockTransactions = """1/1/2023,Ted's coffee,6.5
1/1/2023,Moe's Shiny Shoes,249.99"""
    mockFilePath = 'transactionFile.csv'
    mockOpen = mock_open(read_data=mockTransactions)   
    with patch("builtins.open", mockOpen):
        testResults = transactions.getTransactions(datetime(2023,1,1), datetime(2023,1,9))
        mockOpen.assert_called_once_with(mockFilePath, 'r')
        
        assert type(testResults) == list
        assert type(testResults[0]) == TransactionInfo.TransactionInfo
        assert len(testResults) == 2
        assert testResults[1].amount == '249.99'


def test_importTransactions(fix_transactionAccess):
    transactions = fix_transactionAccess
    mockTransactions = """1/1/2023,Ted's coffee,6.5
1/1/2023,Moe's Shiny Shoes,249.99"""
    mockFilePath = 'transactions.csv'
    mockOpen = mock_open(read_data=mockTransactions)
    with patch("builtins.open", mockOpen), patch("csv.reader") as reader, patch("csv.writer") as writer:
        testResults = transactions.importTransactions(mockFilePath)
        mockOpen.assert_any_call(mockFilePath, "r")
        mockOpen.assert_any_call("transactionFile.csv", 'w', newline='')
        reader.assert_called_once()
        writerInstance = writer.return_value

# Testing ReportManager
@pytest.fixture
def fix_reportManager():
    return ReportManager.ReportManager(
        TransactionAccess.TransactionAccess(), 
        RuleAccess.RuleAccess(), ReportAccess.ReportAccess(), 
        Classification.Classification())

def test_listTransactions(fix_reportManager):
    manager = fix_reportManager
    mockCsv = """2023-01-10,Maccas,24.99,Unclassified
2023-02-03,Rent,950,Home"""
    mockFilePath = "transactionReport.csv"
    mockOpen = mock_open(read_data=mockCsv)
    with patch("builtins.open", mockOpen):
        reportData = manager.listTransactions(datetime(2023,1,10), datetime(2023,2,3))
        mockOpen.assert_called_once_with(mockFilePath, 'r')

    assert type(reportData) == list
    assert type(reportData[0]) == ReportData.ReportData
    assert len(reportData) == 2
    assert reportData[0].label == "Unclassified"

def test_expenditure(fix_reportManager):
    manager = fix_reportManager
    mockCsv = """2023-01-10,Maccas,24.99,Unclassified
2023-02-03,Rent,950,Home"""
    mockFilePath = "transactionReport.csv"
    mockOpen = mock_open(read_data=mockCsv)
    with patch("builtins.open", mockOpen):
        reportData = manager.expenditure(datetime(2023,1,10), datetime(2023,2,3))
        mockOpen.assert_called_once_with(mockFilePath, 'r')

    assert type(reportData) == dict
    assert reportData["Other"] == 24.99
    assert reportData["Home"] == 950