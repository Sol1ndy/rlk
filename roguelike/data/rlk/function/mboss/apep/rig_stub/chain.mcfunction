# STUB rig (tools/mboss_apep/stub_rig_rt.py; ap_contract 0.4.9): the real rig (wip/ap-rig) replaces it per function.
# The stub clips' clocks (ids >= 1000): this tick's events, then loop / next / hold. Also called after a
# real rig tick while clips fall back (api.rig_tick_lines).
execute unless score @s apRigC matches 1000.. run return 0
execute if score @s apRigC matches 1000..1017 run return run function rlk:mboss/apep/rig_stub/cl/d1000_1017
execute if score @s apRigC matches 1018..1035 run return run function rlk:mboss/apep/rig_stub/cl/d1018_1035
