// Copy the bundled news image to MAKEFUN_OUTPUT_DIR (default: /output).
import { copyFile, mkdir, readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const source = fileURLToPath(new URL('./entry.png', import.meta.url));
const outputDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? '/output');

try {
  try {
    await readFile(source);
  } catch (error) {
    throw new Error(`Cannot read bundled image at ${source}. Ensure entry.png is beside main.ts. ${error.message}`);
  }
  await mkdir(outputDir, { recursive: true });
  await copyFile(source, resolve(outputDir, 'entry.png'));
} catch (error) {
  console.error(`Image copy failed: ${error.message}`);
  process.exitCode = 1;
}
