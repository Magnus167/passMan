# passMan.py

- password manager that generates psuedo-random passwords using a random seed
- each password is stored as a dictionary entry. the keys are indices and the values are dictionaries with website, username, length.
- password is calculated by creating a string composed of the website, username, index, and seed.
- this is then hashed with sha256, and the result is mapped to a set of characters.

# Implementation

- gui.py uses PySimpleGUI to create a gui, and loads the password manager passMan from passMan.py.
- the user can search with by website and/or username. 
- click to copy password
- can add/delete logins as well


# Further Scope

- enable file to be stored on gcp or amazon ec2
