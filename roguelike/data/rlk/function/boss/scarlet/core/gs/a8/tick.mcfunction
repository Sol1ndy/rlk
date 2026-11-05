# Stand-in A8 tick (#pt hr 1..).
execute if score #pt hr matches 0 run function rlk:boss/scarlet/rig_stub/play/g_tell
execute if score #pt hr matches 14 run function rlk:boss/scarlet/rig_stub/play/g_dash
execute if score #pt hr matches 20 run function rlk:boss/scarlet/core/gs/cut {s:27}
execute if score #pt hr matches 24 run function rlk:boss/scarlet/rig_stub/play/g_ring
execute if score #pt hr matches 31 run function rlk:boss/scarlet/rig_stub/play/g_rise
execute if score #pt hr matches 33 run function rlk:boss/scarlet/core/gs/cut {s:40}
execute if score #pt hr matches 46 run function rlk:boss/scarlet/rig_stub/play/g_leap
execute if score #pt hr matches 48 run function rlk:boss/scarlet/core/gs/cut {s:55}
execute if score #pt hr matches 70 run function rlk:boss/scarlet/rig_stub/play/g_glide
execute if score #pt hr matches 75 run function rlk:boss/scarlet/core/gs/cut {s:82}
execute if score #pt hr matches 79 run function rlk:boss/scarlet/rig_stub/play/g_sweep
execute if score #pt hr matches 87 run function rlk:boss/scarlet/core/gs/cut {s:94}
execute if score #pt hr matches 88 run function rlk:boss/scarlet/rig_stub/play/g_x
execute if score #pt hr matches 108 run function rlk:boss/scarlet/rig_stub/play/g_dash
execute if score #pt hr matches 114 run function rlk:boss/scarlet/core/gs/cut {s:121}
execute if score #pt hr matches 118 run function rlk:boss/scarlet/rig_stub/play/g_ring
execute if score #pt hr matches 130 run function rlk:boss/scarlet/rig_stub/play/g_drop
execute if score #pt hr matches 140 run function rlk:boss/scarlet/core/gs/cut {s:147}
execute if score #pt hr matches 144 run function rlk:boss/scarlet/rig_stub/play/g_wrap
execute if score #pt hr matches 152 run function rlk:boss/scarlet/core/gs/cut {s:159}
execute if score #pt hr matches 156 run function rlk:boss/scarlet/rig_stub/play/g_dome
execute if score #pt hr matches 167 run function rlk:boss/scarlet/core/gs/cut {s:174}
execute if score #pt hr matches 169 run function rlk:boss/scarlet/rig_stub/play/g_vert
execute if score #pt hr matches 188 run function rlk:boss/scarlet/rig_stub/play/g_dive
execute if score #pt hr matches 194 run function rlk:boss/scarlet/core/gs/a8/judge
execute if score #pt hr matches 206 if score #gres hr matches 1 run scoreboard players set #done hr 1
execute if score #pt hr matches 214 if score #gres hr matches 2 run scoreboard players set #done hr 1
