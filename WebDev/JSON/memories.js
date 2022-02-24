function click_memories() {
    var fileContent = "1";
    var bb = new Blob([fileContent], { type: 'text/plain' });
    var a = document.createElement('a');
    a.download = 'select_memories.txt';
    a.href = window.URL.createObjectURL(bb);
    a.click();
}