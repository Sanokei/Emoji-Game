const searchInput = document.getElementById('search-input');
const modeToggle = document.getElementById('mode-toggle');
const appContainer = document.querySelector('.app-container');

modeToggle.onclick = () => document.documentElement.classList.toggle('dark-mode');

// removes the alt-click functionality
document.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', function (e) {
      if (e.altKey) {
        e.preventDefault(); // no download
        this.click(); // fake a normal click
      }
    });
  });

//

const ErrorCode = (error) => Toastify({
    text: error,
    duration: 3000,
    style: {
        background: "#BF3F3F",
        fontFamily: 'Inter',
    },
    offset: {
        y: 50 // vertical axis - can be a number or a string indicating unity. eg: '2em'
    },
}).showToast();


const getErrorLines = () => (new Error()).stack.split('\n')[2]?.trim() ?? 'Unknown location';

const search = async query => (await fetch(`/guess?guess=${query}`, {
    method:'POST',
    mode: "cors"
}));

const searchQuery = async () => {
    const query = searchInput.value;
    await search(query).then((response) => {
        if(response.redirected){
            window.location.replace(response.url);
        }
    });
    // window.location.replace();
};

// function delay(fn, ms) {
//     let timer = 0
//     return function(...args) {
//         clearTimeout(timer)
//         timer = setTimeout(fn.bind(this, ...args), ms || 0)
//     }
// }

// searchInput.oninput = delay(searchQuery, 500);

// searchInput.addEventListener('keyup', function(event) {
//     const key = event.key; // const {key} = event; ES6+
//     if (key === "Backspace" || key === "Delete") {
//         disableSearchInput();
//         searchQuery;
//     }
// });
searchInput.addEventListener('keyup', (event) => {
    const key = event.key; // const {key} = event; ES6+
    if (key === "Enter") {
        searchQuery();
    }
});