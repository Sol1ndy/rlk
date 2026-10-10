/**
 * Original crystalline sword geometry inspired by the supplied Skirk reference.
 * Grip is [8,8,8], blade points along +Y, and the broad faces lie in the XY plane.
 * Both forms share their silhouette. White cutting edges surround broad cobalt,
 * violet and ice-blue facets, with a compact hooked asymmetric guard and a
 * white-wrapped midnight-blue grip. Colours are visible on both broad faces.
 *
 * Every blade/guard section overlaps its neighbour. The small diamond ornaments
 * grow out of visible narrow sockets rather than floating as accidental gaps.
 * Palette: black, blue, gray, light_gray, white, light_blue, purple and cyan.
 */
export function buildSkirkWeaponGeometry(solid) {
  function build(infused) {
    const elements = [];
    const colour = {
      core: 'blue',
      facet: infused ? 'light_blue' : 'purple',
      shade: 'purple',
      pale: infused ? 'white' : 'light_blue',
    };
    const box = (from, to, texture, faces = {}) => {
      const e = solid(from, to, texture);
      for (const [side, tex] of Object.entries(faces)) e.faces[side].texture = '#' + tex;
      elements.push(e);
      return e;
    };
    // Only the guard, its sockets and its ornaments are drawn in this narrower
    // space. The grip, blade length and blade tip retain their original size.
    const guardX = x => 8 + (x - 8) * .65;
    const guardBox = (from, to, texture, faces = {}) => box(
      [guardX(from[0]), from[1], from[2]],
      [guardX(to[0]), to[1], to[2]], texture, faces,
    );

    // Midnight grip, with contrasting front/rear facets and four white wraps.
    box([7.43, 3.0, 7.39], [8.57, 10.35, 8.61], 'blue', {east:'black', west:'purple'});
    for (const y of [3.8, 5.35, 6.9, 8.45]) {
      box([7.31, y, 7.30], [8.69, y + 1.18, 8.70], 'white', {east:'light_gray', west:'light_blue'});
      // A midnight seam makes the wraps read as a banded grip, not a white rod.
      box([7.28, y + .08, 7.26], [7.63, y + .44, 8.74], 'blue');
    }
    box([7.19, 2.65, 7.16], [8.81, 3.42, 8.84], 'white', {east:'light_blue', west:'gray'});
    box([7.18, 9.70, 7.12], [8.82, 10.80, 8.88], 'blue', {north:'purple', south:'light_blue'});

    // Pommel crystal: stepped, genuinely solid diamond, seated in its white cap.
    const pommel = [
      [1.20, 2.87, .85], [.15, 1.35, 1.12], [-.68, .31, .67], [-1.30, -.52, .25],
    ];
    for (const [lo, hi, half] of pommel) {
      box([8-half, lo, 7.48], [8+half, hi, 8.52], 'purple', {north:'light_blue', east:'blue', west:'white'});
    }

    // A continuous long silver blade. Progressively narrower overlapping steps
    // create a sharp point without independent rotated pieces or loose end caps.
    const blade = [
      [11.35, 13.10, 7.68, 2.20],
      [12.98, 14.62, 7.78, 2.12],
      [14.50, 16.14, 7.88, 2.02],
      [16.02, 17.66, 7.98, 1.92],
      [17.54, 19.18, 8.08, 1.81],
      [19.06, 20.70, 8.18, 1.68],
      [20.58, 22.22, 8.28, 1.53],
      [22.10, 23.74, 8.38, 1.36],
      [23.62, 25.26, 8.48, 1.18],
      [25.14, 26.78, 8.58, .98],
      [26.66, 28.30, 8.68, .78],
      [28.18, 29.60, 8.78, .56],
      [29.48, 30.63, 8.89, .34],
      [30.51, 31.65, 9.00, .13],
    ];
    blade.forEach(([lo, hi, centre, originalHalf], i) => {
      // Reduce the wide root by 22%, blending back to the existing fine point.
      const half = originalHalf * (.78 + .22 * i / (blade.length - 1));
      // The supplied side view is almost a silver line: a 0.65-unit base
      // tapers to 0.18 at the tip; only the centre ridge projects beyond it.
      const depth = .09 + (13-i)*.018;
      box([centre-half, lo, 8-depth], [centre+half, hi, 8+depth], 'white', {
        east:'light_blue', west:'light_gray', down:'light_gray',
      });
      if (i >= 13) return;
      const inset = Math.max(.08, half*.66);
      // The crystal ridge is thicker than its silver frame. Alternate tiny depth
      // offsets prevent coplanar flashing at the joints while retaining overlap.
      const ridge = depth + .055 + (i%2)*.008;
      const offset = (i%3-1)*Math.min(.23, half*.16);
      const left = centre-inset+offset;
      const right = centre+inset+offset;
      const seam = centre+offset+inset*(i%2 ? -.14 : .14);
      // Large coloured planes, rather than coloured side walls alone, make the
      // silver / lilac / cobalt contrast readable at ordinary camera distance.
      box([left, lo+.018, 8-ridge], [seam+.012, hi-.018, 8+ridge], colour.facet, {
        east:colour.shade, west:'light_blue', up:colour.pale, down:'blue',
      });
      box([seam, lo+.018, 8-ridge-.006], [right, hi-.018, 8+ridge+.006], colour.core, {
        east:'cyan', west:colour.shade, up:colour.pale, down:colour.shade,
      });
      if (i < 11) {
        // A pale triangular facet grows across the cobalt face. Its stepped
        // boundary and the opposite silver crack suggest interlocking crystal
        // planes without making the thin blade deeper or leaving loose shards.
        const rows = 4;
        const rowHeight = (hi-lo-.07)/rows;
        for (let row=0; row<rows; row++) {
          const t = (row+.5)/rows;
          const spread = .12 + .62*(i%2 ? 1-t : t);
          const facetLeft = right-(right-seam)*spread;
          const y0 = lo+.035+row*rowHeight;
          box([facetLeft, y0, 8-ridge-.020], [right, y0+rowHeight+.005, 8+ridge+.020], colour.pale, {
            east:'white', west:colour.facet,
          });
          const crackX = left + (seam-left)*(.16+.68*(i%2 ? t : 1-t));
          const crackWidth = Math.min(.11, inset*.13);
          box([crackX-crackWidth/2, y0, 8-ridge-.026], [crackX+crackWidth/2, y0+rowHeight+.005, 8+ridge+.026], 'white', {
            east:'light_blue', west:'light_blue',
          });
        }
      }
    });

    // Solid blue/purple guard hub overlaps both grip and blade root.
    guardBox([6.06, 9.97, 7.16], [9.64, 12.05, 8.84], 'blue', {north:'purple', south:'light_blue', up:'white'});
    guardBox([6.81, 10.47, 6.98], [8.91, 12.67, 9.02], colour.facet, {north:colour.pale, south:colour.pale, east:'white', west:'blue'});

    function wing(profile, primary) {
      profile.forEach(([left, right, bottom, top], i) => {
        const depth = (primary ? .32 : .26) + i*.012;
        guardBox([left, bottom, 8-depth], [right, top, 8+depth], 'white', {east:'light_blue', west:'light_gray'});
        const insetX = Math.min(.22, (right-left)*.18);
        const insetY = Math.min(.24, (top-bottom)*.19);
        guardBox([left+insetX, bottom+insetY, 8-depth-.07], [right-insetX, top-insetY, 8+depth+.07], 'purple', {
          north:i%3===1?colour.pale:colour.facet, south:i%3===1?colour.pale:colour.facet, east:'light_blue', west:'blue',
        });
      });
    }
    // The large crescent sweeps around the hand, ending in a slender rear horn.
    // Deliberate 0.18–0.30 overlaps join the curved steps into one silver edge.
    wing([
      [5.20, 7.35, 9.63, 11.23],
      [3.55, 5.48, 8.92, 10.78],
      [2.34, 3.83, 7.55, 10.02],
      [1.49, 2.62, 5.94, 8.04],
      [1.08, 1.76, 4.20, 6.25],
      [1.06, 1.46, 2.73, 4.48],
      [1.18, 1.40, 1.69, 3.02],
    ], true);
    // A shorter opposite wing curls toward the blade, echoing the feather-like
    // white quillons in the reference without making the silhouette symmetrical.
    wing([
      [8.95, 10.76, 10.21, 12.00],
      [10.48, 11.85, 11.42, 13.62],
      [11.58, 12.57, 13.30, 15.46],
      [12.32, 12.93, 15.17, 16.77],
      [12.69, 13.00, 16.50, 17.58],
    ], false);

    // Two attached crystal accents beside the guard. A visible dark setting
    // joins each ornament to the sword so its silhouette cannot look broken.
    function diamond(cx, cy, size, cz=8, halfDepth=.38) {
      const rows = [
        [-1.00,-.43,.32],[-.48,.06,.78],[.01,.52,.84],[.47,1.00,.30],
      ];
      rows.forEach(([lo,hi,w], i) => {
        guardBox([cx-w*size, cy+lo*size, cz-halfDepth], [cx+w*size, cy+hi*size, cz+halfDepth], 'purple', {
          north:i<2?colour.core:colour.pale, south:i<2?colour.facet:colour.pale, east:'white', west:'blue',
        });
      });
    }
    guardBox([2.78, 10.27, 7.79], [5.18, 10.69, 8.21], 'blue');
    diamond(2.55, 10.56, .90);
    guardBox([3.80, 11.39, 7.81], [6.85, 11.80, 8.19], 'blue');
    diamond(3.40, 11.66, .79);

    // The side reference has a raised crystal cluster rather than a flat plate.
    // Front/back gems are seated on explicit sockets; their different depths
    // give the guard volume while leaving the long blade almost paper-thin.
    guardBox([7.63, 10.64, 6.65], [8.37, 12.14, 7.27], 'blue', {west:'purple', east:'light_blue'});
    diamond(8.00, 11.41, 1.04, 6.32, .42);
    guardBox([7.69, 12.47, 6.90], [8.29, 13.26, 7.76], 'blue');
    diamond(7.99, 13.00, .62, 6.65, .36);
    guardBox([7.83, 10.75, 8.78], [8.55, 12.29, 9.34], 'blue', {west:'light_blue', east:'purple'});
    diamond(8.19, 11.52, .91, 9.60, .39);
    return elements;
  }
  return {sword:build(false), cryo_sword:build(true)};
}
