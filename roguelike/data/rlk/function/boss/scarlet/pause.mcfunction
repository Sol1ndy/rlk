# Hook pause (the fight froze: dead, reviving, a menu, no player; @s = body): the kit cards go; a pattern's own pause;
# a running gauntlet is cancelled (hazards, ghost, the banner off) and restarts at resume through lead_re {g} from T0
# with the gauge 5/5 (hr_design §1.5); a judged result is kept: after its fatal the revive stance, after the judged
# deflect the repel, after the judged G1 fail P2 at once (#grs 4), a lethal gauntlet paused past its last cut with
# segments left: its fail at the resume (#grs 5). A locked cutscene never resumes in the middle (§3.6; the lock is
# released by the framework, no module tick requests it): CS0 / CS1 / the repel go to their end state at resume,
# a lead-in restarts from 0 (#grs 6-9, core/seq/pause).
function rlk:boss/scarlet/fx/clear
execute if score #pat hr matches 21.. run function rlk:boss/scarlet/core/g/pause
execute if score #sqn hr matches 1.. if score #grs hr matches 0 run function rlk:boss/scarlet/core/seq/pause
