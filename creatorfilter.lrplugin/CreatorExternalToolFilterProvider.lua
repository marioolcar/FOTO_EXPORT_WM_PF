--[[----------------------------------------------------------------------------

CreatorExternalToolFilterProvider.lua
Export service provider description for Creator external tool sample

--------------------------------------------------------------------------------

ADOBE SYSTEMS INCORPORATED
 Copyright 2008 Adobe Systems Incorporated
 All Rights Reserved.

NOTICE: Adobe permits you to use, modify, and distribute this file in accordance
with the terms of the Adobe license agreement accompanying it. If you have received
this file from a source other than Adobe, then your use, modification, or distribution
of it requires the prior written permission of Adobe.

------------------------------------------------------------------------------]]

-- Lightroom SDK
local LrView = import 'LrView'
local bind = LrView.bind
local LrPathUtils = import 'LrPathUtils'
local LrTasks = import "LrTasks"
local LrExportSession = import 'LrExportSession'


--============================================================================--

local CreatorExternalToolFilterProvider = {}

-------------------------------------------------------------------------------
--[[
CreatorExternalToolFilterProvider.exportPresetFields = {
	{ key = 'creatorName',	 default = 'Lightroom' },
	{ key = 'metachoice', 	 default = 'Title' },
	{ key = 'metavalue', 	 default = '' },
}
]]--
-------------------------------------------------------------------------------




------------------------MOJ DIO KODA----------------------------------------
--[[

-- Define the overlay image file path
local overlayImagePath = "watermark.png"

-- Function to apply overlay
function applyOverlay(photo, exportContext)
    -- Check if the photo and overlay image exist
    if not LrFileUtils.exists(overlayImagePath) then
        LrErrors.throwUserError("Overlay image not found")
        return
    end

    -- Load the overlay image
    local overlayPhoto = photo:addPhoto(overlayImagePath)

    -- Set the position and size of the overlay image
    overlayPhoto:setRawMetadata("customRendered", 1) -- To prevent Lightroom from applying further adjustments
    overlayPhoto:setRawMetadata("angle", 0) -- Set rotation angle
    overlayPhoto:setRawMetadata("renderedHeight", 100) -- Set height (adjust as needed)
    overlayPhoto:setRawMetadata("renderedWidth", 100) -- Set width (adjust as needed)
    overlayPhoto:setRawMetadata("renderedXOffset", 0) -- Set X offset (adjust as needed)
    overlayPhoto:setRawMetadata("renderedYOffset", 0) -- Set Y offset (adjust as needed)

    -- Set the blending mode of the overlay (e.g., "Screen" for a watermark effect)
    overlayPhoto:setDevelopSetting("Blacks", -100) -- Example setting, adjust as needed

    -- Add the overlay image to the photo
    photo:addToStackAbove(overlayPhoto)

    -- Export the photo with the overlay
    exportContext:doExportOnCurrentTask()
end

-- Register the function to run when exporting
LrExportSession.addPostProcessor({
    name = "Apply Overlay and Watermark",
    postProcessRenderedPhotos = applyOverlay,
})






]]--


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
            title = "Hello, World!",
            alignment = "center",
            fill_horizontal = 1,
        },
    }

    -- Show the dialog window
    LrDialogs.presentModalDialog {
        title = "Hello, World!",
        contents = dialogContents,
    }
end

-- Call the function to show the GUI window









---------------------------------------------------------




function CreatorExternalToolFilterProvider.sectionForFilterInDialog( viewFactory, propertyTable )

	return {
		showHelloWorldDialog()
		title = 'Creator External Tool Sample',
		
		viewFactory:row {
			spacing = viewFactory:control_spacing(),
			viewFactory:static_text {
				title = "Export Images that match the following",
			},
		},
		viewFactory:row {
			spacing = viewFactory:control_spacing(),
			viewFactory:popup_menu {
				value = bind 'metachoice',
				items = {
					{ title = "Title",			value = "title" },
					{ title = "Creator",			value = "creator" },
					{ title = "Copyright Status",	value = "copyright" },
					{ title = "File Name",			value = "fileName" },
					{ title = "Folder",			value = "folderName" },
				},
			},

			viewFactory:edit_field {
				value = bind 'metavalue',
			},
		},
		viewFactory:row {
			spacing = viewFactory:control_spacing(),
			viewFactory:static_text {
				title = "Set the Creator Name metadata field to match the following",
			},
		},
		viewFactory:row {
			spacing = viewFactory:control_spacing(),
			viewFactory:static_text {
				title = "Creator Name",
			},
			viewFactory:edit_field {
				value = bind 'creatorName',
			},
		}
	}
end

-------------------------------------------------------------------------------

function CreatorExternalToolFilterProvider.postProcessRenderedPhotos( functionContext, filterContext )

	
	local renditionOptions = {
		plugin = _PLUGIN,
		renditionsToSatisfy = filterContext.renditionsToSatisfy,
		filterSettings = function( renditionToSatisfy, exportSettings )
			
		
			-- This hook function gives you the opportunity to change the render
			-- settings for each photo before Lightroom renders it.
			-- For example, if you wanted Lightroom to generate TIFF files.
			-- You can add below statements:
			-- exportSettings.LR_format = TIFF
			--  return os.tmpname()
			-- By doing so, you assume responsibility for creating
			-- the file type that was originally requested and placing it
			-- in the location that was originally requested in your filter loop below.
			
		end,
	}
	
	local command
	local quotedCommand
	local targetCreator = filterContext.propertyTable.creatorName
			
	for sourceRendition, renditionToSatisfy in filterContext:renditions( renditionOptions ) do
	
		-- Wait for the upstream task to finish its work on this photo.
		
		local success, _ = sourceRendition:waitForRender()
		
		if success then
			
			local path = sourceRendition.destinationPath
		
			-- Now that the photo is completed and available to this filter, you can do your work on the photo here.
			-- In this example, the renditions are passed to an external application that updates the Creator metadata
			-- with the entry added in the export dialog section.
			
			if WIN_ENV == true then
           			command = '"' .. LrPathUtils.child( LrPathUtils.child( _PLUGIN.path, "win" ), "LightroomCreatorXMP.exe" ) .. '" ' .. '"' .. path .. '" ' .. '"' .. targetCreator .. '"'
					quotedCommand = '"' .. command .. '"'
			else
					command = '"' .. LrPathUtils.child( LrPathUtils.child( _PLUGIN.path, "mac" ), "LightroomCreatorXMP" ) .. '" ' .. '"' .. path .. '" ' .. '"' .. targetCreator .. '"'
					quotedCommand = command
			end
			
			if LrTasks.execute( quotedCommand ) ~= 0 then
				renditionToSatisfy:renditionIsDone( false, "Failed to contact XMP Application" )
			end
		
		end
	
	end

end

-------------------------------------------------------------------------------

function CreatorExternalToolFilterProvider.shouldRenderPhoto( exportSettings, photo )

	-- This function should return either:
	--   true, photo gets included in export, or
	--   false, photo should be removed from the export.
	-- The photo represents an LrPhoto object.
	
	local targetField = exportSettings.metachoice
	local targetValue = exportSettings.metavalue

	-- Now that the user has filled in this section we need to filter through the images and only
	-- choose the ones that match the required metadata.

	local sourceMetaValue = photo:getFormattedMetadata( targetField )
	
	local shouldRender = sourceMetaValue == targetValue

	return shouldRender

end

--------------------------------------------------------------------------------

return CreatorExternalToolFilterProvider

-----