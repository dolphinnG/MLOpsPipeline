document.addEventListener("DOMContentLoaded", function () {
    const services = {
        "loadModelBtn": "/scheduler/load_model",
        "unloadModelBtn": "/scheduler/unload_model",
        "startExperimentBtn": "/scheduler/start_experiment",
        "stopExperimentBtn": "/scheduler/stop_experiment",
        "loadPipelineBtn": "/scheduler/load_pipeline",
        "unloadPipelineBtn": "/scheduler/unload_pipeline",
        "serverStatusBtn": "/scheduler/server_status",
        "modelStatusBtn": "/scheduler/model_status",
        "pipelineStatusBtn": "/scheduler/pipeline_status",
        "experimentStatusBtn": "/scheduler/experiment_status",
        "schedulerStatusBtn": "/scheduler/scheduler_status"
    };

    function fetchData(endpoint, data, responseDiv, form) {
        fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
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
            if (formId === "loadPipelineForm") {
                // Clear additional forms in the Load Pipeline tab
                document.getElementById("steps").innerHTML = "";
                document.getElementById("outputSteps").innerHTML = "";
            }
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
            const data = {};

            if (evt.target.id === "loadModelForm") {
                data.model = {
                    meta: {
                        name: formData.get("model.meta.name")
                    },
                    modelSpec: {
                        uri: formData.get("model.modelSpec.uri"),
                        requirements: formData.get("model.modelSpec.requirements").split(',')
                    }
                };
            } else if (evt.target.id === "unloadModelForm") {
                data.model = {
                    name: formData.get("model.name")
                };
            } else if (evt.target.id === "startExperimentForm") {
                const candidates = [];
                formData.forEach((value, key) => {
                    const match = key.match(/experiment\.candidates\[(\d+)\]\.(name|weight)/);
                    if (match) {
                        const index = parseInt(match[1]);
                        const field = match[2];
                        if (!candidates[index]) {
                            candidates[index] = {};
                        }
                        candidates[index][field] = field === "weight" ? parseInt(value) : value;
                    }
                });
                data.experiment = {
                    name: formData.get("experiment.name"),
                    default: formData.get("experiment.default"),
                    candidates: candidates,
                    resourceType: formData.get("experiment.resourceType")
                };
            } else if (evt.target.id === "stopExperimentForm") {
                data.name = formData.get("name");
            } else if (evt.target.id === "loadPipelineForm") {
                const steps = [];
                formData.forEach((value, key) => {
                    const match = key.match(/pipeline\.steps\[(\d+)\]\.(name|tensorMap\[(\d+)\]\.(source|target)|inputs\[(\d+)\])/);
                    if (match) {
                        const index = parseInt(match[1]);
                        const field = match[2];
                        if (!steps[index]) {
                            steps[index] = { inputs: [], tensorMap: {} };
                        }
                        if (field.startsWith("tensorMap")) {
                            const tensorMapIndex = parseInt(match[3]);
                            const tensorMapField = match[4];
                            if (!steps[index].tensorMap[tensorMapIndex]) {
                                steps[index].tensorMap[tensorMapIndex] = {};
                            }
                            if (tensorMapField === "source") {
                                steps[index].tensorMap[tensorMapIndex].source = value;
                            } else if (tensorMapField === "target") {
                                steps[index].tensorMap[tensorMapIndex].target = value;
                            }
                        } else if (field.startsWith("inputs")) {
                            const inputIndex = parseInt(match[5]);
                            steps[index].inputs[inputIndex] = value;
                        } else {
                            steps[index][field] = value;
                        }
                    }
                });
                const outputSteps = [];
                formData.forEach((value, key) => {
                    const match = key.match(/pipeline\.output\.steps\[(\d+)\]/);
                    if (match) {
                        const index = parseInt(match[1]);
                        outputSteps[index] = value;
                    }
                });
                data.pipeline = {
                    name: formData.get("pipeline.name"),
                    steps: steps.map(step => ({
                        ...step,
                        tensorMap: Object.fromEntries(
                            Object.values(step.tensorMap).map(({ source, target }) => [source, target])
                        )
                    })),
                    output: {
                        steps: outputSteps
                    }
                };
            } else if (evt.target.id === "serverStatusForm") {
                data.subscriberName = formData.get("subscriberName");
            } else {
                formData.forEach((value, key) => {
                    data[key] = value;
                });
            }

            const responseDiv = document.getElementById("response");
            fetchData(services[evt.target.id.replace("Form", "Btn")], data, responseDiv, evt.target);
        });
    }
});