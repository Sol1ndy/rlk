# Stand-in A13 judge (T + 258): shield/judge; the darkness lifts and the banner goes; a fail runs its branch.
function rlk:boss/scarlet/shield/judge
execute if score #gres hr matches 2 as @a[tag=player,limit=1] run function rlk:boss/scarlet/ult/fatal
