// Saturday 21 November 2026 — one-image newspaper front page (v3).
//
// The front page is typeset programmatically (render_v3.py) from an
// explicit story list, so every headline and caption is measured before
// it is drawn and nothing can be silently clipped. This program does not
// draw, generate, or alter the picture: it ships the stored bytes
// (entry.png, a JPEG file kept next to this script) to the directory the
// harness asks for, but only after proving the file on disk is exactly
// the v3 front page — byte count and SHA-256 are pinned below, so a stale
// or swapped image is refused instead of shipped. After the copy it reads
// the destination back and compares it with the source, so a silent short
// write or a corrupted disk cannot slip through unnoticed.
//
// Run it locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// Node 22, standard library only. No dependencies, no network.

import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// The v3 front page, produced by render_v3.py: 37 sourced stories,
// a 23-pin world map, a UTC timeline and a date check.
const EXPECTED = {
  bytes: 266300,
  sha256: "d2b918b09691b17bc520844e0d6c6da925c901e1ce0e5355a5b5e2338f0540f3",
  width: 1024,
  height: 1024,
  maxBytes: 1024 * 1024,
};

// Markers that carry no payload length (standalone markers).
const STANDALONE = new Set([0x01, 0xd8, 0xd9, ...[0, 1, 2, 3, 4, 5, 6, 7].map((i) => 0xd0 + i)]);
// Start-of-frame markers that describe the pixel grid.
const FRAME = new Set([0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf]);

function fail(reason) {
  console.error(`front-page v3: refusing to ship — ${reason}`);
  process.exitCode = 1;
  throw new Error(reason);
}

function sha256Hex(data) {
  return createHash("sha256").update(data).digest("hex");
}

// One pass over the JPEG stream. Confirms the SOI/EOI envelope, walks
// every marker segment until the scan data (SOS), and pulls the pixel
// grid out of the first frame segment it meets. Returns everything the
// caller needs in a single plain object.
function scan(jpeg) {
  if (jpeg.length < 8) fail(`file is only ${jpeg.length} bytes`);
  if (jpeg[0] !== 0xff || jpeg[1] !== 0xd8) fail("missing SOI marker FFD8 at the start");
  if (jpeg[jpeg.length - 2] !== 0xff || jpeg[jpeg.length - 1] !== 0xd9) {
    fail("missing EOI marker FFD9 at the end");
  }
  if (jpeg.length > EXPECTED.maxBytes) {
    fail(`file is ${jpeg.length} bytes, over the ${EXPECTED.maxBytes} byte limit`);
  }

  const found = { segments: 0, dqt: false, dht: false, width: 0, height: 0, components: 0, sosAt: -1 };
  let pos = 2; // FFD8 already confirmed
  while (pos + 1 < jpeg.length) {
    if (jpeg[pos] !== 0xff) {
      fail(`byte ${pos} is 0x${jpeg[pos].toString(16)} where a marker prefix 0xff was expected`);
    }
    const marker = jpeg[pos + 1];
    found.segments += 1;
    if (marker === 0xda) {
      found.sosAt = pos;
      break; // scan data follows; nothing more to parse
    }
    if (marker === 0xdb) found.dqt = true;
    if (marker === 0xc4) found.dht = true;
    if (STANDALONE.has(marker)) {
      pos += 2;
      continue;
    }
    if (pos + 4 > jpeg.length) fail(`segment starting at ${pos} is cut off`);
    const declared = jpeg.readUInt16BE(pos + 2);
    if (declared < 2) fail(`segment at ${pos} declares an impossible length ${declared}`);
    if (pos + 2 + declared > jpeg.length) fail(`segment at ${pos} overruns the file`);
    if (FRAME.has(marker)) {
      if (declared - 2 < 6) fail("frame segment is too short to hold dimensions");
      const precision = jpeg[pos + 4];
      found.height = jpeg.readUInt16BE(pos + 5);
      found.width = jpeg.readUInt16BE(pos + 7);
      found.components = jpeg[pos + 9];
      if (precision !== 8) fail(`sample precision is ${precision}, expected 8`);
      if (found.components < 1 || found.components > 4) {
        fail(`component count ${found.components} is outside 1..4`);
      }
    }
    pos += 2 + declared;
  }
  if (found.sosAt < 0) fail("ran out of bytes before the start-of-scan marker");
  if (found.width === 0) fail("no frame segment found before the scan data");
  if (!found.dqt) fail("required quantisation tables (DQT) are absent");
  if (!found.dht) fail("required Huffman tables (DHT) are absent");
  if (found.width !== EXPECTED.width || found.height !== EXPECTED.height) {
    fail(`picture is ${found.width}x${found.height}, expected ${EXPECTED.width}x${EXPECTED.height}`);
  }
  return found;
}

async function main() {
  const scriptDir = dirname(fileURLToPath(import.meta.url));
  const sourcePath = resolve(scriptDir, "entry.png");
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const targetPath = resolve(outDir, "entry.png");

  const original = await readFile(sourcePath);
  if (original.length !== EXPECTED.bytes) {
    fail(`source is ${original.length} bytes, expected the v3 front page at ${EXPECTED.bytes} bytes`);
  }
  const sourceDigest = sha256Hex(original);
  if (sourceDigest !== EXPECTED.sha256) {
    fail(`source sha256 ${sourceDigest} does not match the v3 front page ${EXPECTED.sha256}`);
  }
  const info = scan(original);

  await mkdir(outDir, { recursive: true });
  await writeFile(targetPath, original);

  const shipped = await readFile(targetPath);
  if (!shipped.equals(original)) {
    fail(`copy differs from source (shipped ${shipped.length} bytes, source ${original.length} bytes)`);
  }
  if (sha256Hex(shipped) !== EXPECTED.sha256) fail("copy digest does not match the v3 front page");

  console.log(
    `front-page v3: shipped ${targetPath} — ${shipped.length} bytes, ` +
      `${info.width}x${info.height} JPEG (${info.components} components, ${info.segments} segments), sha256 ${EXPECTED.sha256}`,
  );
}

main().catch((error) => {
  if (process.exitCode !== 1) {
    console.error(`front-page v3: unexpected failure — ${error.message ?? String(error)}`);
    process.exitCode = 1;
  }
});
