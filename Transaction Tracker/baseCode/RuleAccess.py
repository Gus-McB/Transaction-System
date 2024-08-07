import csv, RuleInterface

class RuleAccess(RuleInterface.RuleInterface):
    """
    Provides the necessary functionality to access and import the 
    clasification patterns/rules provided by the user prior to 
    clasification of transaction data.
    """
    def __init__(self):
        self.__ruleFile = "patternFile.csv"
    
    def importRules(self, filePath: str) -> bool:
        # Reads from the userdefined file and writes it to the internal rule file
        try:
            with open(filePath, "r") as patternFile, open("patternFile.csv", 'w', newline='') as newPattern: 
                writer = csv.writer(newPattern)
                reader = csv.reader(patternFile)
                for pattern in reader:
                    writer.writerow(pattern)
            return True
        except FileNotFoundError as e:
            print("File not accessible using provided file path.", e)
        except Exception as e:
            print("An error has occured.", e)

    def getRules(self) -> dict:
        patternDict = dict()
        # Reads the internal pattern file
        try:
            with open (self.__ruleFile, "r") as patterns: 
                reader = csv.reader(patterns)
                for row in reader:
                    # Splits by '|' to create each key
                    row[0] = row[0].split("|") 
                    for name in row[0]:
                        # Creates each new key and value pair
                        patternDict[name] = row[1] 
            return patternDict
        except FileNotFoundError as e:
            print("File does not exists.", e)
        except Exception as e:
            print("An error has occured", e)