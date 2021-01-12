Spelling Wizard is a predictive system and spell checker written in python that can interact with the user or correct a text file.  
There are two modes which can be accessed with the read and write commands. The exit command will either exit the mode you are in or terminate the program if you are not currently in a mode. The help command will print the information of the functions.  
Read command:
read <input file> <output file>: 
The input file must be given. If the output file is not given, the results will be printed to the terminal.
If the program is unsure about a specific word, it will prompt the user with the probable corrections to choose from.

Write command:
write <output file>:
If no output file is specified, the results will be printed to a file called "spelling_wizard.txt". Every line entered will be spellchecked and corrected.  
Once corrected, the results will be printed to the screen. If the program is unsure about a specific error, it will prompt the user with probable corrections. 
To select a correction, enter the number correlated with the intended word. 
If the intended word is not an available option or the there was no mistake, press c.
If you enter a sentence that has not been finished (not ending in punctuation), the program 
will correct the line and prompt you to choose from 15 probable next words. If you do not want to use any of the available options, you can press c to cancel and continue writing the sentence.  

All data utilized by spelling wizard is collected from Project Gutenberg: https://www.gutenberg.org/
