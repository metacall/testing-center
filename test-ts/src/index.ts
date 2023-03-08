import {spawn} from 'child_process';
import * as fs from 'fs';

function getMetacallProcess() {
  const process = spawn('metacall', [], {
    stdio: ['pipe', 'pipe', 'pipe'],
  });
  return process;
}

async function passOptionsToMetacall(
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  process: any,
  options: string[],
  saveOutput = false
) {
  for (const option of options) {
    process.stdin.write(option);
  }
  const [stdout, stderr] = await Promise.all([
    new Promise(resolve => process.stdout.once('data', resolve)),
    new Promise(resolve => process.stderr.once('data', resolve)),
  ]);

  if (process.stdin.writable) {
    process.stdin.end();
  }

  if (typeof stdout === 'string' && typeof stderr === 'string') {
    const outStr = stdout.toString();
    const errStr = stderr.toString();
    if (saveOutput) {
      // eslint-disable-next-line node/no-unsupported-features/node-builtins
      await fs.promises.writeFile('output.txt', outStr);
    }
    return [outStr, errStr];
  }
  return ['', ''];
}

async function main() {
  const process = getMetacallProcess();
  console.log('Process started');
  const [out, err] = await passOptionsToMetacall(process, ['help', 'exit']);
  console.log('Process ended');
  console.log(out);
  console.log(err);
}

main();
