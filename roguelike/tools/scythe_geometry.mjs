/**
 * Connected crimson crescent weapons, in the existing model coordinate system.
 * Grip: [8,8,8]. Shaft: +Y. Hook: -X. The cutting edge is the lower/inner
 * outline (-Y along the broad blade, +X along its downward curling tip).
 *
 * Each stepped spine section overlaps the next in X and Y. Its red lip also
 * overlaps the spine; a vertical red riser joins every change in edge height.
 * Small depth offsets keep overlapping visible faces from being coplanar.
 * No independently rotated pieces or detached flame decorations are used.
 */
export function buildScytheGeometry(solid) {
  const shaft = () => [
    solid([7.55, -9, 7.55], [8.45, 26, 8.45], 'black'),
    solid([7.30, 5.5, 7.30], [8.70, 10.5, 8.70], 'gray'),
    solid([7.15, -9, 7.15], [8.85, -7.5, 8.85], 'red'),
    solid([7.25, 22, 7.25], [8.75, 24, 8.75], 'red'),
  ];

  // Profiles run from the hooked point towards the haft. Entries contain
  // [left, right, lower cutting outline, upper black spine].
  const physicalProfile = [
    [-5.30, -4.15, 18.70, 23.20],
    [-4.30, -2.65, 21.80, 25.10],
    [-2.80, -0.60, 23.70, 26.40],
    [-0.75,  2.00, 25.00, 27.40],
    [ 1.85,  8.65, 26.00, 28.00],
  ];
  const infusedProfile = [
    [-10.00, -8.60, 15.20, 20.20],
    [ -8.75, -7.20, 18.80, 22.90],
    [ -7.35, -5.20, 21.60, 25.10],
    [ -5.35, -2.60, 23.60, 26.70],
    [ -2.75,  0.40, 25.00, 27.60],
    [  0.25,  8.85, 26.00, 28.30],
  ];

  function crescent(profile, infused) {
    const elements = [];
    const lip = infused ? 0.70 : 0.56;
    profile.forEach(([left, right, lower, upper], index) => {
      // Neighbouring sections differ in thickness by 0.03 model units.
      // Their 0.15 X overlap hides the joints even from oblique views.
      const inset = index * 0.015;
      const front = 7.40 + inset;
      const back = 8.60 - inset;
      elements.push(solid(
        [left, lower + 0.18, front],
        [right, upper, back],
        'black',
      ));
      elements.push(solid(
        [left, lower - 0.16, front + 0.07],
        [right + 0.12, lower + lip, back - 0.07],
        'red',
      ));
      const next = profile[index + 1];
      if (next) {
        // The inner vertical face is part of the cutting edge too. Extend it
        // into both horizontal lips, rather than placing a separate diagonal.
        elements.push(solid(
          [right - 0.37, lower - 0.11, front + 0.045],
          [right + 0.12, next[2] + lip, back - 0.045],
          'red',
        ));
      }
    });

    // One continuous pointed ember inset. It sits inside the first red lip,
    // with a slight front/back protrusion, so it cannot appear detached.
    if (infused) {
      const [left, right, lower] = profile[0];
      elements.push(solid(
        [left + 0.10, lower - 0.10, 7.44],
        [right - 0.05, lower + 0.36, 8.56],
        'orange',
      ));
    }
    return elements;
  }

  function crown(infused) {
    return [
      // Haft-to-blade socket overlaps both the pole and the crescent spine.
      solid([6.55, 23.40, 7.10], [9.45, 27.20, 8.90], 'black'),
      solid([7.20, 26.70, 7.48], [8.80, 30.25, 8.52], 'black'),
      solid([7.60, 29.80, 7.57], [8.40, 31.80, 8.43], 'red'),
      // The rear spur has an overlapping elbow instead of a rotated loose bar.
      solid([8.70, 25.15, 7.47], [infused ? 11.35 : 10.20, 27.70, 8.53], 'black'),
      solid([infused ? 10.45 : 9.40, 27.30, 7.56], [infused ? 11.35 : 10.20, infused ? 29.40 : 28.80, 8.44], 'red'),
    ];
  }

  return {
    spear: [...shaft(), ...crescent(physicalProfile, false), ...crown(false)],
    scythe: [...shaft(), ...crescent(infusedProfile, true), ...crown(true)],
  };
}
