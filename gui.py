
import PySimpleGUI as sg
import passMan

# First the window layout in 2 columns

file_list_column = [
    [
        sg.Text("passMan.py"),
        sg.In(size=(25, 1), enable_events=True, key="-WebsiteName-"),
        sg.Button("PasteWebsite", key="-PasteWebsite-"),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-PassList-"
        )
    ],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        # sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Image Viewer", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-PasteWebsite-":
        window.find_element("-WebsiteName-").Update(passMan.pasteTextFromClipboard())


    if event == "-WebsiteName-":
        passFile = passMan.get_passFile()
        passList = passMan.get_login_list(passFile, values["-WebsiteName-"])
        passListStr = [i[0] + " - " + i[1] for i in passList]
        window.find_element("-PassList-").Update(passListStr)
        if len(passList) == 0:
            window.find_element("-PassList-").Update(["No Passwords Found"])
        if len(passList) == 1:
            passMan.pasteTextToClipboard(text=passMan.get_password(passList[0][2], passFile))
            window.find_element("-PassList-").Update(["Password Copied to Clipboard"])
            # showmessage("Copied Password to Clipboard")
        window.find_element("-PassList-").Update(passList)

        

window.close()
