#------------------------------------------#
# Title: Assignment06.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# AHernandez, 2021-Feb-20, Modified File Organized SoC Structure and added Docstrings to functions
#------------------------------------------#
import pathlib 
import pickle
# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object
strErrorType= ''
blnErrorflag = False

# -- PROCESSING -- #
class DataProcessor:
    
    @staticmethod
    def delete_inventory(id_to_remove, table):
        """Function to Delete a CD from the inventory

        Args:
            intIDDel (string): Used to identify the ID to delete

        Returns:
            blnCDRemoved (bool): Returns flag if cd was removed
        """
        intRowNr = -1
        blnCDRemoved = False
        # for row in lstTbl:
        for row in table:
            intRowNr += 1
            if row['ID'] == id_to_remove:
                # del lstTbl[intRowNr]
                del table[intRowNr]
                blnCDRemoved = True

        return blnCDRemoved

    @staticmethod
    def apend_inventory(strID, strTitle, strArtist, table):
        """Function to Apend a new entry to the inventory

        Args:
            strID (string): ID for the new CD added to the inventory
            strTitle (string):Title for the new CD added to the inventory
            strArtist (string):Artist for the new CD added to the inventory

        Returns:
            None.
        """
        intID = int(strID)
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
        table.append(dicRow)
        
class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            error_type (string): returns the class name of the error that was thrown 
        """
        table.clear()  # this clears existing data and allows to load data from file
        error_type = ''
        try:
            objFile = open(file_name, 'rb')
            while True:
                data = pickle.load(objFile)
                dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
                table.append(dicRow)
            objFile.close()
        except Exception as e:
            error_type = e.__class__.__name__
        return error_type

    @staticmethod
    # def write_file(file_name):
    def write_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to write the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
        Returns:
            error_type (string): returns the class name of the error that was thrown 
        """
        error_type = ''
        try:
            with open(file_name,'wb') as pickledFile:
                for row in table:
                    lstValues = list(row.values())
                    lstValues[0] = str(lstValues[0])
                    pickle.dump(lstValues, pickledFile)
        except Exception as e:
            error_type = e.__class__.__name__
        return error_type
# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user
        
        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Function to get user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
    
        
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Function to Display current inventory table
        
        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        if not table:
            print('The Inventory is currently empty \n')
        else:
            for row in table:
                print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================\n')
        
    @staticmethod
    def showload_inventory():
        """Display the messages when loading the inventory from a file.
        
        Args:
            None.

        Returns:
            strYesNo (string): User input to check if users want to continue loading file.

        """

        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled ')
        return strYesNo

    @staticmethod    
    def showadd_inventory(): 
        """Displays the User Input Questions for adding a new CD to the inventory

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            strID (int): CD Id to add to the inventory
            strTitle(string):Title to add to the inventory
            strArtist(string): Artist to add to the inventory
            error_type (string): returns the class name of the error that was thrown
            error_flag (bool): returns false if user enters not int to strID
        """
        error_type =''
        strID = -1
        strTitle =''
        strArtist =''
        error_flag = False
        while not error_flag:
            try:
                strID = int(input('Enter ID: '))
                strTitle = input('What is the CD\'s title? ').strip()
                strArtist = input('What is the Artist\'s name? ').strip()
                error_type =''
                error_flag = True
                break
            except Exception as e:
                error_type = e.__class__.__name__
                error_flag = False
                break
        return strID, strTitle, strArtist,error_type,error_flag
        
    @staticmethod        
    def showdelete_entry(blnCDRemoved,intIDDel):
        """Displays information if the CD item is deleted or not 


        Args:
            blnCDRemoved (Bool): Boolean result from checking if the CD Id is in the inventory
            intIDDel (Int): CD Id that was deleted

        Returns:
            None.

        """
        if blnCDRemoved:
            print(f'CD Id {intIDDel} was removed\n')
        else:
            print(f'Could not find CD Id {intIDDel} in the Inventory!\n')
        return

    @staticmethod         
    def error_status(error_type):
        if error_type == 'FileNotFoundError':
            print('The File {} does not exists!'.format(strFileName))
            print('\n') 
        elif error_type == 'ValueError':
            print('The Value entered is not an integer base 10')
                
# 1. When program starts, read in the currently saved Inventory
file = pathlib.Path(strFileName)
strErrorType = FileProcessor.read_file(strFileName, lstTbl) 
IO.error_status(strErrorType)

# 2. start main loop
while True:
# 2.1 Display Menu to user and get choice
    IO.print_menu()   
    strChoice = IO.menu_choice()        
        # 3. Process menu selection
        # 3.1 process exit first

    if strChoice == 'x':
        break
    
    # 3.2 process load inventory
    if strChoice == 'l':
    
        strYesNo = IO.showload_inventory()
            
        if strYesNo.lower().strip() == 'yes':
            print('reloading...\n')
            strErrorType = FileProcessor.read_file(strFileName, lstTbl)
            
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
        IO.error_status(strErrorType)    
        IO.show_inventory(lstTbl)          
        continue # start loop back at top.
    
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        while True:
            str_id, str_title, str_artist,strErrorType,blnErrorflag = IO.showadd_inventory()
            if str_id == -1:
                IO.error_status(strErrorType)
            else:
                DataProcessor.apend_inventory(str_id, str_title, str_artist, lstTbl)
                IO.show_inventory(lstTbl)
                break
            # 3.3.2 Add item to the table
        continue  # start loop back at top.
    
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
        
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        while True:
            try:
                intIDDel = int(input('Which ID would you like to delete? '))
                break
            except Exception as e:
                strErrorType = e.__class__.__name__
                IO.error_status(strErrorType)
        # 3.5.2 search thru table and delete CD
        was_cd_removed = DataProcessor.delete_inventory(intIDDel, lstTbl)
        IO.showdelete_entry(was_cd_removed, intIDDel)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
        
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
            print(f"The inventory has been saved to file {strFileName}")
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    else:
        print('Invalid option was selected')

    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
 





