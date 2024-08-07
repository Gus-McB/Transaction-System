import ClassificationInterface

class Classification(ClassificationInterface.ClassificationInterface):
    """
    The classification class provides the necessary functionality to clasify
    transactions using the information provided in the description of the 
    transaction. Using user defined patterns, the clasifyTransactions method 
    searches through the transaction data and assigns a label to each transaction.
    """
    def __init__(self):
        pass

    def clasifyTransactions(self, transactionData: list, patterns: dict) -> list:
        try:
            clasifiedTransactionList = []
            for transaction in transactionData:
                # Removes capitals and splits the description
                descriptionList = transaction.description.lower().split(" ") 
                isValidTransaction = False
                label = 'Unclassified'
                for item in descriptionList: 
                    # Checks if the word is contained in the dictionary
                    if item in patterns: 
                        isValidTransaction = True
                        # Assigns appropriate label
                        label = patterns[item] 
                # Checks if the transaction can be labelled
                if isValidTransaction == True: 
                    # Appends the List containing the transaction and label
                    clasifiedTransactionList.append([transaction, label]) 
                else: 
                    # Appends the list containing the transaction and 'unclassified' label
                    clasifiedTransactionList.append([transaction, label]) 
            return clasifiedTransactionList
        except TypeError as e:
            print("Incorrect parameter Type.", e)
        except ValueError as e:
            print("Incorrect value was passed in.", e)
        except Exception as e:
            print("An error occurred", e)