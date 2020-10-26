Spelling Wizard is a predictive system and spell checker written for python3 that can interact with the user or just correct a text file.  
There are two modes which can be accessed with commands read or write.  The exit command will either exit the mode you are in or terminate 
the program if you are not currenty in a mode.  The help command will print information of the functions.  
Read command:
read <input file> <output file>: 
The input file must be given.  If the output file is not given, the results will be printed to the terminal.
If the program is unsure about a specific word it will promt the user with the probable corrections to choose from

Write command:
write <output file>:
If no output file is specified, the results will be printed to a file called "spelling_wizard.txt". Every line entered into the program will be spellchecked and corrected.  
once corrected, the results will be printed to the screen. If the program is unsure about a specific error it will promt the user with probable corrections with numbers.  
If this was a mistake and the target word is an option press c otherwise enter the number of the intended word.  If you enter a line with ending it with punctuation, the program 
will correct the line and prompt you to choose from 15 probable next words. If there are no options you like press c to cancel and continue writing the sentence.  
Entering exit exit the writing mode but not the program.
