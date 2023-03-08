'use strict';
Object.defineProperty(exports, 'esModule', {value: true});
exports.hello = void 0;
const world = 'world';
function hello(who = world) {
  return `Hello ${who}! `;
}
exports.hello = hello;

// run the function
console.log(hello());
