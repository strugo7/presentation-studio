-- pptx_to_keynote.applescript <abs .pptx in> <abs .key out>
-- Opens a .pptx in Keynote and exports a .key. macOS + Keynote only; first run prompts for Automation.
on run argv
	if (count of argv) < 2 then error "usage: osascript pptx_to_keynote.applescript IN.pptx OUT.key"
	set inPath to item 1 of argv
	set outPath to item 2 of argv
	set inFile to POSIX file inPath
	set outFile to POSIX file outPath
	tell application "Keynote"
		activate
		set theDoc to open inFile
		delay 1
		export theDoc to outFile as Keynote
		close theDoc saving no
	end tell
	return "saved " & outPath
end run
