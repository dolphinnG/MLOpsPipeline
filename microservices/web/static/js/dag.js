document.addEventListener('DOMContentLoaded', function() {
    var cy = cytoscape({
        container: document.getElementById('cy'),
        elements: [
            { data: { id: 'a' } },
            { data: { id: 'b' } },
            { data: { id: 'c' } },
            { data: { id: 'd' } },
            { data: { source: 'a', target: 'b' } },
            { data: { source: 'a', target: 'c' } },
            { data: { source: 'b', target: 'd' } },
            { data: { source: 'c', target: 'd' } }
        ],
        style: [
            {
                selector: 'node',
                style: {
                    'background-color': '#666',
                    'label': 'data(id)'
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 3,
                    'line-color': '#ccc',
                    'target-arrow-color': '#ccc',
                    'target-arrow-shape': 'triangle',
                    'arrow-scale': 1.5,
                    'curve-style': 'bezier'
                }
            }
        ],
        layout: {
            name: 'breadthfirst',
            directed: true
        }
    });

    cy.on('tap', 'node[id="b"]', function() {
        alert('node b clicked');
    });
});
