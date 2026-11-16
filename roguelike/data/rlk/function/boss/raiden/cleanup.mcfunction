function rlk:boss/raiden/camera/release_all
function rlk:boss/raiden/caption/clear
function rlk:boss/raiden/illusion/cleanup
kill @e[tag=rlk_raiden_aux]
kill @e[tag=rlk_rd_tmp]
function rlk:boss/raiden/bars_hide
# A fight stopped mid-Tenma (test/stop, run end, uninstall) gives the arena its Shogun floor back.
execute if entity @e[tag=rlk_raiden_arena,limit=1] run function rlk:room/raiden/look_shogun
