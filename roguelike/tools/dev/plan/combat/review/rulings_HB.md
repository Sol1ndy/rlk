# Review H-B (홍련, the cutscenes) — lead rulings (11-11). Findings: `findings_HB.json` (head d7da75e79). Fix lane: `wip/combat-hfb`.

The user's requests: 「컷신이나 대사 중에는 플레이어를 조작할 수 없고 홍련에 클로즈업이 되도록 해줘」 · 「플레이어도 같이 때리는 모습이 있어야」.

| id | ruling |
|---|---|
| HB-01 | Fix both sides of the repel's shoulder throw (78-96): the actor's hands hold her wrist / forearm through 78-96 and pull her over its shoulder in a low arc (her pelvis passes ≤ 0.6 b above the actor's shoulder at the top); she lands on her back beyond it as designed. Add **mutual** contact rows (both figures' points, not one side) to `test_contact` and both builders for every grab / hold / throw beat; fix the actor manifest's description to what the clip does. Render it from the shot camera and from the side and look. |
| HB-02 | Mitigate and document: while Shift is held during a lock, each tick also teleport the player to the live stand's eye position and rotation (so the free view cannot drift or sink); README states that holding Shift loosens the view until it is released. test_cam's K4 asserts the new behaviour. |
| HB-03 | Fix: stands are summoned at their first shot's eye point and rotation (Rotation in the summon NBT) at least 2 ticks before they go live, so no spawn glide / spin can be seen; make camsim model a new entity's spawn packet (appears where it was summoned, then glides) so the suite catches it. |
| HB-04 | Fix E2: cut before both figures leave the frame (or reframe so the shove stays in frame). |
| HB-05 | Fix: the hand-back happens only after the coda's black is fully opaque (or the black holds through the hand-back tick). |
| HB-06 | **The user's request wins**: every one of her lines plays on a shot close on her (her head and shoulders fill a good part of the frame; the actor may be in it). Keep the video's beats where no line plays. Line 8 over the empty field → a close-up of her. List the reframed shots. |
| HB-07 | Fix the reveal: I18 opens with her face hidden under the brim; her eyes are seen only when the brim lifts at 1330-1346 (keep the lens clear of the brim, ≥ 0.3 b, as HI fixed). |
