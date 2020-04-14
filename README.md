# git-rebuild
Git-rebuild is a pentest tool which can be used to reconstruct misconfigured and exposed .git repositories 

## Scenario
A poorly misconfigured .git repo might exist on a server which can be accessible by http://site.com/.git/ . An attacker can download the entire repo and can reproduce the files from these exposed git repo. In a scenario where directory listing is not enabled, the 403 forbidden error will pop up. These tool automate the extraction of those repos in case directory listing is disabled. It reconstructs from the objects of git repo by automatically downloading them and reconsturcting them properly. 

THIS DOES NOT WORK FOR THE PACKED OBJECTS AT THE MOMENT

### How to use the tool
```
-  ~$ mkdir demo => create a directory
-  ~$ cd demo => move to the directory
-  ~demo $ git init => initialize the directory as a git repo
-  ~demo $ cp tool.py .git => copy tool.py inside the .git repo 
-  ~demo $ cd .git => move to the .git repo
-  ~demo/.git $ python3 tool.py http://vulnerable.com => Run the command
-  ~demo/.git $ cd .. => move to the parent directory after the code execution finishes
-  ~demo $ ls => find the recoverd files 
```
