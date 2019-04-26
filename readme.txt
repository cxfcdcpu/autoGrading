Required packets:

sudo apt install Python2
Tkinter(I think it's embedded)
pip install pillow
pip install canvasapi


Required information:
follow the prompt to provid the canvas token(need to apply at the website) when running the Mask.sh.

type in classID (you can find at the canvas website) to the file: _canvasInfo.txt
The CPP password will be asked by the program prompt when sign in. 

How to run:
./Mask.sh  course section  class#   downloadToDir(default:~/Desktop)
example:     ./Mask.sh 1580 f 3 YourSpecifiedDir

How to use:
1. Draw the comments using mouse
2. Right click to add comments.
3. Click clear button to clear all comments.
4. Upload by click the upload button.
5. choose or search students.
6. If you find any bugs click help and the link to report the Bug. Thanks


Known bugs:
1. The TAB button the student use will cause the unmatch of the printout format.
The visualized printout (which we see) use 4 spaces for TAB symbol while the
saved comments file use single space rectangle to represent it. The reason 
causes this bug is the font I download not support to represent TAB symbol.
