console.log("External JS loaded");

function handleSubmit(form) {
    const vulnIndex = sessionStorage.getItem("vulnIndex");
    const actionWithVuln = form.action + '?vuln=' + vulnIndex;

    fetch(actionWithVuln, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(res => res.text())
    .then(html => {
        const match = html.match(/alert\(['"](.*?)['"]\)/);
        if (match) {
            alert(match[1]);
        }
    });

    return false; // prevent full page reload
}

// Pick vulnerable index ONCE per tab session
const userCount = 500;
if (!sessionStorage.getItem("vulnIndex")) {
    const randomIndex = Math.floor(Math.random() * userCount) + 1;
    sessionStorage.setItem("vulnIndex", randomIndex);
}

// Inject DOM comment into vulnerable form
document.querySelectorAll("form").forEach((form, idx) => {
    if ((idx + 1) === parseInt(sessionStorage.getItem("vulnIndex"))) {
        form.appendChild(document.createComment(" TO DO: fix this "));
    }
});