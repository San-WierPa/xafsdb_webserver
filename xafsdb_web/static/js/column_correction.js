/* Column correction only. All XAS processing uses the server's standard QC. */
(() => {
    'use strict';
    const byId = id => document.getElementById(id);
    const panel = byId('column-correction-panel');
    if (!panel) return;
    const initialPreview = JSON.parse(byId('column-preview-data').textContent);
    const initial = JSON.parse(byId('qc-initial-state').textContent);
    const form = byId('verify_form');
    panel.closest('form').addEventListener('submit',event => event.preventDefault());
    const submit = byId('submit-measurement');
    const apply = byId('apply-columns');
    const status = byId('correction-status');
    const scan = byId('preview-scan');
    const originalPanel = byId('frank-qc-panel').outerHTML;
    const map = {
        energy:['preview-energy','qc-energy-column'], signal_a:['preview-signal-a','qc-signal-a'],
        signal_b:['preview-signal-b','qc-signal-b'], formula:['preview-formula','qc-formula'],
        scan:['preview-scan','qc-scan'], energy_unit:['preview-energy-unit','qc-energy-unit'],
        reference_enabled:['reference-enabled','qc-reference-enabled'], reference_a:['reference-a','qc-reference-a'],
        reference_b:['reference-b','qc-reference-b'], reference_formula:['reference-formula','qc-reference-formula']
    };
    const originalMetadata = Object.fromEntries(['Source','Element','Edge'].map(id => [id,byId(id).value]));
    let generation = 0, scanGeneration = 0, confirmed = false, busy = false, columnsReady = true, manualEdge = false;
    let controller;
    let currentPreview = initialPreview;

    // A raw signal preview only: automatic XAS processing remains on the server.
    function previewPlots() {
        const container = byId('column-plot-preview'), note = byId('column-plot-note');
        container.replaceChildren();
        if (!columnsReady) { note.textContent = 'Reading scan data for the preview.'; return; }
        const energyIndex = Number(byId('preview-energy').value);
        const energies = currentPreview.columns[energyIndex] || [];
        const finiteEnergy = energies.filter(value => value !== null && Number.isFinite(value)).sort((a,b) => a-b);
        const requested = byId('preview-energy-unit').value;
        const declared = (currentPreview.units || [])[energyIndex];
        const median = finiteEnergy.length ? (finiteEnergy[Math.floor((finiteEnergy.length-1)/2)] + finiteEnergy[Math.floor(finiteEnergy.length/2)])/2 : 0;
        const convert = requested === 'keV' || (requested === 'auto' &&
            (declared === 'keV' || (declared !== 'eV' && declared !== 'keV' && median > 0 && median < 100)));
        const columnName = index => `${Number(index)+1}: ${currentPreview.labels[index]}`;
        const descriptions = [];
        function draw(title, aId, bId, formulaId, color) {
            const aIndex = byId(aId).value, bIndex = byId(bId).value;
            const a = currentPreview.columns[Number(aIndex)] || [], b = currentPreview.columns[Number(bIndex)] || [];
            const formula = byId(formulaId).value;
            const expression = formula === 'raw' ? columnName(aIndex) :
                `${formula === 'log_ratio' ? 'ln' : formula === 'negative_log_ratio' ? '-ln' : ''}(${columnName(aIndex)} / ${columnName(bIndex)})`;
            const figure = document.createElement('figure');
            figure.style.cssText = 'margin:16px 0;padding:10px;border:1px solid #d6dee7;border-radius:6px;background:white';
            const caption = document.createElement('figcaption');
            caption.textContent = `${title}: ${expression}`;
            caption.style.cssText = 'font-size:12px;overflow-wrap:anywhere;margin-bottom:6px';
            figure.append(caption); container.append(figure);
            const points = energies.map((energy,i) => {
                if (energy === null || !Number.isFinite(energy) || a[i] === null || !Number.isFinite(a[i])) return null;
                let y = a[i];
                if (formula !== 'raw') {
                    if (b[i] === null || !Number.isFinite(b[i]) || b[i] === 0) return null;
                    y /= b[i];
                    if (formula !== 'ratio') {
                        if (y <= 0) return null;
                        y = Math.log(y) * (formula === 'negative_log_ratio' ? -1 : 1);
                    }
                }
                return Number.isFinite(y) ? [energy * (convert ? 1000 : 1), y] : null;
            });
            const valid = points.filter(Boolean);
            const omitted = points.length - valid.length;
            if (valid.length < 2) {
                const warning = document.createElement('p');
                warning.textContent = 'No plottable curve. Check the selected columns, zero denominators and logarithm inputs.';
                warning.style.fontSize = '13px'; figure.append(warning);
                descriptions.push(`${title}: insufficient valid points.`); return;
            }
            let xmin=Infinity,xmax=-Infinity,ymin=Infinity,ymax=-Infinity;
            for (const [x,y] of valid) { xmin=Math.min(xmin,x);xmax=Math.max(xmax,x);ymin=Math.min(ymin,y);ymax=Math.max(ymax,y); }
            if (xmin === xmax) {
                const warning = document.createElement('p'); warning.textContent = 'Choose an energy column with changing values.';
                figure.append(warning); descriptions.push(`${title}: constant energy.`); return;
            }
            const padding = ymax === ymin ? Math.max(Math.abs(ymin)*0.05,0.5) : (ymax-ymin)*0.06;
            ymin-=padding;ymax+=padding;
            const svg = document.createElementNS('http://www.w3.org/2000/svg','svg');
            svg.setAttribute('viewBox','0 0 500 260'); svg.setAttribute('role','img');
            svg.setAttribute('aria-label',`${title} signal versus energy in electronvolts`);
            svg.style.cssText='display:block;width:100%;height:auto';
            const el = (tag,attrs,text) => {
                const item=document.createElementNS('http://www.w3.org/2000/svg',tag);
                for (const [key,value] of Object.entries(attrs)) item.setAttribute(key,String(value));
                if (text !== undefined) item.textContent=text;
                svg.append(item);return item;
            };
            const xpixel = x => 72+(x-xmin)/(xmax-xmin)*405;
            const ypixel = y => 210-(y-ymin)/(ymax-ymin)*190;
            const tick = value => Number(value.toPrecision(5)).toString();
            for(let i=0;i<=4;i++) {
                const x=xmin+(xmax-xmin)*i/4,y=ymin+(ymax-ymin)*i/4;
                el('line',{x1:72,y1:ypixel(y),x2:477,y2:ypixel(y),stroke:'#e3e9ef'});
                el('text',{x:xpixel(x),y:228,'text-anchor':'middle','font-size':11,fill:'#435465'},tick(x));
                el('text',{x:65,y:ypixel(y)+4,'text-anchor':'end','font-size':11,fill:'#435465'},tick(y));
            }
            el('path',{d:'M72 20 V210 H477',fill:'none',stroke:'#607183'});
            let path='', connected=false;
            // Break at invalid rows instead of connecting across missing data.
            for(const point of points) {
                if(!point){connected=false;continue;}
                path+=(connected?'L':'M')+xpixel(point[0]).toFixed(2)+' '+ypixel(point[1]).toFixed(2)+' ';
                connected=true;
            }
            el('path',{d:path,fill:'none',stroke:color,'stroke-width':1.8,'data-signal':title.toLowerCase()});
            el('text',{x:275,y:251,'text-anchor':'middle','font-size':12,fill:'#435465'},'Energy (eV)');
            el('text',{transform:'translate(14 115) rotate(-90)','text-anchor':'middle','font-size':12,fill:'#435465'},'Signal');
            figure.append(svg);
            descriptions.push(`${title}: ${valid.length} preview points${omitted ? `; ${omitted} invalid rows omitted` : ''}.`);
        }
        draw('Sample','preview-signal-a','preview-signal-b','preview-formula','#123e63');
        if(byId('reference-enabled').value === 'yes') draw('Reference','reference-a','reference-b','reference-formula','#a35418');
        note.textContent = descriptions.join(' ') +
            (currentPreview.original_points > currentPreview.displayed_points ? ' Preview uses a reduced set of rows.' : '') +
            ' Unprocessed signals with separate scales. Apply columns to update QC using the full data.';
    }

    function message(text, ready=false) {
        status.textContent = text;
        status.className = 'preview-status ' + (ready ? 'ready' : 'review');
    }
    function buttons() {
        submit.disabled = !confirmed || busy || !columnsReady;
        apply.disabled = busy || !columnsReady;
        apply.textContent = busy ? 'Applying columns…' : 'Apply columns';
    }
    function dirty() {
        generation++;
        if (controller) controller.abort();
        busy = false; confirmed = false;
        byId('qc-confirmation').value = '';
        message('Changes are not applied. Apply columns to update QC before submitting.');
        buttons();
    }
    function signalControls() {
        const sampleRaw = byId('preview-formula').value === 'raw';
        byId('sample-b-label').hidden = sampleRaw;
        byId('sample-a-label').querySelector('span').textContent = sampleRaw ? 'Sample absorption column' : 'Sample signal A (numerator)';
        const reference = byId('reference-enabled').value === 'yes';
        const referenceRaw = byId('reference-formula').value === 'raw';
        byId('reference-fields').hidden = !reference;
        byId('reference-b-label').hidden = referenceRaw;
        byId('reference-a-label').querySelector('span').textContent = referenceRaw ? 'Reference absorption column' : 'Reference signal A (numerator)';
        byId('reference-note').textContent = reference
            ? 'Choose the detector pair or absorption column for the measured reference.'
            : 'No separate reference is supplied. QC will use the sample signal for both inputs; independent reference calibration is unavailable.';
    }
    function fillColumns(preview) {
        currentPreview = preview;
        for (const id of ['preview-energy','preview-signal-a','preview-signal-b','reference-a','reference-b']) {
            const select = byId(id); select.replaceChildren();
            preview.labels.forEach((label,index) => select.add(new Option(`${index+1}: ${label}`,String(index))));
        }
        for (const [key,ids] of Object.entries(map)) {
            if (key !== 'scan') byId(ids[0]).value = String(preview.defaults[key] ?? (key==='energy_unit'?'auto':''));
        }
        byId('preview-energy-unit').value = 'auto';
        byId('scan-selection-wrap').hidden = (preview.scans||[]).length < 2;
        const notes = [...((preview.reading||{}).warnings||[])];
        if (!preview.confident) notes.unshift('Review these column choices against the file header.');
        byId('file-reading-note').textContent = notes.join(' ');
        const header = byId('Header info');
        if (header && preview.header) header.value = preview.header.join('\n');
        signalControls();
        previewPlots();
    }
    function setMetadata(id,value) {
        const control = byId(id);
        if (![...control.options].some(option => option.value === value)) control.add(new Option(value,value));
        control.value = value;
    }
    function restoreAutomatic() {
        generation++; scanGeneration++;
        if (controller) controller.abort();
        busy = false; columnsReady = true; manualEdge = false;
        byId('frank-qc-panel').outerHTML = originalPanel;
        scan.value = '0'; fillColumns(initialPreview);
        for (const [id,value] of Object.entries(originalMetadata)) setMetadata(id,value);
        for (const [,ids] of Object.entries(map)) byId(ids[1]).value = '';
        byId('qc-scan').value = '0'; byId('qc-energy-unit').value = 'auto';
        byId('qc-reference-enabled').value = 'no'; byId('qc-reference-formula').value = 'raw';
        byId('qc-use-column-selection').value = 'no';
        byId('qc-range-min').value = initial.energy_min ?? '';
        byId('qc-range-max').value = initial.energy_max ?? '';
        byId('qc-confirmation').value = initial.confirmation || '';
        confirmed = Boolean(initial.ready);
        message(confirmed ? 'Automatic columns are in use. You can submit the measurement or correct its columns.'
            : 'Automatic QC is unavailable. Review the columns and apply them before submitting.', confirmed);
        buttons();
    }
    for (const item of initialPreview.scans || [{index:0,label:'Table 1'}]) {
        scan.add(new Option(item.label + (item.points ? ` — ${item.points} points` : ''),String(item.index)));
    }
    for (const [key,ids] of Object.entries(map)) {
        if (key === 'scan') continue;
        byId(ids[0]).addEventListener('change',() => { signalControls(); dirty(); previewPlots(); });
    }
    for (const id of ['Source','Element','Edge']) byId(id).addEventListener('change',() => {
        if (id !== 'Source') manualEdge = true;
        dirty();
    });
    scan.addEventListener('change', async () => {
        dirty(); columnsReady = false; buttons(); previewPlots();
        const request = ++scanGeneration;
        const body = new FormData();
        body.set('dataset_name',byId('qc-dataset-name').value); body.set('scan',scan.value);
        body.set('csrfmiddlewaretoken',form.querySelector('[name=csrfmiddlewaretoken]').value);
        message('Reading the selected scan…');
        try {
            const response = await fetch(panel.dataset.scanUrl,{method:'POST',body});
            const value = await response.json();
            if (request !== scanGeneration) return;
            if (!response.ok) throw new Error(value.error || 'This scan could not be read.');
            columnsReady = true; fillColumns(value);
            message('Review the selected scan’s columns, then apply them to update QC.');
        } catch(error) { if (request === scanGeneration) {
            message(error.message);
            byId('column-plot-note').textContent = 'Preview unavailable for this scan. Select another scan or use automatic columns.';
        } }
        finally { if (request === scanGeneration) buttons(); }
    });
    apply.addEventListener('click', async () => {
        if (!columnsReady || busy) return;
        dirty(); busy = true; buttons();
        const request = ++generation;
        controller = new AbortController();
        const chosen = Object.fromEntries(Object.entries(map).map(([key,ids]) => [key,byId(ids[0]).value]));
        const body = new FormData();
        Object.entries(chosen).forEach(([key,value]) => body.set(key,value));
        body.set('dataset_name',byId('qc-dataset-name').value);
        body.set('Source',byId('Source').value);
        body.set('Element',manualEdge ? byId('Element').value : '');
        body.set('Edge',manualEdge ? byId('Edge').value : '');
        body.set('csrfmiddlewaretoken',form.querySelector('[name=csrfmiddlewaretoken]').value);
        message('Applying columns and updating QC…');
        try {
            const response = await fetch(panel.dataset.applyUrl,{method:'POST',body,signal:controller.signal});
            const value = await response.json();
            if (request !== generation) return;
            if (!response.ok) throw new Error(value.error || 'QC could not be completed. Review the columns.');
            byId('frank-qc-panel').outerHTML = value.html;
            for (const [key,ids] of Object.entries(map)) byId(ids[1]).value = chosen[key];
            byId('qc-use-column-selection').value = 'yes';
            byId('qc-confirmation').value = value.confirmation;
            byId('qc-range-min').value = value.energy_min; byId('qc-range-max').value = value.energy_max;
            setMetadata('Source',value.source); setMetadata('Element',value.element); setMetadata('Edge',value.edge);
            confirmed = true;
            message('Columns applied. The QC plots and upload now use these inputs.',true);
        } catch(error) {
            if (request === generation && error.name !== 'AbortError') message(error.message);
        } finally {
            if (request === generation) { busy = false; buttons(); }
        }
    });
    byId('reset-columns').addEventListener('click',restoreAutomatic);
    form.addEventListener('submit',event => {
        if (!confirmed || busy || !columnsReady) {
            event.preventDefault(); message('Apply the current columns before submitting, or use automatic columns.');
        }
    });
    restoreAutomatic();
})();
