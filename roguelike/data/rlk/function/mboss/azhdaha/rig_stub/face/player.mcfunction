# STUB rig (tools/mboss_azhdaha/stub_rig.py, manifest.md 8): the real rig (wip/az-rig) replaces it per function.
# Instant yaw toward the player's body.
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
