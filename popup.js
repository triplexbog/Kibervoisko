document.getElementById("btn-pop-up").addEventListener("click", () => {
    new Fancybox(
        [
            {
                src: "<img src='qr.jpg'></img>",
                type: "html",
            },
        ],
        {
        }
    );
});