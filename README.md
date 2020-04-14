# git-rebuild
Git-rebuild is a pentest tool which can be used to download and extract misconfigured .git repositories

How to use the tool

-  ~$ mkdir demo => create a directory
-  ~$ cd demo => move to the directory
-  ~demo $ git init => initialize the directory as a git repo
-  ~demo $ cp tool.py .git => copy tool.py inside the .git repo 
-  ~demo $ cd .git => move to the .git repo
-  ~demo/.git $ python3 tool.py http://vulnerable.com => Run the command
-  ~demo/.git $ cd .. => move to the parent directory after the code execution finishes
-  ~demo $ ls => find the recoverd files 
-  
