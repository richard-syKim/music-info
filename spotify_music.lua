obs = obslua

function script_load(settings)
    os.execute('C:\\Path\\To\\YourScript.bat')  -- Run script on OBS start
end

function script_unload()
    os.execute('C:\\Path\\To\\YourStopScript.bat')  -- Run script on OBS close
end