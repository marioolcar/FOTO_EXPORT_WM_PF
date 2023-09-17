-- Import the Lightroom SDK modules
local LrDialogs = import 'LrDialogs'
local LrView = import 'LrView'



-- Create a function to show the GUI window
function showHelloWorldDialog()
    -- Define the contents of the window
    local f = LrView.osFactory()
    local dialogContents = f:column {
        spacing = f:control_spacing(),
        f:static_text {
            title = "Dolje uprava!",
            alignment = "center",
            fill_horizontal = 1,
        },
    }

    -- Show the dialog window
    LrDialogs.presentModalDialog {
        title = "Dolje uprava!",
        contents = dialogContents,
    }
end






-- Call the function to show the GUI window
showHelloWorldDialog()