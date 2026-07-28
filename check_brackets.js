const fs = require('fs');
const code = fs.readFileSync('t2.js', 'utf-8');

let stack = [];
for (let i = 0; i < code.length; i++) {
  const c = code[i];
  if (c === '{' || c === '(' || c === '[') stack.push({char: c, line: code.substring(0, i).split('\n').length});
  else if (c === '}' || c === ')' || c === ']') {
    const last = stack.pop();
    if (!last) {
      console.log(`Unmatched closing ${c} at line ${code.substring(0, i).split('\n').length}`);
    } else {
      const match = (c === '}' && last.char === '{') || (c === ')' && last.char === '(') || (c === ']' && last.char === '[');
      if (!match) console.log(`Mismatched ${c} at line ${code.substring(0, i).split('\n').length}, expected match for ${last.char} from line ${last.line}`);
    }
  }
}

if (stack.length > 0) {
  console.log('Unclosed brackets remaining:', stack.map(s => `${s.char} from line ${s.line}`));
} else {
  console.log('All brackets match!');
}
