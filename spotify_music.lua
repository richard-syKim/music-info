obs = obslua

function script_load(settings)
    os.execute('start "OBS with Music" cmd /k py "D:/Code Projects/Stream/music-info/music.py"')  -- Run script on OBS start
end

function script_unload()
    os.execute('echo stop') -- doesn't work
end