# Record Books v. 1.1
Author: Constantine Ryzhykov constantine.ryzhikov@gmail.com

Release Date: October 5, 2022


Record Books is an application for blind and visually impaired speakers that will allow them to perform voiceovers more efficiently.
The application is a text editor where you can open and save a file, record and listen to the recordings.


# Usage
CTRL+O - open a file

CTRL+S - save a file

CTRL+SHIFT+S - save a file as

Also, these features are available from the alt menu

CTRL+1 - start recording

CTRL+2 - stop recording

CTRL+3 - play last record

CTRL+4 - delete last record


Recordings are saved to the root of the program folder as 1.wav, 2.wav, 3.wav, 4.wav...
If you already have some recordings when you start the application, the recording will start from the last file. Thus, if you have 4 records at the time of application startup, pressing CTRL+3 will play the last 4.wav file, and pressing CTRL+1 will start recording the 5.wav file.
In the alt menu there is "Clear" item, with which you can delete all recordings.


# Remarks
You can't open every file. It must not be a Word, RTF or FB2 document. It is also optional, but desirable to use UTF8 encoding.


# Changes
Version 1.0 was developed using the C# programming language. Since version 1.1, the application has been developed in Python and the code is open source.


About any bugs, for any questions and suggestions, please contact the author by Email: constantine.ryzhikov@gmail.com
