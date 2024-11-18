document.addEventListener("DOMContentLoaded", function () {
    const services = {
        "serverLiveBtn": "/dataplane/server_live",
        "serverReadyBtn": "/dataplane/server_ready",
        "modelReadyBtn": "/dataplane/model_ready",
        "serverMetadataBtn": "/dataplane/server_metadata",
        "modelMetadataBtn": "/dataplane/model_metadata",
        "modelInferBtn": "/dataplane/model_infer_UI"
    };

    function fetchData(endpoint, data, responseDiv, form, headers = {}) {
        fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...headers
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            responseDiv.innerHTML = '';
            if (form.id === "modelInferForm") {
                const pre = document.createElement("pre");
                pre.textContent = JSON.stringify(data, null, 2); // Display raw JSON prettily
                pre.style.backgroundColor = "#9d9b9b"; // Set background to grey
                responseDiv.appendChild(pre);
            } else {
                if (Object.keys(data).length === 0) {
                    responseDiv.textContent = "Operation completed, nothing to display.";
                } else {
                    responseDiv.appendChild(generateHTML(data));
                }
            }
            responseDiv.style.display = "block"; // Show the response div after submission
            form.style.display = "none"; // Hide the form after submission
        })
        .catch(error => {
            responseDiv.innerHTML = `<pre>${error}</pre>`;
            responseDiv.style.display = "block"; // Show the response div after submission
            form.style.display = "none"; // Hide the form after submission
        });
    }

    function fetchStatus(endpoint, responseDiv) {
        fetch(endpoint, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            responseDiv.innerHTML = '';
            if (Object.keys(data).length === 0) {
                responseDiv.textContent = "Operation completed, nothing to display.";
            } else {
                responseDiv.appendChild(generateHTML(data));
            }
            responseDiv.style.display = "block"; // Show the response div after submission
        })
        .catch(error => {
            responseDiv.innerHTML = `<pre>${error}</pre>`;
            responseDiv.style.display = "block"; // Show the response div after submission
        });
    }

    function generateHTML(data) {
        if (typeof data === 'object' && data !== null) {
            const ul = document.createElement('ul');
            for (const key in data) {
                const li = document.createElement('li');
                if (!/^\d+$/.test(key)) { // Check if the key is not a number
                    const keySpan = document.createElement('span');
                    keySpan.style.fontWeight = 'bold';
                    keySpan.textContent = `${key}: `;
                    li.appendChild(keySpan);
                }
                li.appendChild(generateHTML(data[key]));
                ul.appendChild(li);
            }
            return ul;
        } else {
            const textNode = document.createTextNode(data);
            return textNode;
        }
    }

    function openTab(evt, tabId) {
        const tablinks = document.getElementsByClassName("tablinks");
        for (let i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
        }
        evt.currentTarget.className += " active";

        const tabforms = document.getElementsByClassName("tabform");
        for (let i = 0; i < tabforms.length; i++) {
            tabforms[i].style.display = "none";
            tabforms[i].reset(); // Reset the form
        }
        const formId = tabId.replace("Btn", "Form");
        const formElement = document.getElementById(formId);
        if (formElement) {
            formElement.style.display = "block";
        } else {
            fetchStatus(services[tabId], document.getElementById("response"));
        }

        // Reset and hide the response div
        const responseDiv = document.getElementById("response");
        responseDiv.innerHTML = "";
        responseDiv.style.display = "none";
    }

    const tablinks = document.getElementsByClassName("tablinks");
    for (let i = 0; i < tablinks.length; i++) {
        tablinks[i].addEventListener("click", function (evt) {
            openTab(evt, tablinks[i].id);
        });
    }

    const tabforms = document.getElementsByClassName("tabform");
    for (let i = 0; i < tabforms.length; i++) {
        tabforms[i].addEventListener("submit", function (evt) {
            evt.preventDefault();
            const formData = new FormData(evt.target);
            let data = {};
            const headers = {};

            if (evt.target.id === "modelInferForm") {
                headers["seldon-model"] = formData.get("seldon-model");
                try {
                    data = formData.get("model.data");
                } catch (error) {
                    const responseDiv = document.getElementById("response");
                    responseDiv.innerHTML = `<pre>Invalid JSON: ${error}</pre>`;
                    responseDiv.style.display = "block";
                    return;
                }
            } else if (evt.target.id === "modelReadyForm" || evt.target.id === "modelMetadataForm") {
                data.name = formData.get("model.name");
            } else {
                formData.forEach((value, key) => {
                    data[key] = value;
                });
            }

            const responseDiv = document.getElementById("response");
            fetchData(services[evt.target.id.replace("Form", "Btn")], data, responseDiv, evt.target, headers);
        });
    }
});