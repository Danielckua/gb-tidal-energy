/* Grouped map controls; uses Leaflet and the original exported layer objects. */
(function () {
    'use strict';

    L.Control.ResearchLayers = L.Control.extend({
        options: { position: 'topright' },

        initialize: function (groups, options) {
            L.setOptions(this, options);
            this._groups = groups;
            this._inputs = [];
            this._expanded = false;
        },

        onAdd: function (map) {
            this._inputs = [];
            var container = L.DomUtil.create('div', 'research-layer-control');
            container.setAttribute('role', 'region');
            container.setAttribute('aria-label', 'Map layer controls');
            var header = L.DomUtil.create('div', 'research-layer-header', container);
            var title = L.DomUtil.create('span', 'research-layer-title', header);
            title.textContent = 'Map layers';
            var toggle = L.DomUtil.create('button', 'research-layer-toggle', header);
            toggle.type = 'button';
            toggle.setAttribute('aria-controls', 'research-layer-panel-body');
            var body = L.DomUtil.create('div', 'research-layer-body', container);
            body.id = 'research-layer-panel-body';

            this._groups.forEach(function (group, groupIndex) {
                var fieldset = L.DomUtil.create('fieldset', 'research-layer-group', body);
                var legend = L.DomUtil.create('legend', 'research-layer-group-title', fieldset);
                var groupName = L.DomUtil.create('span', '', legend);
                groupName.textContent = group.name;
                group.layers.forEach(function (entry, entryIndex) {
                    var label = L.DomUtil.create('label', 'research-layer-entry', fieldset);
                    label.title = entry.description;
                    var input = L.DomUtil.create('input', 'research-layer-checkbox', label);
                    input.type = 'checkbox';
                    input.checked = map.hasLayer(entry.layer);
                    input.setAttribute('aria-label', entry.name);
                    var symbol = L.DomUtil.create('span', 'research-layer-symbol', label);
                    symbol.setAttribute('aria-hidden', 'true');
                    if (entry.symbol) {
                        var image = L.DomUtil.create('img', '', symbol);
                        image.src = entry.symbol;
                        image.alt = '';
                        image.width = 16;
                        image.height = 16;
                    } else {
                        symbol.textContent = '—';
                    }
                    var text = L.DomUtil.create('span', 'research-layer-text', label);
                    var name = L.DomUtil.create('span', 'research-layer-name', text);
                    name.textContent = entry.name;
                    if (entry.note) {
                        var note = L.DomUtil.create('span', 'research-layer-note', text);
                        note.id = 'research-layer-note-' + groupIndex + '-' + entryIndex;
                        note.textContent = entry.note;
                        input.setAttribute('aria-describedby', note.id);
                    }
                    if (entry.parameters) {
                        var parameters = L.DomUtil.create('span', 'research-layer-parameters', text);
                        parameters.id = 'research-layer-parameters-' + groupIndex + '-' + entryIndex;
                        entry.parameters.forEach(function (criterion) {
                            L.DomUtil.create('span', '', parameters).textContent = criterion;
                        });
                        input.setAttribute('aria-describedby', parameters.id);
                    }
                    L.DomEvent.on(input, 'change', function () {
                        if (input.checked) {
                            map.addLayer(entry.layer);
                        } else {
                            map.removeLayer(entry.layer);
                        }
                    });
                    this._inputs.push({ input: input, layer: entry.layer });
                }, this);
            }, this);

            this._container = container;
            this._toggle = toggle;
            this._body = body;
            this._title = title;
            L.DomEvent.on(toggle, 'click', function () {
                this._setExpanded(!this._expanded);
            }, this);
            L.DomEvent.on(container, 'keydown', function (event) {
                if (event.key === 'Escape' && this._expanded) {
                    this._setExpanded(false);
                    toggle.focus();
                }
                L.DomEvent.stopPropagation(event);
            }, this);
            L.DomEvent.disableClickPropagation(container);
            L.DomEvent.disableScrollPropagation(container);
            map.on('layeradd layerremove', this._sync, this);
            this._setExpanded(false);
            return container;
        },

        onRemove: function (map) {
            map.off('layeradd layerremove', this._sync, this);
        },

        _sync: function () {
            this._inputs.forEach(function (entry) {
                entry.input.checked = this._map.hasLayer(entry.layer);
            }, this);
        },

        _setExpanded: function (expanded) {
            this._expanded = expanded;
            this._container.classList.toggle('research-layer-control-open', expanded);
            this._body.hidden = !expanded;
            this._title.hidden = !expanded;
            this._toggle.textContent = expanded ? 'Hide' : 'Layers';
            this._toggle.setAttribute('aria-label', expanded ? 'Hide layers' : 'Show layers');
            this._toggle.setAttribute('aria-expanded', String(expanded));
        }
    });
    L.control.researchLayers = function (groups, options) {
        return new L.Control.ResearchLayers(groups, options);
    };
}());
