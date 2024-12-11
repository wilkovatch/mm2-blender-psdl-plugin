Blender add-on for exporting PSDL files for Midtown Madness 2

This plugin uses code from this repository: https://github.com/wilkovatch/psdl-exporter-common

Requirements:
  This add-on has been tested with Blender 2.91 and Blender 3.1, it may not work with older versions

Installation:
  - Clone this repository (including the submodules) with: git clone https://github.com/wilkovatch/mm2-blender-psdl-plugin.git --recurse-submodules
  - zip the "io_scene_psdl" directory in a file named "io_scene_psdl.zip"
  - Open Blender, go to the preferences menu (Edit->Preferences) and go to the "Add-ons" tab
  - Click the "Install..." button (in the top right corner, to left of the "Refresh" button)
  - Select the addon .zip file you created earlier (io_scene_psdl.zip)
  - Enable it

Usage:
  - Create your city
  - Export the city (File->Export->Angel Studios PSDL)
  - You can also export INST, PATHSET and BAI (still buggy) files by checking their checkboxes

Notes:
  - The BAI exporter is still incomplete and broken
