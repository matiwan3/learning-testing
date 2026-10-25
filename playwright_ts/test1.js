function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function task1() {
  console.log('Starting task 1');
  await sleep(5000); // Simulating a task taking 2 seconds
  console.log('Task 1 complete');
}

async function task2() {
  console.log('Starting task 2');
  await sleep(2000); // Simulating a task taking 3 seconds
  console.log('Task 2 complete');
}

async function main() {
  await Promise.all([task1(), task2()]);
  console.log('All tasks complete');
}

main();
