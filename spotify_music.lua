obs = obslua

function script_load(settings)
    os.execute('start "music.py" cmd /c py "D:/Code Projects/Stream/music-info/music.py"')  -- Run script on OBS start
end

function script_unload()
    os.execute('start cmd /c stop') -- doesn't work
end