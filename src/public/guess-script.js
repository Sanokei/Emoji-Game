const goBackButton = document.getElementById('goback-button');

const goback = async () => {
    const score = 0;
    await fetch(`/?score=${score}`, {
        method:'POST',
        mode: "cors"
    }).then((response) => {
        if(response.redirected){
            window.location.replace(response.url);
        }
    });
};

goBackButton.addEventListener("click", () => {
    goback();
});