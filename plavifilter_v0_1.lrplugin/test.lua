local LrDialogs = import 'LrDialogs'
local LrView = import 'LrView'



function showHelloWorldDialog()
    local f = LrView.osFactory()
    local dialogContents = f:column {
        spacing = f:control_spacing(),
        f:static_text {
            title = "Dolje uprava!",
            alignment = "center",
            fill_horizontal = 1,
        },
    }

    LrDialogs.presentModalDialog {
        title = "Dolje uprava!",
        contents = dialogContents,
    }
end


showHelloWorldDialog()