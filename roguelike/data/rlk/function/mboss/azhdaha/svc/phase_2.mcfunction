# Phase 2 (absorb 1 at t94): the leg element on the ground hazards (#azE), floor F2, music "2". The brand banner
# (once per fight) is shown by absorb 1 at its roar, when gameplay resumes (REQ ps-3; plan 4.4).
scoreboard players set #azPh mb 2
scoreboard players operation #azE mb = #azLeg mb
scoreboard players set #azET mb 5
function rlk:mboss/azhdaha/svc/floor_f2
function rlk:mboss/azhdaha/svc/music_2
scoreboard players set #azHudQ mb 1
