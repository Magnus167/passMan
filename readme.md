# passMan.py

- password manager that generates random passwords
- each password is stored as a dictionary entry. the keys are indices and the values are dictionaries with website, username, length. 
- password is calculated by creating a string composed of the website, username, index, and seed. 
- this is then hashed with sha256, and the result is mapped to a set of characters. 

# Further Scope:
- add a GUI to enable paste website name
- enable file to be stored on gcp or amazon ec2
