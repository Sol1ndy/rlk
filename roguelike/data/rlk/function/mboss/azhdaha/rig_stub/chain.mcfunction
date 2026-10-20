# STUB rig (tools/mboss_azhdaha/stub_rig.py, manifest.md 8): the real rig (wip/az-rig) replaces it per function.
# Loop / next / hold of the stub clips (ids >= 1000); also called after a real rig tick (api.rig_tick).
execute unless score @s azRigC matches 1000.. run return 0
