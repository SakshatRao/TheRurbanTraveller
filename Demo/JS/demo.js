var fileContent = "My epic novel that I don't want to lose.";
var bb = new Blob([fileContent ], { type: 'text/plain' });
var a = document.createElement('a');
a.download = 'download.txt';
a.href = window.URL.createObjectURL(bb);
a.click();
