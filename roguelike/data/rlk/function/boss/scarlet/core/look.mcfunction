# The look request (PLAN §6.6): started at the first tick with no arena job (#mbArBuild 0), so a pause or a
# reload inside a running job can no longer leave the arena in the wrong look.
execute if score #hrLook hr matches 1.. unless score #mbArBuild mb matches 1.. run function rlk:boss/scarlet/core/look/go
