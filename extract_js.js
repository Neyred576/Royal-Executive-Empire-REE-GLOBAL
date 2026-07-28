const fs = require('fs');
const html = fs.readFileSync('admin/index.html', 'utf-8');
const parts = html.split('<script>');
const scriptBody = parts[parts.length - 1].split('</script>')[0];
fs.writeFileSync('t2.js', scriptBody);
