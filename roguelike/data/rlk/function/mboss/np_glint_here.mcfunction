# np_glint at the execution position (mboss_lib.np_warn(at=...)): for a tell during which the visible body is not at the
# body anchor's glint point - the module gives the rig point (a clip's chest / head anchor, a spot above the floor where
# she will come out). Same gate. The caller keeps it above the floor.
function rlk:mboss/np_gate
execute if score #npOk mb matches 1 run function rlk:player/def/fx/glint
