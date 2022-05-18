
import PySimpleGUI as sg
import passMan

# First the window layout in 2 columns

def create_passListStrs(passList):
    return ['i:{} | {} | {}'.format(i[2], i[0], i[1]) for i in passList]
file_list_column = [
    [
        sg.Text("passMan.py"),
        # sg.In(size=(25, 1), enable_events=True, key="-WebsiteName-"),
        # sg.Button("PasteWebsite", key="-PasteWebsite-"),
    ],     
    [
        # sg.Text("passMan.py"),
        sg.In(size=(25, 1), enable_events=True, key="-WebsiteName-"),
        sg.Button("Paste Website", key="-PasteWebsite-"),
    ],    
    [
        sg.In(size=(25, 1), enable_events=True, key="-UserName-"),
        sg.Button("Paste UserName", key="-PasteUserName-"),
        sg.Button("Search", key="-Search-"),
        
    ],
    [   
        sg.Listbox(
            values=create_passListStrs(passMan.get_login_list(passMan.get_passFile())), enable_events=True, size=(40, 10), key="-PassList-"
        )

    ],
]

second_column = [


    [
        # sg.Text("passMan.py"),
        sg.Text("", key='-Message-')
    ],     [
        # sg.Text("passMan.py"),
        sg.In(size=(25, 1), enable_events=True, key="-WebsiteNameNew-"),
        sg.Button("Paste Website", key="-PasteWebsiteNew-"),
    ],    
    [
        sg.In(size=(25, 1), enable_events=True, key="-UserNameNew-"),
        sg.Button("Paste Username", key="-PasteUserNameNew-"),
    ],    
    [
        sg.Button("Add New Login", key="-AddNewLogin-"),
        sg.Checkbox('Special Characters', default=False, key="-SpecialChars-"),
    ],    
    [
        sg.Button("Delete Login", key="-DelLogin-")
    ],
]


# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(second_column),
    ]
]

window = sg.Window("passMan.py", layout)

def update_message(message):
    window.find_element("-Message-").Update(message)


def update_listbox( username='', website=''):
        passFile = passMan.get_passFile()
        passList = passMan.get_login_list(passFile, website)
        # passList = passMan.get_login_list(passFile, values["-WebsiteName-"])
        passList = [x for x in passList if username.strip() in x[1]]
        window.find_element("-PassList-").Update(create_passListStrs(passList))
        if len(passList) == 0:
            window.find_element("-PassList-").Update(["No Passwords Found"])
            
            update_message("No Passwords Found")
        if len(passList) == 1:
            passMan.pasteTextToClipboard(text=passMan.get_password(passList[0][2], passFile))
            
            update_message("Password Copied to Clipboard")
        window.find_element("-PassList-").Update(create_passListStrs(passList))
        

while True:
    event, values = window.read()

    # on create window
    

    if event == '-Search-':
        update_listbox(values['-UserName-'], values['-WebsiteName-'])

    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-PasteWebsite-":
        window.find_element("-WebsiteName-").Update(passMan.pasteTextFromClipboard())

    if event == "-PassList-":
        currSel = window.find_element("-PassList-").get()
        if currSel != []:
            index = str(currSel[0]).split('|')[0][2:].strip()
            passMan.pasteTextToClipboard(text=passMan.get_password(index=index, passFile=passMan.get_passFile()))
            # sg.Popup("Password Copied to Clipboard")
            update_message("Password Copied to Clipboard")
            update_listbox()        
        

    if event == "-WebsiteName-" or event == "-UserName-":
        update_listbox(username=values["-UserName-"], website=values["-WebsiteName-"])
    
    if event == "-AddNewLogin-":
        passFile = passMan.get_passFile()
        passMan.add_to_passFile([passMan.create_pwd_dict(username=values["-UserNameNew-"], website=values["-WebsiteNameNew-"], special_chars=values["-SpecialChars-"])])
        update_listbox(username=values["-UserNameNew-"], website=values["-WebsiteNameNew-"])
        
        update_message("Password Added and copied to clipboard")
    
    if event == "-DelLogin-":
        if currSel != []:
            index = str(currSel[0]).split('|')[0][2:].strip()
            updated_passFile = passMan.delete_password(index, passMan.get_passFile())
            passMan.save_passFile(passFile=updated_passFile)
            update_message(message="Password Deleted")


        

window.close()
