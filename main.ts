// news-image-20261121 — entry program (Node 22, standard library only).
//
// The entry is a single JPEG newspaper front page for Saturday 21 November
// 2026, stored beside this file as entry.png. This program does not draw or
// fetch anything: it loads the bundled bytes, proves they are a complete
// 1024x1024 JPEG, and only then copies the exact bytes to the output path.
// After writing it reads the file back and refuses to exit cleanly unless
// the copy matches the source byte for byte (length and SHA-256).
//
// Usage:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from "node:crypto";
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const EXPECTED_WIDTH = 1024;
const EXPECTED_HEIGHT = 1024;
const MAX_BYTES = 1_048_576;

function fail(message) {
  console.error(`entry: ${message}`);
  process.exit(1);
}

function sha256Hex(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

// Walk the JPEG marker segments from the start of the buffer and return the
// width/height carried by the first Start-Of-Frame marker (SOF0/SOF1/SOF2).
// Returns null when no frame header is found before the scan data begins.
function frameSize(jpeg) {
  let cursor = 2; // skip the SOI marker (FFD8)
  while (cursor + 9 <= jpeg.length) {
    if (jpeg[cursor] !== 0xff) return null;
    const marker = jpeg[cursor + 1];
    if (marker === 0xd8 || marker === 0x01 || (marker >= 0xd0 && marker <= 0xd7)) {
      cursor += 2;
      continue;
    }
    if (marker === 0xda) return null; // SOS: scan data follows, no SOF seen
    const segmentLength = jpeg.readUInt16BE(cursor + 2);
    if (segmentLength < 2 || cursor + 2 + segmentLength > jpeg.length) return null;
    const isFrame = marker === 0xc0 || marker === 0xc1 || marker === 0xc2;
    if (isFrame) {
      // Layout of a frame segment: length(2) precision(1) height(2) width(2)
      // components(1) then 3 bytes per component. A real baseline frame has
      // 1-4 components and an 8-bit sample precision.
      const precision = jpeg[cursor + 4];
      const components = jpeg[cursor + 9];
      if (precision !== 8) return null;
      if (components < 1 || components > 4) return null;
      if (segmentLength < 8 + 3 * components) return null;
      const height = jpeg.readUInt16BE(cursor + 5);
      const width = jpeg.readUInt16BE(cursor + 7);
      return { width, height };
    }
    cursor += 2 + segmentLength;
  }
  return null;
}

function checkJpeg(bytes) {
  if (bytes.length < 4) fail("image is too short to be a JPEG");
  if (bytes[0] !== 0xff || bytes[1] !== 0xd8) fail("image does not start with the JPEG SOI marker");
  if (bytes[bytes.length - 2] !== 0xff || bytes[bytes.length - 1] !== 0xd9) {
    fail("image does not end with the JPEG EOI marker");
  }
  if (bytes.length > MAX_BYTES) fail(`image is ${bytes.length} bytes, over the 1 MiB limit`);
  const size = frameSize(bytes);
  if (size === null) fail("no JPEG frame header found before the scan data");
  if (size.width !== EXPECTED_WIDTH || size.height !== EXPECTED_HEIGHT) {
    fail(`image is ${size.width}x${size.height}, expected ${EXPECTED_WIDTH}x${EXPECTED_HEIGHT}`);
  }
}

async function main() {
  const here = dirname(fileURLToPath(import.meta.url));
  const sourcePath = resolve(here, "entry.png");
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const targetPath = resolve(outDir, "entry.png");

  const bytes = await readFile(sourcePath);
  checkJpeg(bytes);
  const sourceDigest = sha256Hex(bytes);
  const size = frameSize(bytes);

  await mkdir(outDir, { recursive: true });
  await writeFile(targetPath, bytes);

  const written = await readFile(targetPath);
  if (written.length !== bytes.length) {
    fail(`written file is ${written.length} bytes, source is ${bytes.length}`);
  }
  const writtenDigest = sha256Hex(written);
  if (writtenDigest !== sourceDigest) {
    fail(`written file sha256 ${writtenDigest} does not match source ${sourceDigest}`);
  }
  console.log(`entry: wrote ${targetPath} (${written.length} bytes, ${size.width}x${size.height} JPEG, sha256 ${writtenDigest})`);
}

main().catch((error) => fail(error.message ?? String(error)));
