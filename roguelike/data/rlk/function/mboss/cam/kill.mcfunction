# FN-cam: the cameras and their texts gone (a module's sequence end / cancel / cleanup), the stored line and hint blank
# (new cameras start without a text). A player still spectating one falls back to their own view by the game itself;
# rlk:tick's release (the request has stopped) puts them back.
kill @e[tag=rlk_mb_camx]
data modify storage rlk:mboss camtx set value {line:{text:"",background:0},hint:{text:"",background:0}}
